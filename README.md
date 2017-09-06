# Dive arXiv


Allow you to find trends on topics, based on publications stored on arxiv

Look at:

- Author with the more publication
- Trend over time of the field
- Related words
- ...



See [arXiv API](https://arxiv.org/help/api/user-manual) for improving the code.


# TODO

- Clean the code
- Find a better abstraction for function
- change "iter" over all to "iter" over range
- transfert `ArXiv.ipynb` to `ArXiv_lib.ipynb`
- optimize the code
- do freq calculation of words (for TFIDF) on two separate steps (return first tupple (count_i, count_max))
- algo dataviz for words


# Questions

## author oriented

- How do an author publish along is lifetime
- What are his subject of interest
- Who are his friends / cowriter
- study the whole network (or limit the number of hop)
- dataviz network

## data oriented