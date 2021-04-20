import pandas as pd

import functions as df_functions
import graphFunctions as graph_functions
from scores import calculate_scores
from similarity import similarity

all_criteria = {
    'buildings': [
        df_functions.avg_distance_between_buildings,
        df_functions.buildings_density,
        df_functions.avg_building_area,
        df_functions.buildings_uniformity,
        df_functions.avg_dist_from_building_to_center,
        df_functions.share_of_buildings_near_center
    ],
    'public_transport': [
        df_functions.average_dist_to_any_public_transport_stop,
        df_functions.bus_routes_to_highways,
        df_functions.tram_routes_to_highways
    ],
    'city_facilities': [
        df_functions.cycleways_to_highways,
        df_functions.average_dist_to_park,
        df_functions.crossing_share,
        df_functions.traffic_lights_share,
        # df_functions.bench_dist_to_nearest,

        df_functions.police_building_share,

        df_functions.fire_stations_share,

        df_functions.hospitals_share,
        # df_functions.playground_share,

        graph_functions.avg_short_distances_between_hospitals
    ],
    'streets': [
        df_functions.trunk_percentage,
        df_functions.primary_percentage,
        df_functions.secondary_percentage,
        df_functions.tertiary_percentage,
        df_functions.one_way_percentage,
        df_functions.average_street_length,
        df_functions.street_density_km,
        df_functions.intersection_density_km,
        df_functions.streets_in_radius_of_100_m,
        df_functions.share_of_separated_streets,
        df_functions.no_of_streets_crossing_boundary_proportional,
    ],
    'city_structure': [
        df_functions.circuity_avg,
        df_functions.circuity,
        df_functions.network_orientation,
        df_functions.streets_per_node_avg
    ],
    'railways': [
        df_functions.all_railways_to_highway,
        df_functions.no_of_railways_crossing_boundary
    ],
    'points_of_interest': [
        df_functions.pubs_dist_to_nearest,
        df_functions.education_buildings_dist_to_nearest,
        df_functions.entertainment_buildings_dist_to_nearest,
        df_functions.shops_dist_to_nearest,
        df_functions.office_dist_to_nearest,

        df_functions.pubs_share,
        df_functions.education_buildings_share,
        df_functions.entertainment_buildings_share,
        df_functions.shops_share,
        df_functions.office_share,
    ],
    'subway': [
        graph_functions.average_how_many_subway_routes_are_there_from_one_stop_to_another,
        graph_functions.how_many_failures_can_network_handle,
    ],
    'historic': [
        df_functions.historic_building_dist_to_nearest,
        df_functions.historic_building_share,
    ],
    'tourism': [
        df_functions.hotels_share,
        df_functions.hotels_dist_to_nearest,
    ],
    'population': [
        df_functions.population_per_km
    ],
    'temp': [
        df_functions.population_per_km,
        df_functions.hotels_share,
        df_functions.hotels_dist_to_nearest,
        df_functions.bench_dist_to_nearest,

        df_functions.police_building_share,
        df_functions.police_building_dist_to_nearest,

        df_functions.fire_station_dist_to_nearest,
        df_functions.fire_stations_share,
    ],
    'all_ruhr_bavaria': [
        df_functions.intersection_density_km,
        df_functions.street_density_km,
        df_functions.buildings_density,
        df_functions.natural_terrain_density,

        df_functions.pubs_dist_to_nearest,
        df_functions.education_buildings_dist_to_nearest,
        df_functions.entertainment_buildings_dist_to_nearest,
        df_functions.shops_dist_to_nearest,
        df_functions.office_dist_to_nearest,

        df_functions.pubs_share,
        df_functions.education_buildings_share,
        df_functions.entertainment_buildings_share,
        df_functions.shops_share,
        df_functions.office_share,

        df_functions.average_dist_to_any_public_transport_stop,
        df_functions.mode_dist_to_any_public_transport_stop,
        df_functions.cycleways_to_highways,
        df_functions.all_railways_to_highway,
        df_functions.avg_dist_from_building_to_center,
        df_functions.average_dist_to_park,
        df_functions.average_dist_to_greenland,

        df_functions.average_street_length,
        #
        df_functions.circuity_avg,
        df_functions.one_way_percentage,
        df_functions.share_of_separated_streets,
        df_functions.streets_in_radius_of_100_m,
        #
        df_functions.circuity,
        df_functions.avg_distance_to_5_buildings,
        df_functions.avg_distance_between_buildings,
        df_functions.buildings_density_in_2km_radius,
        df_functions.avg_building_area,
        #
        df_functions.network_orientation,
        df_functions.streets_per_node_avg,
        #
        df_functions.buildings_uniformity,
        df_functions.share_of_buildings_near_center,
        #
        df_functions.traffic_lights_share,
        #
        df_functions.trunk_percentage,
        df_functions.primary_percentage,
        df_functions.secondary_percentage,
        df_functions.tertiary_percentage,
        df_functions.no_of_streets_crossing_boundary,

    ],
    'all_spain_england': [
        df_functions.intersection_density_km,
        df_functions.street_density_km,
        df_functions.natural_terrain_density,

        df_functions.cycleways_to_highways,
        df_functions.all_railways_to_highway,

        df_functions.average_street_length,

        df_functions.circuity_avg,
        df_functions.one_way_percentage,
        df_functions.share_of_separated_streets,
        df_functions.streets_in_radius_of_100_m,

        df_functions.circuity,

        df_functions.network_orientation,
        df_functions.streets_per_node_avg,

        df_functions.traffic_lights_share,
        df_functions.trunk_percentage,
        df_functions.primary_percentage,
        df_functions.secondary_percentage,
        df_functions.tertiary_percentage,
    ],
    'crossing_boundary_and_1km': [
        df_functions.no_of_streets_crossing_boundary,
        df_functions.no_of_streets_crossing_boundary_proportional,

        df_functions.circuity_avg_1km,
        df_functions.street_density_km_1km,
        df_functions.average_street_length_1km,
        df_functions.intersection_density_km_1km,
        df_functions.streets_per_node_avg_1km,
    ],

    'all_functions': df_functions.all_functions + graph_functions.all_functions
}


