from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api


from util.function_util import timed


def get_ways_in_relation(addr, selector):
    relations = overpass_query(addr, selector, 'relation')
    relations = [filter_ways_from_relation(x) for x in relations]
    return [way for relation in relations for way in relation]


def get_count(addr, selector, element_type='way'):
    areaId = _get_area_id(addr)
    overpass = get_overpass_api()
    query = overpassQueryBuilder(area=areaId, selector=selector, out='count', elementType=element_type)
    result = overpass.query(query)
    return result.countElements()

def _get_area_id(place):
    if place.isnumeric():
        return str(int(place) + 3600000000)

    nominatim = Nominatim()
    result = nominatim.query(place)
    areaId = result.areaId()
    if areaId is not None:
        return areaId
    else:
        json = result.toJSON()
        if json and 'osm_type' in json[0] and 'osm_id' in json[0]:
            return json[0]['osm_id'] + 2400000000
        return None

# @timed
# def get_centroid(addr, selector, element_type='way'):
#     areaId = _get_area_id(addr)
#     overpass = get_overpass_api()
#     query = overpassQueryBuilder(area=areaId, selector=selector, out='center', elementType=element_type)
#     overpass.deleteQueryFromCache(query)
#     result = overpass.query(query, timeout=120)
#     return result.countElements()


def overpass_query(addr, selector, element_type):
    areaId = _get_area_id(addr)
    overpass = get_overpass_api()
    query = overpassQueryBuilder(area=areaId, elementType=element_type, selector=selector)
    try:
        return overpass.query(query).toJSON()['elements']
    except Exception as e:
        print(Exception("Could not obtain Overpass data for " + addr + ", selector" + selector + ".\n" + str(e)))
        return []


def filter_ways_from_relation(relation):
    return [x for x in relation['members'] if x['type'] == 'way']


def get_city_center(place):
    overpass = get_overpass_api()
    areaId = _get_area_id(place)
    query_city = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="city"', includeGeometry=True)
    query_town = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="town"', includeGeometry=True)
    query_village = overpassQueryBuilder(area=areaId, elementType='node', selector='"place"="village"', includeGeometry=True)

    result_city = overpass.query(query_city)
    result_town = overpass.query(query_town)
    result_village = overpass.query(query_village)

    city_centers = result_city.elements()
    town_centers = result_town.elements()
    village_centers = result_village.elements()
    if len(city_centers + town_centers + village_centers) > 1:
        print(f'Found more than one city center for {place}')
    if not city_centers + town_centers + village_centers:
        raise Exception('No city center found for ' + place)
    return (city_centers + town_centers + village_centers)[0]


def get_city_tags(place):
    if place.isnumeric():
        tags = Api().query('relation/' + str(place)).tags()
        return tags
    nominatim = get_nominatim_api()
    result = nominatim.query(place)
    relation_id = result.toJSON()[0]['osm_id']
    relation_results = Api().query('relation/' + str(relation_id))
    return relation_results.tags()


def get_city_center_geometry(place):
    return get_city_center(place).geometry()


def get_city_population(place):
    center = get_city_center(place)
    tags = get_city_tags(place)
    population_from_admin_center = center and 'population' in center.tags() and int(center.tags()['population']) or None
    population_from_city_relation = 'population' in tags and int(tags['population']) or None
    return population_from_admin_center or population_from_city_relation


def get_city_center_coordinates(place):
    center = get_city_center(place)
    geometry = center.geometry()
    return geometry.coordinates[0], geometry.coordinates[1]


def get_overpass_api():
    return Overpass(endpoint='http://localhost:12346/api/')

def get_nominatim_api():
    return Nominatim()
