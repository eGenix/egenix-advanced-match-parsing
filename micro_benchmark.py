#!/usr/bin/env python3
"""
    micro_benchmark - User friendly way to run micro benchmarks

    Use: Simply call script with -h as argument to see all available pyperf
    options.

    Example: See the Examples section below or the bench_match.py script for
    an example how to define micro- benchmarks.  Each such script will
    provide the same interface as this one when using the run() function.

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""
import inspect
import re
import textwrap
import pyperf

### Globals

# Output debug information ?
_debug = 0

# Default number of copies to put into the benchmark_code part of the bench mark
# function
DEFAULT_ITERATIONS = 20

# Code template used to build the benchmark functions
PERF_TEMPLATE = """\
def {fct_name}(iterations):
    loops = range(iterations)
    counter = pyperf.perf_counter
    t0 = counter()
{init_code}
    for _ in loops:
{benchmark_code}
    t1 = counter()
{verify_code}
    return t1 - t0
"""

### Examples

# Example bench mark function:
#
# The two sections "# Init" and "# Bench" are required (together with the
# comments.  The two sections are used to build the actual micro benchmark
# functions.
#
# The Init section defines the variables to be used for the Bench section.
# The bench section is run multiple times (depends on the functions
# .iterations attribute, which defaults to 10).
#
def bench_match_int():

    # Init
    obj = 1

    # Bench
    match obj:
        case float() as float_value:
            pass
        case int() as int_value:
            pass
        case _:
            pass

    # Verify
    assert int_value == 1

### Tools

def benchmark_code(fct, iterations=DEFAULT_ITERATIONS, fct_name=None):

    if fct_name is None:
        fct_name = fct.__name__
    if _debug:
        print (f'generating benchmark code for {fct}')
    (lines, start_lineno) = inspect.getsourcelines(fct)
    if _debug:
        print (f'inspect code lines: {lines}')

    # Remove decorators and def
    while lines[0].startswith('@'):
        del lines[0]
    assert lines[0].startswith('def')
    del lines[0]

    # Remove empty lines
    lines = [line
             for line in lines
             if line.strip()]

    code = ''.join(lines)
    lines = textwrap.dedent(code).splitlines(keepends=True)
    if _debug:
        print (f'code lines: {lines}')

    # Find init and bench
    init = []
    bench = []
    verify = []
    junk = []
    add_to = junk
    for line in lines:
        if line.startswith('# Init'):
            add_to = init
            continue
        elif line.startswith('# Bench'):
            add_to = bench
            continue
        elif line.startswith('# Verify'):
            add_to = verify
            continue
        add_to.append(line)
    assert len(junk) == 0, f'found extra code: {junk}'

    init_code = ''.join((
        f'    {line}' for line in init))
    benchmark_code = ''.join((
        f'        {line}' for line in bench * iterations))
    verify_code = ''.join((
        f'    {line}' for line in verify))

    # Build benchmark function
    code = PERF_TEMPLATE.format(
        fct_name=fct.__name__,
        init_code=init_code.rstrip(),
        benchmark_code=benchmark_code.rstrip(),
        verify_code=verify_code.rstrip(),
        )

    return fct_name, code

def benchmark_function(fct, iterations=DEFAULT_ITERATIONS, fct_name=None):

    # Generate code
    fct_name, code = benchmark_code(fct, iterations=iterations, fct_name=fct_name)

    # Note: pyperf uses worker processes which need to rerun the code
    # generation upon startup
    bench_fct = compile(code, '<generated>', 'exec')
    exec(bench_fct, globals(), globals())
    if _debug:
        print ('Built and defined global function:')
        print (code)
        print ()
    return globals()[fct_name]

def run_benchmark(runner, fct):

    if hasattr(fct, 'iterations'):
        iterations = fct.iterations
    else:
        iterations = DEFAULT_ITERATIONS
    if hasattr(fct, 'name'):
        benchmark_name = fct.name
    else:
        benchmark_name = fct.__name__
    bench_fct = benchmark_function(fct, iterations=iterations)
    if _debug:
        print (bench_fct)
    runner.bench_time_func(benchmark_name, bench_fct, inner_loops=iterations)
    return runner

def worker_add_cmdline_args(cmd, args):

    # Make sure our custom args are added to workers as well
    if args.mb_filter:
        cmd.extend(('--mb-filter', *args.mb_filter))
    if _debug:
        print (f'worker cmd: {cmd}')

def create_runner():

    # Create pyperf Runner instance
    runner = pyperf.Runner(
        add_cmdline_args=worker_add_cmdline_args,
    )

    # Add extra parameters for our own use
    runner.argparser.add_argument(
        '--mb-filter',
        help='filter micro benchmark function (regexp)',
        nargs='*',
        type=str)

    # Parse command line
    runner.parse_args()

    return runner

def run(namespace, prefix='bench_', filters=None):

    """ Run all benchmark functions found in namespace.

        prefix is the prefix name of benchmark functions to look for
        (defaults to 'bench_').

        filters may be given as list of regular expression to limit the
        number of functions to run.  The expressions are OR-joined. If
        the parameter is not given, the command line argument
        --mb-filter is used. If this is missing as well, no filtering
        takes place.

    """
    # Create runner (early, since this provides the CLI interface)
    runner = create_runner()

    # Check command line filters
    if filters is None:
        filters = runner.args.mb_filter
        if _debug:
            print (f'filters: {filters}')

    # Prepare filter
    if filters:
        re_filter = re.compile('|'.join(filters)).search
    else:
        re_filter = lambda x: True

    # Find all bench_* functions
    benchmarks = []
    for key, value in namespace.items():
        if key.startswith(prefix) and callable(value):
            if re_filter(key) is None:
                if _debug:
                    print (f'filtering out {key}')
                continue
            benchmarks.append(value)

    # Use runner to run all found benchmark functions
    for bench_fct in benchmarks:
        run_benchmark(runner, bench_fct)
    return runner

### Decorators

def configure(iterations=None, name=None):
    def wrapper(fct):
        if iterations is not None:
            fct.iterations = iterations
        if name is not None:
            fct.name = name
        return fct
    return wrapper

###

if __name__ == '__main__':
    runner = run(globals())
