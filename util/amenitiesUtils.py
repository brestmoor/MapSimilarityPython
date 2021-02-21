import osmnx as ox
from shapely.geometry import Polygon


def get_buildings(place):
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    return buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]