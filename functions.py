import itertools
import logging
import sys
from math import sqrt
from statistics import mode, mean, stdev
from timeit import default_timer as timer

import random

import networkx as nx
import numpy as np
import osmnx as ox
from osmnx.projection import project_geometry
import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point

from ox_api import geometries_from_place_or_rel_id, graph_from_place_or_rel_id, geocode_to_gdf_by_place_or_rel_id
from util.function_util import memoize, timed
from osmApi import get_ways_in_relation, get_city_center, get_city_center_coordinates, get_city_center_geometry, \
    get_count, get_city_population
from util.graphUtils import great_circle_dist, path_len_digraph, shortest_path
from util.spatial_util import distance_to_nearest, within, convert_crs, distances_to_multiple_nearest, simplify_bearing, \
    circle_radius
ox.config(log_console=False, timeout=300,
          use_cache=True,
          overpass_endpoint='http://localhost:12346/api',
          overpass_rate_limit=False, max_query_area_size = 2 * 1000 * 50 * 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)



@memoize
def basic_stats(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'

    @timed
    def graph_from_place_basic_stats(inner_place):
        return graph_from_place_or_rel_id(inner_place, network_type='drive', custom_filter=cf)

    G = graph_from_place_basic_stats(place)
    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    graph_area_m = nodes_proj.unary_union.convex_hull.area

    return ox.basic_stats(G_proj, area=graph_area_m, clean_int_tol=15)

@memoize
def basic_stats_in_1km_radius(place):
    address = None
    if place.isnumeric():
        gdf = ox.geocode_to_gdf('R' + place, by_osmid=True)
        address = gdf.name
    else:
        address = place

    city_center, crs = project_geometry(Point(get_city_center_coordinates(address)))
    city_center_area = city_center.buffer(1000)
    city_center_area_proj, crs = project_geometry(city_center_area, crs, to_latlong=True)
    G = ox.graph_from_polygon(city_center_area_proj)
    G_proj = ox.project_graph(G)

    return ox.basic_stats(G_proj, area=ox.graph_to_gdfs(G_proj, edges=False).unary_union.convex_hull.area, clean_intersects=True, circuity_dist='euclidean')


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
def streets_per_node_avg(place):
    return basic_stats(place)['streets_per_node_avg']

@timed
def average_street_length_1km(place):
    return basic_stats_in_1km_radius(place)['street_length_avg']


@timed
def intersection_density_km_1km(place):
    return basic_stats_in_1km_radius(place)['intersection_density_km']


@timed
def street_density_km_1km(place):
    return basic_stats_in_1km_radius(place)['street_density_km']


@timed
def circuity_avg_1km(place):
    return basic_stats_in_1km_radius(place)['circuity_avg']


@timed
def streets_per_node_avg_1km(place):
    return basic_stats_in_1km_radius(place)['streets_per_node_avg']


@timed
def one_way_percentage(place):
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    oneway_count = 0 if 'oneway' not in highways.columns else len(highways.loc[highways['oneway'] == 'yes']) / len(highways)
    return oneway_count


@timed
def trunk_percentage(place):
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    primary_count = len(highways.loc[highways['highway'] == 'trunk']) / len(highways)
    return primary_count

@timed
def primary_percentage(place):
    start = timer()
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    got_df = timer()
    try:
        primary_count = len(highways.loc[highways['highway'] == 'primary']) / len(highways)
        print("df took:" + str(got_df - start) + " calc: " + str(timer() - got_df))
        return primary_count
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))

@timed
def secondary_percentage(place):
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    try:
        primary_count = len(highways[highways['highway'] == 'secondary']) / len(highways)
        return primary_count
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))

@timed
def tertiary_percentage(place):
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    try:
        primary_count = len(highways.loc[highways['highway'] == 'tertiary']) / len(highways)
        return primary_count
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))


@timed
def traffic_lights_share(place):
    highways = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'highway': ['trunk', 'primary', 'secondary', 'tertiary']}))

    traffic_signals = geometries_from_place_or_rel_id(place, {
        'highway': 'traffic_signals'})
    try:
        return len(traffic_signals) / highways.geometry.length.sum()
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))


