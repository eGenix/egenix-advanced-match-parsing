#!/usr/bin/env oython3

""" Parse XML using the new match statement

"""

from xml.etree.ElementTree import XML, Element, tostring

### Demo data

# From https://docs.python.org/3/library/xml.etree.elementtree.html
COUNTRY_DATA = """\
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

### Helpers

def error_string(elem, objtype='element'):
    return f'could not parse {objtype}: {tostring(elem, encoding="unicode")!r}'

### Functions

def tokenize_xml(data):
    tree = XML(data)
    return tree

def debug_parse_countries(tree):
    countries = {}
    for child in tree:
        match child:
            case Element(tag='country', attrib={'name': name}) as country:
                print (f'found country {name}')
                for child in country:
                    neighbors = {}
                    print (f'processing child element {child!r}')
                    match child:
                        case Element(
                            tag='rank', text=rank):
                            rank = int(rank)
                            print (f'rank: {rank}')
                        case Element(
                            tag='year', text=year):
                            year = int(year)
                            print (f'year ranked: {year}')
                        case Element(
                            tag='gdppc', text=gdppc):
                            gdppc = float(gdppc)
                            print (f'GDP per capita: {gdppc}')
                        case Element(
                            tag='neighbor',
                            attrib={'name': nb_name, 'direction': nb_direction}):
                            neighbors[nb_name] = nb_direction
                            print (f'found neighbor {nb_name} in direction {nb_direction}')
                        case wrong_data:
                            raise TypeError(error_string(wrong_data, 'child'))
                countries[name] = dict(
                    rank=rank,
                    year=year,
                    gdppc=gdppc,
                    neighbors=neighbors,
                )
            case wrong_data:
                raise TypeError(error_string(wrong_data, 'child'))
    return countries

def parse_countries_1(tree):
    countries = {}
    for child in tree:
        match child:
            case Element(tag='country',
                         attrib={'name': name}) as country:
                for child in country:
                    neighbors = {}
                    # WARNING: This does not detect missing child elements
                    match child:
                        case Element(tag='rank', text=rank):
                            rank = int(rank)
                        case Element(tag='year', text=year):
                            year = int(year)
                        case Element(tag='gdppc', text=gdppc):
                            gdppc = float(gdppc)
                        case Element(
                            tag='neighbor',
                            attrib={'name': nb_name,
                                    'direction': nb_direction}):
                            neighbors[nb_name] = nb_direction
                        case wrong_data:
                            raise TypeError(
                                error_string(wrong_data,
                                'country element'))
                countries[name] = dict(
                    rank=rank,
                    year=year,
                    gdppc=gdppc,
                    neighbors=neighbors,
                )
            case wrong_data:
                raise TypeError(error_string(wrong_data,
                                             'country'))
    return countries

def parse_countries_2(tree):
    countries = {}
    for child in tree:
        match child:
            case Element(tag='country',
                         attrib={'name': name}) as country:
                match list(country):
                    case [
                        Element(tag='rank', text=rank),
                        Element(tag='year', text=year),
                        Element(tag='gdppc', text=gdppc),
                        *extra,
                        ]:
                        # Convert types
                        rank = int(rank)
                        year = int(year)
                        gdppc = float(gdppc)
                        # Parse neighbors
                        neighbors = {}
                        for child in extra:
                            match child:
                                case Element(
                                    tag='neighbor',
                                    attrib={
                                        'name': nb_name,
                                        'direction': nb_direction}):
                                    neighbors[nb_name] = nb_direction
                                case wrong_data:
                                    raise TypeError(
                                        error_string(
                                            wrong_data,
                                            'neighbor'))
                    case wrong_data:
                        raise TypeError(error_string(
                                country,
                                'country elements'))
                countries[name] = dict(
                    rank=rank,
                    year=year,
                    gdppc=gdppc,
                    neighbors=neighbors,
                )
            case wrong_data:
                raise TypeError(error_string(wrong_data,
                                             'country'))
    return countries

###

if __name__ == '__main__':
    import pprint
    tree = tokenize_xml(COUNTRY_DATA)
    countries = parse_countries_2(tree)
    pprint.pprint(countries)

