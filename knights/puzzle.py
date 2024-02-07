from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
A_is_a_knight = AKnight
A_is_a_knave = AKnave

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
B_is_a_knight = BKnight
B_is_a_knave = BKnave

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
C_is_a_knight = CKnight
C_is_a_knave = CKnave

"""
What is given?
    - the character is either a knight or a knave
    - a knight speaks only truth
    - a knave only lies
"""

# Puzzle 0
# A says "I am both a knight and a knave."
A_says = And(A_is_a_knight, A_is_a_knave)
knowledge0 = And(
    Or(A_is_a_knight, A_is_a_knave),  # char is a knight or a knave
    Implication(A_is_a_knight, A_says),  # if A is a knight, what they say is true
    Implication(A_is_a_knave, Not(A_says)),  # if A is a knave, what they say is false
)

# Puzzle 1
# A says "We are both knaves."
A_says = And(A_is_a_knave, B_is_a_knave)
# B says nothing.
knowledge1 = And(
    # TODO
    Or(A_is_a_knight, A_is_a_knave),
    Implication(A_is_a_knight, A_says),
    Implication(A_is_a_knave, Not(A_says)),
    Or(B_is_a_knight, B_is_a_knave),
)

# Puzzle 2
# A says "We are the same kind."
A_says = Or(
    And(A_is_a_knight, B_is_a_knight),
    And(A_is_a_knave, B_is_a_knave),
)
# B says "We are of different kinds."
B_says = Or(
    And(A_is_a_knave, B_is_a_knight),
    And(A_is_a_knight, B_is_a_knave),
)
knowledge2 = And(
    Or(A_is_a_knight, A_is_a_knave),
    Implication(A_is_a_knight, A_says),
    Implication(A_is_a_knave, Not(A_says)),
    Or(B_is_a_knight, B_is_a_knave),
    Implication(B_is_a_knight, B_says),
    Implication(B_is_a_knave, Not(B_says)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
A_says = Or(A_is_a_knight, A_is_a_knave)
# B says "A said 'I am a knave'." AND B says "C is a knave."
B_says_A_said = A_is_a_knave
B_says = And(B_says_A_said, C_is_a_knave)
# C says "A is a knight."
C_says = A_is_a_knight
knowledge3 = And(
    Or(A_is_a_knight, A_is_a_knave),
    Implication(A_is_a_knight, A_says),
    Implication(A_is_a_knave, Not(A_says)),
    Or(B_is_a_knight, B_is_a_knave),
    Implication(B_is_a_knight, B_says),
    Implication(B_is_a_knave, Not(B_says)),
    Or(C_is_a_knight, C_is_a_knave),
    Implication(C_is_a_knight, C_says),
    Implication(C_is_a_knave, Not(C_says)),
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
