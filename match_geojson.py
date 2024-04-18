#!/usr/bin/env python3

# From https://geojson.org/
GEOJSON_TYPES = (
    'Feature',
    'FeatureCollection',
    'Point',
    # more
)

geojson_data_1 = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
    },
    "properties": {
        "name": "Dinagat Islands"
    }
}

def parse_geojson_data(instance):
    match instance:
        case {'type': obj_type, **other_members} as obj:
            print (f'new object of type {obj_type!r}')
            if obj_type not in GEOJSON_TYPES:
                print (f'this type is not a valid GeoJSON type')
                return None
            for obj_member in other_members.items():
                match obj_member:
                    case ('geometry', geometry):
                        print (f'found geometry {geometry!r}')
                    case ('properties', properties):
                        print (f'found properties {properties!r}')
                    case wrong_member:
                        print (f'could not parse member: {wrong_member!r}')
        case wrong_values:
            print (f'could not parse object: {wrong_values!r}')

###

if __name__ == '__main__':
    parse_geojson_data(geojson_data_1)
    print ()
