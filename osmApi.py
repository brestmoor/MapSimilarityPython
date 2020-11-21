from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api


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


def get_city_center(query):
    nominatim = Nominatim()
    query = nominatim.query(query)
    osm_id = query.areaId() - 3600000000

    relation = Api().query(f'relation/{osm_id}')
    city_center = [member for member in relation.members() if member.type() == 'node']
    if len(city_center) > 1:
        print(f'Found more than one city center for {query}')

    geometry = city_center[0].geometry()
    return geometry.coordinates[1], geometry.coordinates[0]

# print(get_city_center('Vienna, Austria'))