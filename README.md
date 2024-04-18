
# Resources for the eGenix Talk "Advanced parsing of structured data using Python's new match statement"

## Abstract of the talk

The `match` statement was introduced in Python 3.10, but has not yet seen wide adoption.

In this talk, I'd like to showcase a few more advanced use cases to demonstrate it's expressiveness and versatility, compared to classic parsers using if-elif-else chains, in the hope of attracting a few more Python users to the new concept in Python.

We will have a look at parsing JSON, XML and ASTs, and also compare performance to the classic parsing strategy.

Knowledge of how the `match` statement works and familiarity with at least one of JSON, XML and ASTs are prerequisite for this talk.

## Resources

The various `match_*.py` files have the examples used in the talk and include some extra informmation and code as well, which did not fit the talk.

The `bench_match.py` file defines define micro benchmarks used in the talk. This is based on the `micro_benchmark.py` module, which will soon be released as separate package on PyPI.

## Slides

PDF slides are available in the `slides/` directory.

- PyDDF-Talk-Advanced-Parsing-with-Match-Statement-2024-04-17.pdf points to the version which was presented at the Python Meeting Düsseldorf on 2024-04-17
  - This has a few minor errors found during the talk which will be fixed in an updated version of the talk.

## Conference and Events

This talk was or will be held at the following events:
- [Python Meeting Düsseldorf](https://pyddf.de/) on 2024-04-17
- [PyCon Italia 2024](https://2024.pycon.it/en/event/advanced-parsing-of-structured-data-using-pythons-new-match-statement) in 2024-05-25

For inquiries related to the talk, please write to info@egenix.com
