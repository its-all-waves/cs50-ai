import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


# TODO - DONE ?
def transition_model(
    corpus: dict[str, set[str]], page: str, damping_factor: float
) -> dict[str, float]:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # if page has no outgoing links, return the same probability for all pages
    all_pages: list[str] = corpus.keys()
    linked_pages: set[str] = corpus[page]
    num_all_pages = len(all_pages)
    num_links_on_page = len(linked_pages)
    if num_links_on_page == 0:
        transitions: dict[str, float] = {pg: 1 / num_all_pages for pg in all_pages}
        assert sum(transitions.values()) == 1
        return transitions

    # first, get all the pages from corpus and put them in transitions
    transitions = {pg: 0 for pg in all_pages}

    # calculate proba of choosing each link from this page, populate transitions
    for page in linked_pages:
        transitions[page] = damping_factor / num_links_on_page

    # calculate proba of choosing any other page from corpus, *modify* transitions values
    for page in all_pages:
        transitions[page] += (1 - damping_factor) / num_all_pages

    # assert all probabilities add to 1
    assert sum(transitions.values()) == 1
    return transitions


# TODO
def sample_pagerank(
    corpus: dict[str, set[str]], damping_factor: float, n: int
) -> dict[str, float]:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # first sample - randomly select a page
    all_pages = list(corpus.keys())
    first_page = random.choice(all_pages)
    transitions = transition_model(corpus, first_page, damping_factor)

    # TODO do i remove the first page from the sequence i iterate over?
    # TODO do they mean previous or current in the instruction below? ASSUME CURRENT FOR NOW -- seems like problem says this twice
    # for each remaining sample, generate the next from the previous sample's transition model
    appearances = [first_page]
    for i in range(n - 1):
        # get a random choice based on weight
        pages = []
        weights = []
        for _pg, weight in transitions.items():
            pages.append(_pg)
            weights.append(weight)
        next_page = random.choices(pages, weights, k=1)[0]
        # add it to the list
        appearances.append(next_page)
        transitions = transition_model(corpus, next_page, damping_factor)

    # return val - return a Counter() object probably ? { key: num_appearances, ...}
    counts = Counter(appearances)

    page_ranks = {pg: count / n for pg, count in counts.items()}

    # assert that the sum of values in returned dict is 1
    assert sum(page_ranks.values()) == 1
    return page_ranks


# TODO
def iterate_pagerank(
    corpus: dict[str, set[str]], damping_factor: float
) -> dict[str, float]:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # first, assign each page a rank of 1 / page count
    # repeatedly calculate new rank vals based on all current rank vals (using PageRank formula in "Background" section of problem.)
    # a page with no links - interpret as having 1 link for every page (incl self)
    # repeat process until no PR value changes by more than 0.001 from current to new
    # assert that the sum of values in returned dict is 1
    raise NotImplementedError


if __name__ == "__main__":
    main()