@timed
def crossing_share(place):
    highways = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'highway': ['trunk', 'primary', 'secondary', 'tertiary']}))

    crossings = geometries_from_place_or_rel_id(place, {
        'highway': 'crossing'})
    try:
        return len(crossings) / highways.geometry.length.sum()
    except KeyError as k:
        print(k)
        print("Occured for " + str(place))


@timed
def average_dist_to_park(place):
    parksDf = geometries_from_place_or_rel_id(place, {'leisure': 'park'})

    if parksDf.empty:
        return 10000

    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    parks_proj = ox.project_gdf(parks_polygons)

    distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(parks_proj, row.geometry), axis=1)
    return distances.mean()

@timed
def average_dist_to_greenland(place):
    parksDf = geometries_from_place_or_rel_id(place, {'leisure': ['park', 'garden'], 'landuse': ['forest', 'grass'], 'natural': 'wood'})

    if parksDf.empty:
        return 10000

    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    parks_proj = ox.project_gdf(parks_polygons)

    distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(parks_proj, row.geometry), axis=1)
    return distances.mean()


@timed
def average_dist_to_bus_stop(place):
    print("starting avg_dist_to_bus_stop " + place)
    start = timer()
    bus_df = geometries_from_place_or_rel_id(place, {'highway': 'bus_stop'})
    if bus_df.empty:
        return 10000

    got_stops = timer()

    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    got_buildings = timer()

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    bus_proj = ox.project_gdf(bus_df)
    distances = buildings_proj.iloc[::10].apply(lambda row: distance_to_nearest(bus_proj, row.geometry), axis=1)
    distances_calculated = timer()
    print("stops: " + str(got_stops - start) + " graph:  " + str(got_buildings - got_stops) + "distances: " + str(distances_calculated - got_buildings))
    return distances.mean()



@timed
def average_dist_to_any_public_transport_stop(place):
    print("average_dist_to_any_public_transport_stop" + place)
    start = timer()
    bus_df = geometries_from_place_or_rel_id(place, {'highway': 'bus_stop', 'public_transport': 'stop_position'})
    if bus_df.empty:
        return 10000


    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    got_df_and_graph = timer()

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    bus_proj = ox.project_gdf(bus_df)
    distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(bus_proj, row.geometry), axis=1)
    distances_calculated = timer()
    # print("graph: " + str(got_df_and_graph - start) + " distances: " + str(distances_calculated - got_df_and_graph))
    return distances.mean()

@timed
def mode_dist_to_any_public_transport_stop(place):
    print("average_dist_to_any_public_transport_stop" + place)
    start = timer()
    bus_df = geometries_from_place_or_rel_id(place, {'highway': 'bus_stop', 'public_transport': 'stop_position'})
    if bus_df.empty:
        return 10000


    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    got_df_and_graph = timer()

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    buildings_proj = ox.project_gdf(buildings_polygons)
    bus_proj = ox.project_gdf(bus_df)
    distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(bus_proj, row.geometry), axis=1)
    distances_calculated = timer()
    # print("graph: " + str(got_df_and_graph - start) + " distances: " + str(distances_calculated - got_df_and_graph))
    return distances.round(-1).mode()[0]


@timed
def buildings_density(place):
    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]
    if 'element_type' in buildings_polygons.columns:
        buildings_polygons = buildings_polygons[buildings_polygons.element_type == 'way']

    try:
        buildings_proj = ox.project_gdf(buildings_polygons)
    except AttributeError as ae:
        print(str(ae) + "for " + place)
        return 0

    krakow_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))

    return buildings_proj.area.sum() / krakow_boundary.area[0]

@timed
def no_of_streets_crossing_boundary(place):
    krakow_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))
    poi_highways = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']}, buffer_dist=400))

    return sum(poi_highways.crosses(krakow_boundary.iloc[0].geometry))

