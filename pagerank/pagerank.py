import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000
CONVERGENCE_MARGIN = 0.001


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


# TODO DONE
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
        assert sum(transitions.values()) == 1, "Probabilities don't sum to 1!"
        return transitions

    # first, get all the pages from corpus and put them in transitions
    transitions = {pg: 0 for pg in all_pages}

    # calculate proba of choosing each link from this page, populate transitions
    for page in linked_pages:
        transitions[page] = damping_factor / num_links_on_page

    # calculate proba of choosing any other page from corpus, *modify* transitions values
    for page in all_pages:
        transitions[page] += (1 - damping_factor) / num_all_pages

    assert sum(transitions.values()) == 1, "Probabilities don't sum to 1!"
    return transitions


# TODO DONE
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
    page = random.choice(all_pages)
    transitions = transition_model(corpus, page, damping_factor)

    # for remaining samples, generate next from current's transition model
    occurrences = {pg: 0 for pg in corpus.keys()}
    for _ in range(n - 1):
        # split page:weight pairs into corresponding lists
        pages, weights = zip(*transitions.items())

        # select a page based on weight from the transitions model & keep track
        page = random.choices(pages, weights, k=1)[0]
        transitions = transition_model(corpus, page, damping_factor)
        occurrences[page] += 1

    # assign page rank values to each page in the returned dict
    page_ranks = {pg: count / n for pg, count in occurrences.items()}

    assert round(sum(page_ranks.values()), 2) == 1, "Probabilities don't sum to 1!"
    return page_ranks


# TODO DONE
def rank(
    page,
    page_ranks: dict[str, float],
    corpus,
    damping_factor,
):
    """
    Returns the iterative Page Rank of `page` given an existing
    dict of page ranks, corpus, the page for which we want the
    page rank, and the damping factor.
    ```
              1 - d            PR(i)
    PR(p)  =  ⎯⎯⎯  +  d ∑  ⎯⎯⎯⎯⎯⎯
                N         i  NumLinks(i)

            ⬆ term_a        ⬆ term_b
    ```
    `PR(p)` = page rank of given page, `d` = damping factor,
    `N` = total page count, `i` = a page that links to page `p`,
    `PR(i)` = the page rank of a page `i`, `NumLinks(i)` = the
    link count on page `i`
    """
    page_count = len(corpus)
    term_a = (1 - damping_factor) / page_count

    term_b = 0

    # update the summation of term b for any pages with no links
    pages_with_no_links = set(pg for pg in corpus.keys() if len(corpus[pg]) == 0)
    for pg in pages_with_no_links:
        pg_rank = page_ranks[pg]
        term_b += pg_rank / page_count

    # update the summation of term b for all pages that link to the given page
    pages_with_links_to_page = set(pg for pg in corpus.keys() if page in corpus[pg])
    for pg in pages_with_links_to_page:
        pg_rank = page_ranks[pg]
        pg_link_count = len(corpus[pg])
        term_b += pg_rank / pg_link_count

    # multiply the summation by the damping factor
    term_b *= damping_factor

    return (page_rank := term_a + term_b)


# TODO DONE
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
    # initialize each page to a rank of 1 / page count
    page_count = len(corpus)
    page_ranks: dict[str, float] = {pg: 1 / page_count for pg in corpus.keys()}

    # TODO skip iters where ranks already converged... had mucho trouble with this
    # Is there a reason why I *cannot* do this?

    # calculate new rank values until precision converges
    index = -1
    ranks_converged: list[bool] = [False] * page_count
    while True:
        # cycle thru all pages indefinitely
        index = (index + 1) if index < page_count - 1 else (0)

        # update page's rank
        page, old_rank = list(page_ranks.items())[index]
        new_rank = rank(page, page_ranks, corpus, damping_factor)
        page_ranks[page] = new_rank

        # move to next iteration if this rank hasn't converged
        if abs(new_rank - old_rank) > CONVERGENCE_MARGIN:
            continue

        # this page rank has fully converged and return if all ranks converged
        ranks_converged[index] = True
        if all(ranks_converged):
            assert round(sum(page_ranks.values()), 1), "Probabilities don't sum to 1!"
            return page_ranks


if __name__ == "__main__":
    main()
