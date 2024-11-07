
# Resources for the eGenix Talk "Advanced parsing of structured data using Python's new match statement"

## Abstract of the talk

The `match` statement was introduced in Python 3.10, but has not yet seen wide adoption.

In this talk, I'd like to showcase a few more advanced use cases to demonstrate it's expressiveness and versatility, compared to classic parsers using if-elif-else chains, in the hope of attracting a few more Python users to the new concept in Python.

We will have a look at parsing JSON, XML and ASTs, and also compare performance to the classic parsing strategy.

Knowledge of how the `match` statement works and familiarity with at least one of JSON, XML and ASTs are prerequisite for this talk.

## Resources

The various `match_*.py` files have the examples used in the talk and include some extra informmation and code as well, which did not fit the talk.

The `bench_match.py` file defines define micro benchmarks used in the talk. This is based on the `micro_benchmark.py` module, which will soon be released as separate package on PyPI. Development for this is taking place in the [GitHub - eGenix/egenix-micro-benchmark: Micro benchmark tooling for Python](https://github.com/eGenix/egenix-micro-benchmark) repo, in case you are interested.

Here's a quick example to showcase how easy it is to write micro benchmarks using this new package:

```python
import micro_benchmark

def bench_match_int():
    # Init
    obj = 1
    # Bench
    match obj:
        case float():
            type = 'float'
        case int():
            type = 'int'
        case _:
            pass
    # Verify
    assert type == 'int'

if __name__ == '__main__':
    micro_benchmark.run(globals())
```

Then run this using Python and see immediate results:

```bash
> python3 bench_example.py
.....................
bench_match_int: Mean +- std dev: 107 ns +- 5 ns
```

The micro benchmark package uses the [pyperf package](https://pypi.org/project/pyperf/) to run the benchmarks, so you get all options and features available with perf (plus a few more), to work with these results.

## Slides

PDF slides of the talk are available for download:

- [PyDDF-Talk-Advanced-Parsing-with-Match-Statement-2024-04-17.pdf](https://downloads.egenix.com/python/PyDDF-Talk-Advanced-Parsing-with-Match-Statement.pdf) PDF version which was presented at the Python Meeting Düsseldorf on 2024-04-17.
  - This has a few minor errors corrected which were found during the talk.

- [PyCon-Italia-2024-Talk-Advanced-Parsing-with-Match-Statement.pdf](https://downloads.egenix.com/python/PyCon-Italia-2024-Talk-Advanced-Parsing-with-Match-Statement.pdf) PDF version of the talk which was presented at PyCon Italia 2024 on 2024-05-25.

- [PyCon-Sweden-2024-Talk-Advanced-Parsing-with-Match-Statement.pdf](https://downloads.egenix.com/python/PyCon-Sweden-2024-Talk-Advanced-Parsing-with-Match-Statement.pdf) PDF version of the (current draft) version of the talk which will be presented at PyCon Sweden 2024 on 2024-11-15.

These are released under the same license as the other files in this directory.

## Conference and Events

This talk was or will be held at the following events:
- [Python Meeting Düsseldorf](https://pyddf.de/) on 2024-04-17
- [PyCon Italia 2024](https://2024.pycon.it/en/event/advanced-parsing-of-structured-data-using-pythons-new-match-statement) on 2024-05-25
- [PyCon Sweden 2024](https://www.pycon.se/)

## Contact

For inquiries related to the talk, please write to info@egenix.com or contact Marc-André Lemburg at mal@egenix.com.
