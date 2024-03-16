from pagerank import transition_model, DAMPING, SAMPLES

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


def test_transition_model(corpus, page, damping_factor):
    transitions = transition_model(corpus, page, damping_factor)

    for key, value in (items := transitions.items()):
        transitions[key] = round(value, ndigits=3)

    assert transitions == TRANSITION_MODEL
    print(f"	✅ PASS: transition_model()")


# RUN TESTS
test_transition_model(CORPUS, PAGE, DAMPING)
