#!/usr/bin/env python3
"""
    Micro benchmark for match vs. if-elif-else

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""
import micro_benchmark

###

# Match on second attempt

def bench_match_int():

    # Init
    obj = 1

    # Bench
    match obj:
        case float():
            pass
        case int():
            pass
        case _:
            pass

def bench_if_int():

    # Init
    obj = 1

    # Bench
    if isinstance(obj, float):
        pass
    elif isinstance(obj, int):
        pass
    else:
        pass

# Match on first attempt

def bench_match_int_2():

    # Init
    obj = 1

    # Bench
    match obj:
        case int():
            pass
        case float():
            pass
        case _:
            pass

def bench_if_int_2():

    # Init
    obj = 1

    # Bench
    if isinstance(obj, int):
        pass
    elif isinstance(obj, float):
        pass
    else:
        pass

###

# using generic syntax

def bench_match_int_capvars():

    # Init
    obj = 1

    # Bench
    match obj:
        case float() as value:
            pass
        case int() as value:
            pass
        case _:
            pass

# using inlined syntax

def bench_match_int_inlined_capvars():

    # Init
    obj = 1

    # Bench
    match obj:
        case float(value):
            pass
        case int(value):
            pass
        case _:
            pass

def bench_if_int_capvars():

    # Init
    obj = 1

    # Bench
    if isinstance(obj, float):
        value = obj
    elif isinstance(obj, int):
        value = obj
    else:
        pass

###

# First benchmark where match is actually faster than if

def bench_match_list_int_capvars():

    # Init
    obj = [1, 2, 3]

    # Bench
    match obj:
        case int():
            a = obj
            b = 2
            c = 3
        case [a, b, c]:
            pass
        case _:
            pass

def bench_if_list_int_capvars():

    # Init
    obj = [1, 2, 3]

    # Bench
    if isinstance(obj, int):
        a = obj
        b = 2
        c = 3
    elif isinstance(obj, list) and len(obj) == 3:
        a, b, c = obj
    else:
        pass

###

def bench_match_str():

    # Init
    obj = 'abcdef'

    # Bench
    match obj:
        case float():
            pass
        case str():
            pass
        case _:
            pass

def bench_if_str():

    # Init
    obj = 'abcdef'

    # Bench
    if isinstance(obj, float):
        pass
    elif isinstance(obj, str):
        pass
    else:
        pass

###

def bench_match_str_capvars():

    # Init
    obj = 'abcdef'

    # Bench
    match obj:
        case float() as value:
            pass
        case str() as value:
            pass
        case _:
            pass

def bench_if_str_capvars():

    # Init
    obj = 'abcdef'

    # Bench
    if isinstance(obj, float):
        value = obj
    elif isinstance(obj, str):
        value = obj
    else:
        pass

###

def bench_match_int_guards():

    # Init
    obj = 12

    # Bench
    match obj:
        case int() as value if value > 20:
            pass
        case int() as value if value > 10:
            pass
        case _:
            pass

def bench_if_int_guards():

    # Init
    obj = 12

    # Bench
    if isinstance(obj, int) and obj > 20:
        value = obj
    elif isinstance(obj, int) and obj > 20:
        value = obj
    else:
        pass

###

@micro_benchmark.configure(iterations=10)
def bench_match_complex():

    # Init
    obj = [1, 2, {'abc': 3}, (4, 5, 6)]

    # Bench
    match obj:
        case int() as value if value > 20:
            pass
        case [int() as a, int() as b,
              {'abc': int() as c},
              (int() as d, int() as e, int() as f)]:
            pass
        case _:
            pass

    # Verify
    assert obj == [a, b, {'abc': c}, (d, e, f)]

@micro_benchmark.configure(iterations=10)
def bench_match_complex_inlined_capvars():

    # Init
    obj = [1, 2, {'abc': 3}, (4, 5, 6)]

    # Bench
    match obj:
        case int(value) if value > 20:
            pass
        case [int(a), int(b),
              {'abc': int(c)},
              (int(d), int(e), int(f))]:
            pass
        case _:
            pass

    # Verify
    assert obj == [a, b, {'abc': c}, (d, e, f)]

@micro_benchmark.configure(iterations=10)
def bench_if_complex():

    # Init
    obj = [1, 2, {'abc': 3}, (4, 5, 6)]

    # Bench
    if isinstance(obj, int) and obj > 20:
        value = obj
    elif (isinstance(obj[0], int) and
          isinstance(obj[1], int) and
          isinstance(obj[2], dict) and
          ('abc' in obj[2]) and
          isinstance(obj[2]['abc'], int) and
          isinstance(obj[3], tuple) and
          isinstance(obj[3][0], int) and
          isinstance(obj[3][1], int) and
          isinstance(obj[3][2], int)):
        [a, b, q1, (d, e, f)] = obj
        c = q1['abc']
    else:
        pass

    # Verify
    assert obj == [a, b, {'abc': c}, (d, e, f)]

###

def bench_match_float_or_int():

    # Init
    obj = 1

    # Bench
    match obj:
        case float() | int():
            pass
        case _:
            pass

def bench_if_float_or_int():

    # Init
    obj = 1

    # Bench
    if isinstance(obj, (float, int)):
        pass
    else:
        pass

###

if __name__ == '__main__':
    runner = micro_benchmark.run(globals())