def get_scores_and_similarity(places, criteria_str):
    criteria = []
    for criterion in criteria_str:
        criteria.extend(all_criteria[criterion])
    scores = calculate_scores(places, criteria)
    return scores, similarity(scores)


def get_scores(places, criteria_str):
    criteria = []
    for criterion in criteria_str:
        criteria.extend(all_criteria[criterion])
    scores = calculate_scores(places, criteria)
    return scores

from inspect import getmembers, isfunction

import functions as fn

all_fns_names = ['avg_distance_between_buildings',
'buildings_density',
'avg_building_area',
'buildings_uniformity',
'avg_dist_from_building_to_center',
'share_of_buildings_near_center',
'average_dist_to_any_public_transport_stop',
'bus_routes_to_highways',
'tram_routes_to_highways',
'cycleways_to_highways',
'average_dist_to_park',
'crossing_share',
'traffic_lights_share',
'trunk_percentage',
'primary_percentage',
'secondary_percentage',
'tertiary_percentage',
'one_way_percentage',
'average_street_length',
'street_density_km',
'intersection_density_km',
'streets_in_radius_of_100_m',
'share_of_separated_streets',
'circuity_avg',
'circuity',
'network_orientation',
'streets_per_node_avg',
'all_railways_to_highway',
'circuity_avg',
'average_street_length',
'one_way_percentage',
'share_of_separated_streets',
'pubs_dist_to_nearest',
'education_buildings_dist_to_nearest',
'entertainment_buildings_dist_to_nearest',
'shops_dist_to_nearest',
'office_dist_to_nearest',
'pubs_share',
'education_buildings_share',
'entertainment_buildings_share',
'shops_share',
'office_share']

print([t[0] for t in getmembers(fn, isfunction) if t[0] not in all_fns_names])