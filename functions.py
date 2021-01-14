from timeit import default_timer as timer

import numpy as np
import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

from util.function_util import memoize, timed
from osmApi import get_ways_in_relation
from util.spatial_util import distance_to_nearest, within

ox.config(log_console=False, use_cache=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)


@memoize
def basic_stats(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    G = ox.graph_from_place(place, network_type='drive', custom_filter=cf)

    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    graph_area_m = nodes_proj.unary_union.convex_hull.area

    return ox.basic_stats(G_proj, area=graph_area_m, clean_intersects=True, circuity_dist='euclidean')


@timed
def average_street_length(place):
    return basic_stats(place)['street_length_avg']


@timed
def intersection_density_km(place):
    return basic_stats(place)['intersection_density_km']


@timed
def street_density_km(place):
    return basic_stats(place)['street_density_km']


@timed
def circuity_avg(place):
    return basic_stats(place)['circuity_avg']


@timed
def one_way_percentage(place):
    highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    try:
        oneway_count = highways.loc[highways['oneway'] == 'yes'].osmid.count() / highways.osmid.count()
        return oneway_count
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))


@timed
def primary_percentage(place):
    highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    try:
        primary_count = highways.loc[highways['highway'] == 'primary'].osmid.count() / highways.osmid.count()
        return primary_count
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))


@timed
def average_dist_to_park(place):
    parksDf = ox.geometries_from_place(place, {'leisure': 'park'})

    if parksDf.empty:
        return 10000

    buildingsDf = ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace']})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    parks_proj = ox.project_gdf(parks_polygons)

    distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(parks_proj, row.geometry), axis=1)
    return distances.mean()


@timed
def average_dist_to_bus_stop(place):
    bus_df = ox.geometries_from_place(place, {'highway': 'bus_stop'})
    if bus_df.empty:
        return 1000000

    buildingsDf = ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace']})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    bus_proj = ox.project_gdf(bus_df)
    distances = buildings_proj.iloc[::10].apply(lambda row: distance_to_nearest(bus_proj, row.geometry), axis=1)
    return distances.mean()


@timed
def buildings_density(place):
    buildingsDf = ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]
    if 'element_type' in buildings_polygons.columns:
        buildings_polygons = buildings_polygons[buildings_polygons.element_type == 'way']

    try:
        buildings_proj = ox.project_gdf(buildings_polygons)
    except AttributeError as ae:
        print(str(ae) + "for " + place)
        return 0

    krakow_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

    return buildings_proj.area.sum() / krakow_boundary.area[0]


@timed
def natural_terrain_density(place):
    parksDf = ox.geometries_from_place(place, {'leisure': ['park', 'garden'],
                                               'natural': ['wood', 'scrub', 'heath', 'grassland'],
                                               'landuse': ['grass', 'forest']})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    if 'element_type' in parks_polygons.columns:
        parks_polygons = parks_polygons[parks_polygons.element_type == 'way']

    if parks_polygons.empty:
        return 0

    parks_proj = ox.project_gdf(parks_polygons)

    krakow_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

    if 'leisure' not in parks_proj:
        parks_proj['leisure'] = ''

    if 'natural' not in parks_proj:
        parks_proj['natural'] = ''

    if 'landuse' not in parks_proj:
        parks_proj['landuse'] = ''

    parks_filtered = parks_proj[parks_proj['leisure'].isin(['park', 'garden']) | parks_proj['natural'].isin(
        ['wood', 'scrub', 'heath', 'grassland']) | parks_proj['landuse'].isin(['grass', 'forest'])]

    return parks_filtered.area.sum() / krakow_boundary.area[0]



# def numer_of_parks_total(place):
#     parksDf = ox.geometries_from_place(place, {'leisure': 'park'})
#     parks_filtered = parksDf[parksDf['leisure'] == 'park']
#
#     return len([isinstance(x, Polygon) for x in parks_filtered.geometry])

@timed
def cycleways_to_highways(place):
    poi_cycleways = ox.geometries_from_place(place, {'highway': 'cycleway',
                                                     'cycleway': ['lane', 'opposite_lane', 'opposite', 'shared_lane'],
                                                     'bicycle': 'designated'})
    poi_highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    if poi_cycleways.empty:
        return 0

    cycleways_proj = ox.project_gdf(poi_cycleways)
    highways_proj = ox.project_gdf(poi_highways)

    return cycleways_proj.length.sum() / highways_proj.length.sum()  # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS


@timed
def bus_routes_to_highways(place):
    bus_routes_ways = get_ways_in_relation(place, '"route"="bus"')
    ids_of_bus_ways = [x['ref'] for x in bus_routes_ways]
    poi_highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    highways_proj = ox.project_gdf(poi_highways)

    return highways_proj[highways_proj.osmid.isin(
        ids_of_bus_ways)].length.sum() / highways_proj.length.sum()  # pokrycje sie zwiekszylo z 28 do 38 %


@timed
def tram_routes_to_highways(place):
    poi_tram_routes = ox.geometries_from_place(place, {'railway': 'tram'})
    poi_highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    if poi_tram_routes.empty:
        return 0

    tram_routes_proj = ox.project_gdf(poi_tram_routes)
    highways_proj = ox.project_gdf(poi_highways)

    return tram_routes_proj.length.sum() / highways_proj.length.sum()  # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS


@timed
def avg_dist_between_crossroads(place):
    start = timer()
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)
    g_proj = ox.project_graph(g)
    consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

    after_consolidated = timer()
    outdeg = consolidated.out_degree()
    to_keep = [n for (n, deg) in outdeg if deg > 1]

    consolidated_subgraph = consolidated.subgraph(to_keep)
    undir = ox.get_undirected(consolidated_subgraph)
    before_mean = timer()
    mean = np.mean([length_tuple[2] for length_tuple in undir.edges.data('length')])
    after_mean = timer()
    # print(str(after_mean - before_mean) + " " + str(before_mean - after_consolidated) + " " + str(after_consolidated - start))
    return mean


@timed
def streets_in_radius_of_100_m(place):
    highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    gdf = ox.project_gdf(highways)
    gdf['no_of_neighbours'] = gdf.apply(lambda row: len(within(gdf, row.geometry.buffer(100))), axis=1)
    return gdf['no_of_neighbours'].mean()


@timed
def share_of_separated_streets(place):
    highways = ox.geometries_from_place(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    gdf = ox.project_gdf(highways)
    gdf['no_of_neighbours'] = gdf.apply(lambda row: len(within(gdf, row.geometry.buffer(50))), axis=1)
    return gdf[gdf['no_of_neighbours'] < 4].shape[0] / gdf.shape[0]


@timed
def distance_between_buildings(place):
    buildingsDf = ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    try:
        buildings_polygons = ox.project_gdf(buildings_polygons)
    except AttributeError as ae:
        print(str(ae) + "for " + place)
        return 0

    try:
        buildings_polygons['dist_to_nearest_building'] = buildings_polygons.apply(
            lambda row: distance_to_nearest(buildings_polygons, row.geometry), axis=1)
    except ValueError as e:
        print(str(e) + " happened for " + place)
        return 1000000
    return buildings_polygons['dist_to_nearest_building'].mean()


all_functions = [
    average_street_length,
    intersection_density_km,
    street_density_km,
    circuity_avg,
    one_way_percentage,
    primary_percentage,
    average_dist_to_park,
    average_dist_to_bus_stop,
    buildings_density,
    natural_terrain_density,
    cycleways_to_highways,
    bus_routes_to_highways,
    tram_routes_to_highways,
    avg_dist_between_crossroads,
    streets_in_radius_of_100_m,
    share_of_separated_streets
]
