import itertools
from math import sqrt
from statistics import mode, mean, stdev
from timeit import default_timer as timer

import random
import numpy as np
import osmnx as ox
from osmnx.projection import project_geometry
import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point

from util.function_util import memoize, timed
from osmApi import get_ways_in_relation, get_city_center, get_city_center_coordinates, get_city_center_geometry
from util.graphUtils import great_circle_dist, path_len_digraph, shortest_path
from util.spatial_util import distance_to_nearest, within, convert_crs, distances_to_multiple_nearest, simplify_bearing

ox.config(log_console=False, use_cache=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)


@memoize
def basic_stats(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'

    @timed
    def graph_from_place_basic_stats(inner_place):
        return ox.graph_from_place(inner_place, network_type='drive', custom_filter=cf)

    G = graph_from_place_basic_stats(place)
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
def streets_per_node_avg(place):
    return basic_stats(place)['streets_per_node_avg']


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


# @timed
# def share_of_dead_end_street(place):
#     cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
#     g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)
#
#     g.
#     mean = np.mean([length_tuple[2] for length_tuple in undir.edges.data('length')])
#     return mean


@timed
def median_dist_between_crossroads(place):
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
    median = np.median([length_tuple[2] for length_tuple in undir.edges.data('length')])
    after_mean = timer()
    print(str(after_mean - before_mean) + " " + str(before_mean - after_consolidated) + " " + str(
        after_consolidated - start))
    return median


@timed
def mode_dist_between_crossroads(place):
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
    result_mode = mode(([round(length_tuple[2], -1) for length_tuple in undir.edges.data('length')]))
    after_mean = timer()
    print(str(after_mean - before_mean) + " " + str(before_mean - after_consolidated) + " " + str(
        after_consolidated - start))
    return result_mode


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
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    center = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
    dist_to_center = buildingsDf.apply(lambda row: row.geometry.centroid.distance(center), axis=1)
    return dist_to_center.mean()


@timed
def pubs_density(place):
    return amenity_density(place, {
        "amenity": ["pub", "bar", "bbq", "cafe", "nightclub", "fast_food", "food_court", "ice_cream", "restaurant"]
    })


@timed
def education_buildings_density(place):
    return amenity_density(place, {
        "amenity": ["library", "school", "university", "college", "language_school"],
        "tourism": ["museum"]
    })


@timed
def entertainment_buildings_density(place):
    return amenity_density(place, {
        "amenity": ["casino", "cinema", "community_centre", "theatre", "language_school"],
        "leisure": ["dance", "bowling_alley", "amusement_arcade", "fitness_centre", "fitness_station"]
    })


@timed
def shops_density(place):
    return amenity_density(place, {"shop": True})


@timed
def office_density(place):
    return amenity_density(place, {"office": True})


@timed
def amenity_density(place, amenities):
    amenities = ox.geometries_from_place(place, amenities)
    city_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

    return len(amenities) / (city_boundary.area[0] / 1000000)


@timed
def buildings_uniformity(place):
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    city_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

    distances_to_nearest = buildingsDf.apply(lambda row: distances_to_multiple_nearest(buildingsDf, row.geometry, 4),
                                             axis=1)
    mean_of_distances = distances_to_nearest.explode().mean()

    expected_avg_dist_to_nearest = sqrt(city_boundary.area[0] / len(buildingsDf))
    return mean_of_distances / expected_avg_dist_to_nearest


@timed
def avg_distance_to_5_buildings(place):
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    city_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

    distances_to_nearest = buildingsDf.apply(lambda row: distances_to_multiple_nearest(buildingsDf, row.geometry, 5),
                                             axis=1)
    mean_of_distances = distances_to_nearest.explode().mean()

    return mean_of_distances


@timed
def share_of_buildings_near_center(place):
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    city_boundary_area = ox.project_gdf(ox.geocode_to_gdf(place)).area[0]

    r_of_1_10th_circle = sqrt(city_boundary_area / (10 * np.math.pi))

    projected_point = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
    circle = projected_point.buffer(r_of_1_10th_circle)

    return sum([circle.contains(building) for building in buildingsDf.geometry.centroid]) / len(buildingsDf)


@timed
def avg_building_area(place):
    buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {
        'building': ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'house', 'residential',
                     'terrace', 'commercial',
                     'industrial', 'office', 'retail', 'supermarket', 'warehouse', 'civic', 'hospital', 'public',
                     'school', 'train_station', 'university', 'semidetached_house']}))

    buildingsDf = buildingsDf[[isinstance(x, Polygon) for x in buildingsDf.geometry]]

    return buildingsDf.apply(lambda row: row.geometry.area, axis=1).mean()


@timed
def circuity(place):
    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)

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
    g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)

    g = ox.add_edge_bearings(ox.get_undirected(g))
    bearings = pd.Series([simplify_bearing(d['bearing']) for u, v, k, d in g.edges(keys=True, data=True)])
    bearings = bearings.map(lambda bearing: round(bearing, -1))
    bearings = bearings.map(lambda bearing: bearing if bearing != 180 else 0)
    expected_number_in_group = len(bearings) / 18
    frequency = bearings.groupby(bearings).count()

    return stdev(frequency, expected_number_in_group) / expected_number_in_group

network_orientation("Torrevieja, Spain")

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
