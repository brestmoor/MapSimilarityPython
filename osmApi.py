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