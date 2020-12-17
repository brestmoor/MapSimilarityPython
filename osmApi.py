from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass


def get_ways_in_relation(addr, selector):
    nominatim = Nominatim()
    areaId = nominatim.query(addr).areaId()
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=selector)
    result = overpass.query(query)
    relations = [filter_ways_from_relation(x) for x in result.toJSON()['elements']]
    return [way for relation in relations for way in relation]


def filter_ways_from_relation(relation):
    return [x for x in relation['members'] if x['type'] == 'way']


def get_city_center(place):
    nominatim = Nominatim()
    overpass = Overpass()
    areaId = nominatim.query(place).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="city"', includeGeometry=True)
    result = overpass.query(query)

    city_centers = result.elements()
    if len(city_centers) > 1:
        print(f'Found more than one city center for {query}')

    geometry = city_centers[0].geometry()
    return geometry.coordinates[1], geometry.coordinates[0]

# print(get_city_center('Kielce, Poland'))