import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon


def distance(G, first_node, second_node):
    return ox.distance.great_circle_vec(G.nodes[first_node]['y'], G.nodes[first_node]['x'],
                                 G.nodes[second_node]['y'], G.nodes[second_node]['x'])


def min_dist(first_series, second_series_list):
    return min(second_series_list, key=lambda x: x.geometry.centroid.distance(first_series.geometry.centroid))


def min_dist_row_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return df.loc[distances.idxmin()]


def min_dist_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return distances.min()


# place = 'Krakow, Poland'
# cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
# g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)
# gu = ox.get_undirected(g)
# mapDf = ox.project_gdf(ox.graph_to_gdfs(gu, nodes=False))

parksDf = ox.pois_from_place('Krakow, Poland', {'leisure': ['park', 'garden'], 'natural': ['wood', 'scrub', 'heath', 'grassland'], 'landuse': ['grass', 'forest']})
buildingsDf = ox.pois_from_place('Krakow, Poland', {'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential', 'terrace']})

parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

parks_proj = ox.project_gdf(parks_polygons)
buildings_proj = ox.project_gdf(buildings_polygons)

parks_proj.area.sum() / ox.project_gdf(ox.geocode_to_gdf('Krakow, Poland')).area

ox.project_gdf(ox.geocode_to_gdf('Krakow, Poland')).area

buildings_proj['distance'] = buildings_proj.apply(lambda row: min_dist_df(row.geometry.centroid, parks_proj), axis=1)