@timed
def no_of_railways_crossing_boundary(place):
    krakow_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))
    railwaysDf = geometries_from_place_or_rel_id(place, {'railway': True}, buffer_dist=400)

    if railwaysDf.empty:
        return 0

    railwaysDf_projected = ox.project_gdf(railwaysDf)

    return sum(railwaysDf_projected.crosses(krakow_boundary.iloc[0].geometry))

@timed
def no_of_streets_crossing_boundary_proportional(place):
    krakow_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))
    poi_highways = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']}, buffer_dist=400))

    return sum(poi_highways.crosses(krakow_boundary.iloc[0].geometry)) / krakow_boundary.iloc[0].geometry.length

@timed
def natural_terrain_density(place):
    parksDf = geometries_from_place_or_rel_id(place, {'leisure': ['park', 'garden'],
                                               'natural': ['wood', 'scrub', 'heath', 'grassland'],
                                               'landuse': ['grass', 'forest']})

    parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
    if 'element_type' in parks_polygons.columns:
        parks_polygons = parks_polygons[parks_polygons.element_type == 'way']

    if parks_polygons.empty:
        return 0

    parks_proj = ox.project_gdf(parks_polygons)

    krakow_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))

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
#     parksDf = geometries_from_place_or_rel_id(place, {'leisure': 'park'})
#     parks_filtered = parksDf[parksDf['leisure'] == 'park']
#
#     return len([isinstance(x, Polygon) for x in parks_filtered.geometry])

@timed
def cycleways_to_highways(place):
    print("starting cycleways_to_highways " + place)
    poi_cycleways = geometries_from_place_or_rel_id(place, {'highway': 'cycleway',
                                                     'cycleway': ['lane', 'opposite_lane', 'opposite', 'shared_lane'],
                                                     'bicycle': 'designated'})
    poi_highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    if poi_cycleways.empty:
        return 0

    cycleways_proj = ox.project_gdf(poi_cycleways)
    highways_proj = ox.project_gdf(poi_highways)

    return cycleways_proj.length.sum() / highways_proj.length.sum()  # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS


@timed
def bus_routes_to_highways(place):
    start = timer()
    print("Starting bus_routes_to_higways for: " + place)
    bus_routes_ways = get_ways_in_relation(place, '"route"="bus"')

    if not bus_routes_ways:
        return 0

    got_ways = timer()
    ids_of_bus_ways = [x['ref'] for x in bus_routes_ways]
    poi_highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    got_pois = timer()
    highways_proj = ox.project_gdf(poi_highways)

    proportion = highways_proj[highways_proj.index.isin(ids_of_bus_ways, level='osmid')].length.sum() / highways_proj.length.sum()
    calculated_proportion = timer()
    # print("got bus routes: " + str(got_ways - start) + " got pois: " + str(got_pois - got_ways) +  " calculated proportion" + str(calculated_proportion - got_pois))
    return proportion


@timed
def tram_routes_to_highways(place):
    poi_tram_routes = geometries_from_place_or_rel_id(place, {'railway': 'tram'})
    poi_highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    if poi_tram_routes.empty:
        return 0

    tram_routes_proj = ox.project_gdf(poi_tram_routes)
    highways_proj = ox.project_gdf(poi_highways)

    return tram_routes_proj.length.sum() / highways_proj.length.sum()  # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS

@timed
def all_railways_to_highway(place):
    poi_tram_routes = geometries_from_place_or_rel_id(place, {'railway': True})
    poi_highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

    if poi_tram_routes.empty:
        return 0

    tram_routes_proj = ox.project_gdf(poi_tram_routes)
    highways_proj = ox.project_gdf(poi_highways)

    return tram_routes_proj.length.sum() / highways_proj.length.sum()  # ilosc krawedzi i suma jest 2 razy mniejsza niz w przypadku PostGIS



