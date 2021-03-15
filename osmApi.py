from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

from util.function_util import timed


def get_ways_in_relation(addr, selector):
    relations = overpass_query(addr, selector, 'relation')
    relations = [filter_ways_from_relation(x) for x in relations]
    return [way for relation in relations for way in relation]


def get_count(addr, selector, element_type='way'):
    nominatim = Nominatim()
    areaId = nominatim.query(addr).areaId()
    overpass = Overpass(endpoint='https://overpass.kumi.systems/api/')
    query = overpassQueryBuilder(area=areaId, selector=selector, out='count', elementType=element_type)
    result = overpass.query(query)
    return result.countElements()

@timed
def get_centroid(addr, selector, element_type='way'):
    nominatim = Nominatim()
    areaId = nominatim.query(addr).areaId()
    overpass = Overpass(endpoint='https://overpass.kumi.systems/api/')
    query = overpassQueryBuilder(area=areaId, selector=selector, out='center', elementType=element_type)
    overpass.deleteQueryFromCache(query)
    result = overpass.query(query, timeout=120)
    return result.countElements()


def overpass_query(addr, selector, element_type):
    nominatim = Nominatim()
    areaId = nominatim.query(addr).areaId()
    overpass = Overpass(endpoint='https://overpass.kumi.systems/api/')
    query = overpassQueryBuilder(area=areaId, elementType=element_type, selector=selector)
    try:
        return overpass.query(query).toJSON()['elements']
    except Exception as e:
        print(Exception("Could not obtain Overpass data for " + addr + ", selector" + selector + ".\n" + str(e)))
        return []


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
# get_centroid("Bochum, Germany", '"building"')
# print()
