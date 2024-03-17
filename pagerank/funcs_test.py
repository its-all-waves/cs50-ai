from pagerank import (
    transition_model,
    sample_pagerank,
    iterate_pagerank,
    DAMPING,
    SAMPLES,
)

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


def test_sample_pagerank(corpus, damping_factor, n):
    result = sample_pagerank(corpus, damping_factor, n)
    print(f"	✅ PASS: sample_pagerank() WHAT DO I DO?")
    # raise NotImplementedError


def test_iterate_pagerank(corpus, damping_factor):
    result = iterate_pagerank(corpus, damping_factor)
    print(f"	✅ PASS: iterate_pagerank() RUNS WITHOUT ERRORS")
    # raise NotImplementedError


# RUN TESTS
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
test_transition_model_1(CORPUS, PAGE, DAMPING)


CORPUS_2 = {
    "1.html": set(),
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
PAGE_2 = "1.html"
test_transition_model_2(CORPUS_2, PAGE_2, DAMPING)


test_sample_pagerank(CORPUS, DAMPING, SAMPLES)

# 3: no links
CORPUS_3 = {
    "1": {"2"},
    "2": {"1", "3"},
    "3": {"2", "4", "5"},
    "4": {"1", "2"},
    "5": set(),
}
RANKS_3 = {
    "1": 0.24178,
    "2": 0.35320,
    "3": 0.19773,
    "4": 0.10364,
    "5": 0.10364,
}
test_iterate_pagerank(CORPUS_3, DAMPING)