@timed
def median_dist_between_crossroads(place):
    start = timer()
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = graph_from_place_or_rel_id(place, network_type='drive', custom_filter=cf)
    g_proj = ox.project_graph(g)
    consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

    after_consolidated = timer()
    outdeg = consolidated.out_degree()
    to_keep = [n for (n, deg) in outdeg if deg > 1]

    consolidated_subgraph = consolidated.subgraph(to_keep)
    undir = ox.get_undirected(consolidated)
    before_mean = timer()
    median = np.median([length_tuple[2] for length_tuple in undir.edges.data('length')])
    after_mean = timer()
    print(str(after_mean - before_mean) + " " + str(before_mean - after_consolidated) + " " + str(
        after_consolidated - start))
    return median


@timed
def mode_dist_between_crossroads(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = graph_from_place_or_rel_id(place, network_type='drive', custom_filter=cf)
    g_proj = ox.project_graph(g)
    consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

    outdeg = consolidated.out_degree()
    to_keep = [n for (n, deg) in outdeg if deg > 1]

    consolidated_subgraph = consolidated.subgraph(to_keep)
    undir = ox.get_undirected(consolidated)
    result_mode = mode(([round(length_tuple[2], -1) for length_tuple in undir.edges.data('length')]))
    return result_mode


@timed
def streets_in_radius_of_100_m(place):
    start = timer()
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    got_df = timer()
    gdf = ox.project_gdf(highways)
    projected_df = timer()
    gdf['no_of_neighbours'] = gdf.iloc[::5].apply(lambda row: len(within(gdf, row.geometry.buffer(100))), axis=1)
    calculated = timer()
    print("Getting df: " + str(got_df - start) + ", streets in radious " + str(calculated - projected_df))
    return gdf['no_of_neighbours'].mean()


@timed
def share_of_separated_streets(place):
    highways = geometries_from_place_or_rel_id(place, {
        'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    gdf = ox.project_gdf(highways)
    no_of_neighbors = gdf.apply(lambda row: len(within(gdf, row.geometry.buffer(50))), axis=1)
    return no_of_neighbors[no_of_neighbors < 4].count() / len(gdf)


@timed
def avg_distance_between_buildings(place):
    print("downloading buildings for " + place)
    buildingsDf = geometries_from_place_or_rel_id(place, {
        'building': True})

    print("got buildings for " + place)
    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    try:
        buildings_polygons = ox.project_gdf(buildings_polygons)
    except AttributeError as ae:
        print(str(ae) + "for " + place)
        return 0

    try:
        buildings_polygons['dist_to_nearest_building'] = buildings_polygons.iloc[::5].apply(
            lambda row: distance_to_nearest(buildings_polygons, row.geometry), axis=1)
    except ValueError as e:
        print(str(e) + " happened for " + place)
        return 10000
    return buildings_polygons['dist_to_nearest_building'].mean()


@timed
def buildings_density_in_2km_radius(place):
    projected_point, crs = project_geometry(Point(get_city_center_coordinates(place)))
    circle = projected_point.buffer(1000)
    buildingsDf = ox.geometries_from_polygon(project_geometry(circle, crs, to_latlong=True)[0], {'building': True})

    buildings_polygons = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]
    if 'element_type' in buildings_polygons.columns:
        buildings_polygons = buildings_polygons[buildings_polygons.element_type == 'way']

    try:
        buildings_proj = ox.project_gdf(buildings_polygons)
    except AttributeError as ae:
        print(str(ae) + "for " + place)
        return 0

    return buildings_proj.area.sum() / circle.area


@timed
def avg_dist_from_building_to_center(place):
    buildingsDf = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'building': True}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    center = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
    dist_to_center = buildingsDf.iloc[::3].apply(lambda row: row.geometry.centroid.distance(center), axis=1)
    return dist_to_center.mean()


@timed
def crossing_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {
        'highway': 'crossing'
    })

@timed
def pubs_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {
        "amenity": ["pub", "bar", "bbq", "cafe", "fast_food", "food_court", "ice_cream", "restaurant", "biergarten"]
    })


@timed
def education_buildings_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {
        "amenity": ["library", "school", "university", "college", "language_school"],
        "tourism": ["museum"]
    })


