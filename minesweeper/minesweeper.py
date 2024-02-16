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

        # compute an array with all available cells
        # TODO is this right? or .height - 1 and .width - 1 ?
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

    def surrounding_cells(self, cell):
        """
        Returns an array of nearby cells.
        """

        # Record nearby mines
        all_surrounding_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell is in bounds and is a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    # if self.board[i][j]:
                    all_surrounding_cells.add((i, j))

        return all_surrounding_cells

    # TODO
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as a move that has been made
        # 2) mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        self.recurse(self.surrounding_cells(cell), count, self.knowledge)

    def add_sentence_to_knowledge(self, cells, count):
        filtered_cells = self.filtered(cells)

        # BUGFIX keeps count from being greater than len(filtered_cells)
        # subtract from count the # of mines removed by filtering
        count -= len(cells & self.mines)

        new_sentence = Sentence(filtered_cells, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

    def filtered(self, cells):
        """Return `cells` with known safes and mines removed"""
        return cells - (self.safes | self.mines)

    def recurse(self, cells, count, knowledge):
        if len(cells) == 0:
            return

        # 3) add a new sentence to the AI's knowledge base
        #     based on the value of `cell` and `count`
        self.add_sentence_to_knowledge(cells, count)

        # 4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base
        self.try_to_eliminate_sentences()

        # 5) add any new sentences to the AI's knowledge base
        #     if they can be inferred from existing knowledge
        self.try_to_infer_new_knowledge()

        # return self.check_recursive_case_and_add_knowledge(cells, count, knowledge)
        # return knowledge

    def try_to_eliminate_sentences(self, some_left=True):
        """
        4) mark any additional cells as safe or as mines
        if it can be concluded based on the AI's knowledge base
        """
        if not some_left:
            return

        some_left = False
        for sentence in self.knowledge:
            if sentence.count == 0 and len(sentence.cells) > 0:
                for cell in sentence.cells.copy():
                    self.mark_safe(cell)
                return self.try_to_eliminate_sentences(some_left=True)
            if sentence.count > 0 and sentence.count == len(sentence.cells):
                for cell in sentence.cells.copy():
                    self.mark_mine(cell)
                    print(": : : ADDED MINE:", cell)
                return self.try_to_eliminate_sentences(some_left=True)

        self.prune_knowledge()
        self.try_to_infer_new_knowledge()

    def try_to_infer_new_knowledge(self):
        """
        5) add any new sentences to the AI's knowledge base
        if they can be inferred from existing knowledge
        """
        if len(self.knowledge) < 2:
            return

        # check each pair of sentences in knowledge for a subset, add new knowledge
        new_knowledge = []
        for sent_A, sent_B in itertools.combinations(self.knowledge, 2):
            if sent_A == sent_B:
                continue
            cells = None
            count = None
            if sent_B.cells.issubset(sent_A.cells):
                cells = self.filtered((sent_A.cells - sent_B.cells))
                count = sent_A.count - sent_B.count
            if sent_A.cells.issubset(sent_B.cells):
                cells = self.filtered((sent_B.cells - sent_A.cells))
                count = sent_B.count - sent_A.count
            if not cells:
                continue

            # add new sentence to knowledge
            new_sentence = Sentence(cells, count)
            if new_sentence not in self.knowledge:
                new_knowledge.append(new_sentence)
            ...

        # exit recursion if no new knowledge discovered
        if new_knowledge == []:
            return

        self.knowledge += new_knowledge
        return self.try_to_eliminate_sentences()

    def prune_knowledge(self):
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

        if len(safe_moves) == 0:
            return None
        return safe_moves.pop()

    # TODO
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = list(self.filtered(self.all_cells))
        if len(possible_moves) == 0:
            return None
        return random.choice(possible_moves)
