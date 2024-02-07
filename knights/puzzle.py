from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

"""
What is given?
    - the character is either a knight or a knave
    - a knight speaks only truth
    - a knave only lies
"""

# Puzzle 0
# A says "I am both a knight and a knave."
A_says_i_am_both = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    Or(AKnight, AKnave),  # char is a knight or a knave // NOT X-OR!, hence...
    Implication(AKnight, A_says_i_am_both),
    Implication(AKnave, Not(A_says_i_am_both)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A_says_we_are_both_knaves = AKnave
knowledge1 = And(
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