@timed
def entertainment_buildings_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {
        "amenity": ["casino", "cinema", "community_centre", "theatre", "nightclub"],
        "leisure": ["dance", "bowling_alley", "amusement_arcade", "fitness_centre", "fitness_station"]
    })


@timed
def shops_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"shop": True})

@timed
def office_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"office": True})

@timed
def historic_building_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"historic": True})

@timed
def police_building_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"amenity": "police"})


@timed
def fire_station_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"amenity": "fire_station"})


@timed
def hotels_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"tourism": ['hotel', 'hostel', 'motel', 'guest_house']})


@timed
def bench_dist_to_nearest(place):
    return amenity_dist_to_nearest(place, {"amenity": 'bench'})


@timed
def pubs_share(place):
    return amenity_to_all_buildings(place, {
        "amenity": ["pub", "bar", "bbq", "cafe", "fast_food", "food_court", "ice_cream", "restaurant", "biergarten"]
    })


@timed
def education_buildings_share(place):
    return amenity_to_all_buildings(place, {
        "amenity": ["library", "school", "university", "college", "language_school"],
        "tourism": ["museum"]
    })


@timed
def entertainment_buildings_share(place):
    return amenity_to_all_buildings(place, {
        "amenity": ["casino", "cinema", "community_centre", "theatre", "nightclub"],
        "leisure": ["dance", "bowling_alley", "amusement_arcade", "fitness_centre", "fitness_station"]
    })


@timed
def shops_share(place):
    return amenity_to_all_buildings(place, {"shop": True})


@timed
def office_share(place):
    return amenity_to_all_buildings(place, {"office": True})


@timed
def historic_building_share(place):
    return amenity_to_all_buildings(place, {"historic": True})

@timed
def police_building_share(place):
    return amenity_to_all_buildings(place, {"amenity": "police"})

@timed
def fire_stations_share(place):
    return amenity_to_all_buildings(place, {"amenity": "fire_station"})


@timed
def hotels_share(place):
    return amenity_to_all_buildings(place, {"tourism": ['hotel', 'hostel', 'motel', 'guest_house']})


@timed
def tourism_buildings_share(place):
    return amenity_to_all_buildings(place, {"tourism": True})


@timed
def attractions_share(place):
    return amenity_to_all_buildings(place, {"tourism": ['attraction']})


@timed
def artwork_share(place):
    return amenity_to_all_buildings(place, {"tourism": ['artwork']})


@timed
def camp_site_share(place):
    return amenity_to_all_buildings(place, {"tourism": ['caravan_site', 'camp_site', 'camp_pitch']})


@timed
def hospitals_share(place):
    return amenity_to_all_buildings(place, {"amenity": "hospital"})

def amenity_dist_to_nearest(place, amenities):
    start = timer()
    print("Starting amenity_density for: " + place + " " + str(amenities))

    amenities_df = geometries_from_place_or_rel_id(place, amenities)

    if len(amenities_df) <= 1:
        return 10000

    amenities_df_projected = ox.project_gdf(amenities_df)

    got_amenities = timer()
    distances_to_nearest = amenities_df_projected.apply(lambda row: distances_to_multiple_nearest(amenities_df_projected, row.geometry, 3),
                                         axis=1)
    if distances_to_nearest is None:
        return None
    calculated_dist_to_nearest = timer()
    mean_of_distances = distances_to_nearest.explode().mean()
    calculated_mean = timer()

    # print("Getting df: " + str(got_amenities - start) + ", distances to nearest: " + str(calculated_dist_to_nearest - got_amenities)
    #       + ", mean: " + str(calculated_mean - calculated_dist_to_nearest))
    return mean_of_distances



def amenity_to_all_buildings(place, amenities):
    print("Starting amenity_to_all_buildings for: " + place + " " + str(amenities))

    amenities_df = geometries_from_place_or_rel_id(place, amenities)
    if amenities_df.empty:
        return 0
    return len(amenities_df) / get_count(place, '"building"')

