import itertools
import random

DEBUG_ALL_MINES: set


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

        # DEBUG
        print(f"~ ~ ~ ALL THE MINES: {self.mines}")

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
        return f"{self.cells} = {self.count}"

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
        # self.cells.add(cell)
        # self.count += 1

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
        Returns an array of nearby mines.
        """

        # Record nearby mines
        set_of_nearby_mines = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell is in bounds and is a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    # if self.board[i][j]:
                    set_of_nearby_mines.add((i, j))

        return set_of_nearby_mines

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

        surrounding_cells = self.surrounding_cells(cell)

        # 5) add any new sentences to the AI's knowledge base
        #     if they can be inferred from existing knowledge
        self.check_recursive_case_and_add_knowledge(surrounding_cells, count)

        # print(f": : : : mines: {self.mines or ''}")
        # print(f": : : : : safes: {self.safes or ''}")
        # print(f": : : : : : remaining: {self.safes - self.moves_made or ''}")

    def add_sentence_to_knowledge(self, cells, count):
        surrounding_cells = set(
            filter(
                lambda cell: cell not in self.mines and cell not in self.safes,
                cells,
            )
        )
        new_sentence = Sentence(surrounding_cells, count)
        self.knowledge.append(new_sentence)

    def check_recursive_case_and_add_knowledge(self, cells, count):
        # 3) add a new sentence to the AI's knowledge base
        #     based on the value of `cell` and `count`
        self.add_sentence_to_knowledge(cells, count)

        # 4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base
        self.check_knowledge_for_base_case_and_mark_cells()

        for sentence_A in self.knowledge:
            for sentence_B in self.knowledge:
                if sentence_A == sentence_B:
                    continue
                if len(sentence_A.cells) == 0 or len(sentence_B.cells) == 0:
                    continue

                intersection = sentence_A.cells & sentence_B.cells
                count = min(sentence_A.count, sentence_B.count)
                if intersection and count > 0:
                    for cell in intersection:
                        self.add_knowledge(cell, count)
        self.prune_knowledge()

    def check_knowledge_for_base_case_and_mark_cells(self):
        # 4.1) - NOTE BASE CASE ??? check for easy inferences
        for sentence in self.knowledge:
            if sentence.count == 0 and len(sentence.cells) > 0:
                for cell in sentence.cells.copy():
                    self.mark_safe(cell)
                ...
            if sentence.count > 0 and sentence.count == len(sentence.cells):
                for cell in sentence.cells.copy():
                    self.mark_mine(cell)
                ...
        self.prune_knowledge()

    def prune_knowledge(self):
        knowledge_copy = self.knowledge.copy()
        for sentence in self.knowledge:
            if 0 == len(sentence.cells):
                knowledge_copy.remove(sentence)
        self.knowledge = knowledge_copy

    # TODO
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # return a choice from known safes - moves made
        safe_moves = list(self.safes - self.moves_made)
        # return possible_moves.pop()
        if len(safe_moves) == 0:
            return None
        return random.choice(safe_moves)

    # TODO
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # return a choice from all cells - moves made - known mines
        possible_moves = list(
            self.all_cells - self.moves_made - self.mines - self.safes
        )
        if len(possible_moves) == 0:
            return None
        return random.choice(possible_moves)
