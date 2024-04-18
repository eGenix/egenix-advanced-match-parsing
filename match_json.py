#!/usr/bin/env python3

import numbers

### Examples

# JSON schema
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
        },
}

# Demo data
demo_data_1 = {
    "name" : "eggs",
    "price" : 2.99
}
demo_data_1a = {
    "name" : "eggs",
    "price" : 2
}
demo_data_2 = {
    "name" : "eggs"
}
demo_data_3 = {
    "name" : "eggs",
    "price" : 3.99,
    "color": "brown"
}
demo_data_4 = [1, 2, 3, 4]

demo_data_list = [
    demo_data_1,
    demo_data_1a,
    demo_data_2,
    demo_data_3,
    demo_data_4,
]

### Parsers

# Validation and parsing of a single instance
def parse_demo_data(instance):
    match instance:
        case dict() as data_item:
            match data_item:
                case {
                    'name': str() as name,
                    #'price': numbers.Real() as price,
                    #'price': int() | float() as price,
                    'price': int(price) | float(price),
                    **extra}:
                    # Note: numbers.Real(price) does not work, since ABCs
                    # are not supported for inline capturing parameters
                    if extra:
                        print (f'found extra values: {extra!r}')
                    # Process data
                    print (f'{name}: {price}')
                case wrong_values:
                    print (f'could not parse properties: {wrong_values!r}')
        case wrong_values:
            print (f'could not parse instance: {wrong_values!r}')
    # Note: The above could also be written as a single more involved
    # match statement.

# Validation and parsing of a list of instances
def parse_list_data(many_instances):
    match many_instances:
        case list() as data_list:
            for instance in data_list:
                parse_demo_data(instance)
        case wrong_data:
            print (f'unknown data format: {wrong_data!r}')

###

if __name__ == '__main__':
    import pprint
    parse_demo_data(demo_data_1)
    parse_demo_data(demo_data_1a)
    parse_demo_data(demo_data_2)
    parse_demo_data(demo_data_3)
    parse_demo_data(demo_data_4)
    print ()
    pprint.pprint(demo_data_list)
    parse_list_data(demo_data_list)
    parse_list_data(demo_data_1)
