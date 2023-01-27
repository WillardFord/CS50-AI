import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000

# Haven't set up a system for dealing with identical links on same page yet.

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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transition_dist = {}

    minimum_prob = (1-damping_factor)/len(corpus)
    if len(corpus[page]) != 0:
        inv_num_links = 1/len(corpus[page])
        for site in corpus:
            if site in corpus[page] and site is not page:
                transition_dist[site] = minimum_prob + damping_factor*inv_num_links
            else:
                transition_dist[site] = minimum_prob
    else:
        for site in corpus:
            transition_dist[site] = 1/len(corpus)
    sum = 0
    for site in transition_dist.keys():
        sum += transition_dist[site]
    if sum < .99:
        for site in transition_dist.keys():
            transition_dist[site] = transition_dist[site]/sum
    return transition_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visit_counts = {}

    transition_dists = {}
    for site in corpus:
        transition_dists[site] = transition_model(corpus, site, damping_factor)

    # Add random for curr_site
    curr_site = random.choice(list(corpus.keys()))
    curr_dist = {}
    for i in range(n):
        visit_counts[curr_site] = visit_counts.setdefault(curr_site, 0) +1
        curr_dist = transition_dists[curr_site]
        curr_site = random.choices(list(curr_dist.keys()), list(curr_dist.values()))[-1]
        

    probability_dist = {}
    for site in corpus:
        probability_dist[site] = visit_counts.setdefault(site, 0)/n
    return probability_dist

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    PageRanks = {}
    
    for page in corpus.keys():
        PageRanks[page] = 1/len(corpus)

    inputs_dictionary = find_inputs(corpus)
    change = 1
    default_value = (1-damping_factor)/len(corpus)
    while np.abs(change) > .00001:
        changes = set()
        for page in PageRanks.keys():
            weighted_value = calculate_weighted(inputs_dictionary[page], PageRanks, corpus)
            page_rank = default_value + damping_factor*(weighted_value)
            changes.add(PageRanks[page]-page_rank)
            PageRanks[page] = page_rank
        change = max(changes)
    return PageRanks

def find_inputs(corpus): # {a:(c, b), b:(a), c(b)} -> {a:(b), b:(c,a), c:(a)}
    dictionary = {}
    for page in corpus.keys():
        if len(corpus[page]) == 0:
            page_links = corpus.keys()
        else:
            page_links = corpus[page]
        for linked_page in page_links:
            input = dictionary.setdefault(linked_page, set())
            input.add(page)
            dictionary[linked_page] = input
    return dictionary

def calculate_weighted(linking_pages, PageRanks, corpus):
    weighted_value = 0
    for page in linking_pages:
        if len(corpus[page]) == 0:
            weighted_value += PageRanks[page]/len(corpus)
        else:
            weighted_value += PageRanks[page]/len(corpus[page])
    return weighted_value


if __name__ == "__main__":
    main()
