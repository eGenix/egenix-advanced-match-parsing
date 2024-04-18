#!/usr/bin/env python3

def test_match_obj(obj):
    match obj:
        case list() as list_obj:
            print (f'found list: {list_obj!r}')
        case dict() as dict_obj:
            print (f'found dict: {dict_obj!r}')
        case [a, b, c]:
            print (f'found 3 element sequence: {obj!r}')
        case {'name': name, 'value': value}:
            print (f'found name-value mapping: {obj!r}')
        case unknown:
            print (f'could not parse object: {unknown!r}')

# SyntaxError:
#def test_match_obj1(d):
#    match d:
#        case wrong_values:
#            print (f'could not parse object: {wrong_values!r}')
#        case list():
#            print (f'found list')
#        case dict():
#            print (f'found dict')

def test_match_obj1(obj):
    match obj:
        case _ if obj > 0:
            print (f'found value greater than 0: {obj!r}')
        case list():
            print (f'found list')
        case dict():
            print (f'found dict')

def test_match_obj1a(obj):
    match obj:
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')


def test_match_obj2(obj):
    match obj:
        case list():
            print (f'found list')
        case { 'properties': dict }:
            print (f'found dict with properties {dict!r}')
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')

def test_match_obj3(obj):
    match obj:
        case (a, b):
            print (f'found a tuple')
        case [a, b]:
            print (f'found a list')
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')

def test_match_obj3a(obj):
    match obj:
        case tuple((a, b)):
            print (f'found a tuple: {(a, b)!r}')
        case list((a, b)):
            print (f'found a list: {[a, b]!r}')
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')
    print (f'found data: {(a, b)!r}')

def test_match_obj3b(obj):
    match obj:
        case [1, _, _, 4]:
            print (f'found a 4 item list with 1 and 4 at the ends: {obj}')
        case [1, 2, *more]:
            print (f'found a list with 1 and 2 at the start: {obj}')
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')

###

if __name__ == '__main__':
    d = {'a': 1, 'properties': [2, 3, 4]}
    test_match_obj(d)
    test_match_obj1a(d)
    test_match_obj2(d)
    t = (1, 2)
    l = [2, 3]
    test_match_obj3(t)
    test_match_obj3(l)
    test_match_obj3a(t)
    test_match_obj3a(l)
    test_match_obj3b([1, 2, 3, 4])
    test_match_obj3b([1, 0, 0, 4])
    test_match_obj3b([1, 2, 3])
    test_match_obj3b([1, 2])
