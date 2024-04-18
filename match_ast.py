#!/usr/bin/env python3

import inspect
import ast
from ast import *

### Globals

_debug = 0

### Examples

def example(x):

    if isinstance(x, int) and x > 12:
        print ('Int > 12: {x}')
    elif isinstance(x, float):
        print ('Float: {x}')
    elif isinstance(x, str) and len(x) > 5:
        print ('String with more than 5 chars: {x}')
    else:
        print ('Unknown type: {x}')

def example_refactored(x):

    match x:
        case int() if x > 12:
            print ('Int > 12: {x}')
        case float():
            print ('Float: {x}')
        case str() if len(x) > 5:
            print ('String with more than 5 chars: {x}')
        case _:
            print ('Unknown type: {x}')

### Tools

def if_refactor(if_node, varname, cases, orelse):

    print (f'Found if which can be refactored')

    # Build match_cases
    case_nodes = [
        match_case(
            pattern=MatchClass(
            cls=Name(id=typename),
            patterns=[],
            kwd_attrs=[],
            kwd_patterns=[]),
            guard=condition,
            body=body)
        for (varname, typename, condition, body) in cases
    ]
    case_nodes.append(
        match_case(
              pattern=MatchAs(),
              body=orelse)
    )

    # Build Match node
    match_node = Match(
        subject=Name(id=varname),
        cases=case_nodes,
    )
    return match_node

def scan_if(node, varname, test, body, orelse, cases=None):

    # Trick for non-capturing vars
    class params:
        pass
    params.varname = varname

    # Check whether this is a possible match refactoring if-candidate
    match test:
        case Call(func=Name(id='isinstance'),
                  args=[Name(id=params.varname),
                        Name(id=typename)]):
            # isinstance(varname, typename)
            new_case = (varname, typename, None, body)

        case BoolOp(op=And(),
                    values=[
                        Call(func=Name(id='isinstance'),
                             args=[Name(id=params.varname),
                                   Name(id=typename)]),
                        condition
                    ]):
            # isinstance(varname, typename) and condition
            new_case = (varname, typename, condition, body)

        case _:
            # Unsupported if-variant
            return cases, node

    # Add new case
    if cases is None:
        cases = []
    cases.append(new_case)

    # Recursively check whether there are more if-elif cases
    match orelse:
        case [If(elif_test, elif_body, elif_orelse) as elif_node]:
            cases, orelse = scan_if(
                elif_node, varname,
                elif_test, elif_body, elif_orelse,
                cases)
        case _:
            pass

    return cases, orelse

def function_refactor(fct_node, name, varname):

    print (f'Found function {name} with variable {varname}')

    # Find if-elif-else
    new_body = []
    for node in fct_node.body:
        match node:
            case If(test, body, orelse):
                # Scan for match cases written as if-elif chain
                cases, orelse = scan_if(node, varname,
                                        test, body, orelse)
                if cases:
                    # Refactor to use match instead
                    node = if_refactor(node, varname,
                                       cases, orelse)
            case _:
                # Not an if node
                break
        new_body.append(node)
    fct_node.body = new_body

def if_match_refactor(fct):
    source = inspect.getsource(fct)
    tree = ast.parse(source) # AST.Module

    # Find functions
    for node in tree.body:
        match node:
            case FunctionDef(
                name,
                args=arguments(args=[arg(arg=varname)])):
                # Refactor function name with variable varname
                function_refactor(node, name, varname)
            case _:
                # skip
                pass

    return tree

### Helpers

def print_ast(fct):
    source = inspect.getsource(fct)
    tree = ast.parse(source)
    print (f'AST of function {fct.__name__}:')
    print (ast.dump(tree, indent=2))
    print ()

def print_function(fct):
    source = inspect.getsource(fct)
    print (f'Function {fct.__name__}:')
    print (source)
    print ()

###

if __name__ == '__main__':
    print ('Before refactoring:')
    print_function(example)
    if _debug:
        print_ast(example)
        print_ast(example_refactored)
    print ()

    # Refactor
    tree = if_match_refactor(example)
    new_function = ast.unparse(tree)
    print ()

    print ('Refactored function:')
    print (new_function)

