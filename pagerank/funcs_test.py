from pagerank import transition_model, DAMPING, SAMPLES

# TEST DATA
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CORPUS = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}

TRANSITION_MODEL = {
    "1.html": 0.05,
    "2.html": 0.475,
    "3.html": 0.475,
}

PAGE = "1.html"

# TESTS
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def test_transition_model_1(corpus, page, damping_factor):
    transitions = transition_model(corpus, page, damping_factor)
    for key, value in (items := transitions.items()):
        transitions[key] = round(value, ndigits=3)
    assert transitions == TRANSITION_MODEL
    print(f"	✅ PASS: transition_model() solves given test case")


def test_transition_model_2(corpus, page, damping_factor):
    transitions = transition_model(corpus, page, damping_factor)
    assert all(val == 1 / len(corpus.keys()) for val in transitions.values())
    print(f"	✅ PASS: transition_model() returns equal proba when page has no links")


# RUN TESTS
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
test_transition_model_1(CORPUS, PAGE, DAMPING)


CORPUS_2 = {
    "1.html": set(),
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
PAGE_2 = "1.html"
test_transition_model_2(CORPUS_2, PAGE_2, DAMPING)
