import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell is in bounds and is a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.count} {self.cells or '{}'}"
        # return f"{self.cells} = {self.count}"

    # TODO
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    # TODO
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    # TODO
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    # TODO
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge: list[Sentence] = []

        # TODO
        # compute an array with all available cells
        self.all_cells = set(
            (i, j) for i in range(self.height) for j in range(self.width)
        )

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # TODO
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        1) mark the cell as a move that has been made
        2) mark the cell as safe
        3) add a new sentence to the AI's knowledge base
            based on the value of `cell` and `count`
        4) mark any additional cells as safe or as mines
            if it can be concluded based on the AI's knowledge base
        5) add any new sentences to the AI's knowledge base
            if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  # 1)
        self.mark_safe(cell)  # 2)
        self.add_sentence_to_knowledge(self.surrounding_cells(cell), count)  # 3)
        self.try_to_eliminate_sentences_recursively()  # 4), 5)

    # TODO
    def add_sentence_to_knowledge(self, cells, count):
        filtered_cells = self.known_cells_removed(cells)

        # subtract from count the # of mines removed by filtering cells
        count -= len(cells & self.mines)

        new_sentence = Sentence(filtered_cells, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

    # TODO
    def try_to_eliminate_sentences_recursively(self, some_left=True):
        """
        4) mark any additional cells as safe or as mines
        if it can be concluded based on the AI's knowledge base
        """
        # exit recursion if we made no changes in the last cycle
        if not some_left:
            return

        some_left = False
        for sentence in self.knowledge:
            if sentence.count == 0 and len(sentence.cells) > 0:
                # mark cells as safes
                for cell in sentence.cells.copy():
                    self.mark_safe(cell)
                # continue inner recursion, assume there's more to eliminate
                return self.try_to_eliminate_sentences_recursively(some_left=True)
            if sentence.count > 0 and sentence.count == len(sentence.cells):
                # mark cells as mines
                for cell in sentence.cells.copy():
                    self.mark_mine(cell)
                # continue inner recursion, assume there's more to eliminate
                return self.try_to_eliminate_sentences_recursively(some_left=True)

        self.prune_knowledge()

        # continue outer recursion based on pared down knowledge
        self.try_to_infer_new_knowledge()

    # TODO
    def try_to_infer_new_knowledge(self):
        """
        5) add any new sentences to the AI's knowledge base
        if they can be inferred from existing knowledge
        """
        # nothing to infer if only one sentence in knowledge
        if len(self.knowledge) < 2:
            return

        # check each pair of sentences in knowledge subsets, add new knowledge
        new_knowledge = []
        for sent_A, sent_B in itertools.combinations(self.knowledge, 2):
            if sent_A == sent_B:
                continue

            # check for info to construct a new sentence
            cells, count = None, None
            if sent_B.cells.issubset(sent_A.cells):
                cells = self.known_cells_removed(sent_A.cells - sent_B.cells)
                count = sent_A.count - sent_B.count
            if sent_A.cells.issubset(sent_B.cells):
                cells = self.known_cells_removed(sent_B.cells - sent_A.cells)
                count = sent_B.count - sent_A.count
            if not cells:
                continue

            # got info needed, so add new sentence to knowledge
            new_sentence = Sentence(cells, count)
            if new_sentence not in self.knowledge:
                new_knowledge.append(new_sentence)

        # exit this recursion phase if nothing could be inferred
        if new_knowledge == []:
            return

        # new knowledge found, so add it to knowledge
        self.knowledge += new_knowledge

        # continue outer recursion based on updated knowledge
        return self.try_to_eliminate_sentences_recursively()

    # TODO
    def surrounding_cells(self, cell):
        """
        Returns an array of nearby cells.
        """
        # record cells within 1 row and col of cell, excluding cell
        all_surrounding_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue

                # if this is a valid cell, add it to the return value
                if 0 <= i < self.height and 0 <= j < self.width:
                    all_surrounding_cells.add((i, j))

        return all_surrounding_cells

    # TODO
    def known_cells_removed(self, cells):
        """Return `cells` with known safes and mines removed"""
        return cells - (self.safes | self.mines)

    # TODO
    def prune_knowledge(self):
        """Remove empty sentences and duplicates from knowledge"""
        # remove empty sentences
        knowledge_copy = self.knowledge.copy()
        for sentence in self.knowledge:
            if 0 == len(sentence.cells):
                knowledge_copy.remove(sentence)

        # remove duplicates
        no_duplicates = []
        for sentence in knowledge_copy:
            if sentence not in no_duplicates:
                no_duplicates.append(sentence)

        self.knowledge = no_duplicates

    # TODO
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = list(self.safes - self.moves_made)
        return safe_moves[0] if len(safe_moves) > 0 else None

    # TODO
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        avail_moves = list(self.known_cells_removed(self.all_cells))
        return avail_moves[0] if len(avail_moves) > 0 else None