@timed
def buildings_uniformity(place):
    buildingsDf = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'building': True}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    city_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))

    distances_to_nearest = buildingsDf.iloc[::3].apply(lambda row: distances_to_multiple_nearest(buildingsDf, row.geometry, 4),
                                             axis=1)
    mean_of_distances = distances_to_nearest.explode().mean()

    expected_avg_dist_to_nearest = sqrt(city_boundary.area[0] / len(buildingsDf))
    return mean_of_distances / expected_avg_dist_to_nearest


@timed
def avg_distance_to_5_buildings(place):
    buildingsDf = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'building': True}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    distances_to_nearest = buildingsDf.iloc[::5].apply(lambda row: distances_to_multiple_nearest(buildingsDf, row.geometry, 5),
                                             axis=1)
    mean_of_distances = distances_to_nearest.explode().mean()

    return mean_of_distances


@timed
def share_of_buildings_near_center(place):
    buildingsDf = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'building': True}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    city_boundary_area = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place)).area[0]

    r_of_1_10th_circle = sqrt(city_boundary_area / np.math.pi) / 10

    projected_point = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
    circle = projected_point.buffer(r_of_1_10th_circle)

    return sum([circle.contains(building) for building in buildingsDf.geometry.centroid]) / len(buildingsDf)

@timed
def avg_building_area(place):
    a = timer()
    buildingsDf = ox.project_gdf(geometries_from_place_or_rel_id(place, {
        'building': True}))
    print('got: ' + str(a - timer()))
    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    return buildingsDf.geometry.area.mean()



@timed
def circuity(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = graph_from_place_or_rel_id(place, network_type='drive', custom_filter=cf, simplify=False)

    random_node_ids = random.sample(g.nodes, 30)

    nodes_pairs = list(itertools.combinations(random_node_ids, 2))

    city_paths = [path for path in (shortest_path(g, orig, dest) for orig, dest in nodes_pairs) if path is not None]

    nodes_pairs = [(path[0], path[-1]) for path in city_paths]

    city_paths_lengths = sum(path_len_digraph(g, path) for path in city_paths)
    great_circle_paths_lengths = sum([great_circle_dist(g, orig, dest) for orig, dest in nodes_pairs])

    return city_paths_lengths / great_circle_paths_lengths

@timed
def network_orientation(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = graph_from_place_or_rel_id(place, network_type='drive', custom_filter=cf, simplify=False)

    g = ox.add_edge_bearings(ox.get_undirected(g))
    bearings = pd.Series([simplify_bearing(d['bearing']) for u, v, k, d in g.edges(keys=True, data=True)])
    bearings = bearings.map(lambda bearing: round(bearing, -1))
    bearings = bearings.map(lambda bearing: bearing if bearing != 180 else 0)
    expected_number_in_group = len(bearings) / 18
    frequency = bearings.groupby(bearings).count()

    return stdev(frequency, expected_number_in_group) / expected_number_in_group


@timed
def population_per_km(place):
    population = get_city_population(place)
    city_boundary = ox.project_gdf(geocode_to_gdf_by_place_or_rel_id(place))
    boundary_in_km2 = city_boundary.area[0] / 1000000

    if population is None:
        return None
    else:
        return population / boundary_in_km2


@timed
def roads_curvature(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.get_undirected(graph_from_place_or_rel_id(place, network_type='drive', custom_filter=cf, simplify=False))
    triplets_per_node = [_get_triplets(g[node], node) for node in g.nodes if len(g[node]) > 1]
    triplets_with_data = [[g[node] for node in triplet] for triplet in triplets_per_node]
    triplets = list(itertools.chain(*triplets_with_data))
    [circle_radius(*triplet) * sum([ox.great_circle_vec() ]) for triplet in triplets]


def _get_triplets(g, node):
    neighbors_combinations = list(itertools.combinations(g[node], 2))
    return [(combination[0], node, combination[1]) for combination in neighbors_combinations]

def haversine_length(nodes):
    result = 0
    for node in nodes:
        ox.great_circle_vec(node.x)


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
    streets_in_radius_of_100_m,
    share_of_separated_streets
]

