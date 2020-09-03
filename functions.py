import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon
from timeit import default_timer as timer
from osmApi import get_ways_in_relation

ox.config(log_console=True, use_cache=True)

def timeit(func):
    start = timer()
    ret = func()
    end = timer()
    print("took: " + str(end - start))
    return ret


def min_dist_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return distances.min()


def one_way_percentage():
    place = 'Krakow, Poland'
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)
    gu = ox.get_undirected(g)
    mapDf = ox.project_gdf(ox.graph_to_gdfs(gu, nodes=False))
    return mapDf.loc[mapDf['oneway'] == True].osmid.count() / mapDf.osmid.count()


def primary_percentage():
    place = 'Krakow, Poland'
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)
    gu = ox.get_undirected(g)
    mapDf = ox.project_gdf(ox.graph_to_gdfs(gu, nodes=False))
    return mapDf.loc[mapDf['highway'] == 'primary'].osmid.count() / mapDf.osmid.count()


def average_dist_to_park():
    parksDf = ox.pois_from_place('Krakow, Poland', {'leisure': 'park'})

    buildingsDf = ox.pois_from_place('Krakow, Poland', {'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential', 'terrace']})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    parks_proj = ox.project_gdf(parks_polygons)

    buildings_proj['distance'] = buildings_proj[::5, :].apply(lambda row: min_dist_df(row.geometry.centroid, parks_proj), axis=1)
    return buildings_proj['distance'].mean()



def average_dist_to_bus_stop():
    bus_df = ox.pois_from_place('Krakow, Poland', {'highway': 'bus_stop'})

    buildingsDf = ox.pois_from_place('Krakow, Poland', {'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential', 'terrace']})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    bus_proj = ox.project_gdf(bus_df)

    buildings_proj['distance'] = buildings_proj.iloc[::10, :].apply(lambda row: min_dist_df(row.geometry.centroid, bus_proj), axis=1)

    print(buildings_proj['distance'].mean())


def natural_terrain_coverage():
    parksDf = ox.pois_from_place('Krakow, Poland', {'leisure': ['park', 'garden'], 'natural': ['wood', 'scrub', 'heath', 'grassland'], 'landuse': ['grass', 'forest']})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    parks_proj = ox.project_gdf(parks_polygons)

    krakow_boundary = ox.project_gdf(ox.geocode_to_gdf('Krakow, Poland'))

    parks_filtered = parks_proj[parks_proj['leisure'].isin(['park', 'garden']) | parks_proj['natural'].isin(['wood', 'scrub', 'heath', 'grassland']) |  parks_proj['landuse'].isin(['grass', 'forest'])]

    return parks_filtered.area.sum() / krakow_boundary.area


def numer_of_parks_total():
    parksDf = ox.pois_from_place('Krakow, Poland', {'leisure': 'park'})
    parks_filtered = parksDf[parksDf['leisure'] == 'park']

    return len([isinstance(x, Polygon) for x in parks_filtered.geometry])


def cycleways_to_highways():
    poi_cycleways = ox.pois_from_place('Krakow, Poland', {'highway': 'cycleway'})
    poi_highways = ox.pois_from_place('Krakow, Poland', {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    cycleways_proj = ox.project_gdf(poi_cycleways)
    highways_proj = ox.project_gdf(poi_highways)

    return cycleways_proj.length.sum() / highways_proj.length.sum() # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS


def bus_routes_to_highways():
    bus_routes_ways = get_ways_in_relation("Krakow, Poland", '"route"="bus"')
    ids_of_bus_ways = [x['ref'] for x in bus_routes_ways]
    poi_highways = ox.pois_from_place('Krakow, Poland', {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    highways_proj = ox.project_gdf(poi_highways)

    return highways_proj[highways_proj.osmid.isin(ids_of_bus_ways)].length.sum() / highways_proj.length.sum() #pokrycje sie zwiekszylo z 28 do 38 %


def tram_routes_to_highways():
    poi_tram_routes = ox.pois_from_place('Krakow, Poland', {'railway': 'tram'})
    poi_highways = ox.pois_from_place('Krakow, Poland', {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    tram_routes_proj = ox.project_gdf(poi_tram_routes)
    highways_proj = ox.project_gdf(poi_highways)

    return tram_routes_proj.length.sum() / highways_proj.length.sum() # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS


def avg_dist_between_crossroads():
    place = 'Krakow, Poland'
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.graph_from_point((50.102526, 19.927396), network_type='drive', custom_filter=cf, dist=1000)
    g_proj = ox.project_graph(g)
    consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

    outdeg = consolidated.out_degree()
    to_keep = [n for (n, deg) in outdeg if deg > 1]

    consolidated_subgraph = consolidated.subgraph(to_keep)
    # ox.plot_graph(consolidated_subgraph)
    print('')



print(timeit(avg_dist_between_crossroads))
