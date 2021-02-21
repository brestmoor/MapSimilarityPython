from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass


def get_ways_in_relation(addr, selector):
    nominatim = Nominatim()
    areaId = nominatim.query(addr).areaId()
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=selector)
    try:
        result = overpass.query(query)
    except Exception as e:
        print(Exception("Could not obtain Overpass data for " + addr + ", selector" + selector + ".\n" + str(e)))
        return []
    relations = [filter_ways_from_relation(x) for x in result.toJSON()['elements']]
    return [way for relation in relations for way in relation]


def filter_ways_from_relation(relation):
    return [x for x in relation['members'] if x['type'] == 'way']


def get_city_center(place):
    nominatim = Nominatim()
    overpass = Overpass()
    areaId = nominatim.query(place).areaId()
    query_city = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="city"', includeGeometry=True)
    query_town = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="town"', includeGeometry=True)
    result_city = overpass.query(query_city)
    result_town = overpass.query(query_town)
    city_centers = result_city.elements()
    town_centers = result_town.elements()
    if len(city_centers + town_centers) > 1:
        print(f'Found more than one city center for {place}')
    if len(city_centers + town_centers) == 0:
        raise Exception(f'Found no city centers for {place}')
    return (city_centers + town_centers)[0]


def get_city_center_geometry(place):
    return get_city_center(place).geometry()

def get_city_center_coordinates(place):
    center = get_city_center(place)
    geometry = center.geometry()
    return geometry.coordinates[0], geometry.coordinates[1]

# print(get_city_center('Kielce, Poland'))