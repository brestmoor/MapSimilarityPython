import pandas as pd

import functions as df_functions
import graphFunctions as graph_functions
from scores import calculate_scores
from similarity import similarity

all_criteria = {
    'roads_and_buildings': [
        df_functions.average_street_length,
        df_functions.intersection_density_km,
        df_functions.buildings_density,
        df_functions.avg_distance_between_buildings,
        df_functions.natural_terrain_density,
    ],
    'buildings': [
        df_functions.avg_distance_between_buildings,
        df_functions.avg_distance_to_5_buildings,
        df_functions.buildings_uniformity,
        df_functions.avg_building_area,
        df_functions.average_dist_to_any_public_transport_stop,
        df_functions.average_dist_to_greenland,
        df_functions.average_dist_to_park,
        df_functions.primary_percentage,
        df_functions.traffic_lights_share,
        df_functions.traffic_lights_share,
        df_functions.trunk_percentage,
        df_functions.primary_percentage,
        df_functions.secondary_percentage,
        df_functions.tertiary_percentage,
        df_functions.all_railways_to_highway,
        df_functions.mode_dist_to_any_public_transport_stop,
        df_functions.average_dist_to_bus_stop
    ],
    'city_structure': [
        df_functions.circuity_avg,
        df_functions.average_street_length,
        df_functions.one_way_percentage,
        df_functions.share_of_separated_streets,
    ],
    'city_structure_extended': [
        df_functions.circuity_avg,
        df_functions.average_street_length,
        df_functions.one_way_percentage,
        df_functions.intersection_density_km,
        df_functions.share_of_separated_streets,
        df_functions.avg_distance_between_buildings,
        df_functions.avg_dist_from_building_to_center,
        df_functions.buildings_uniformity,
        df_functions.share_of_buildings_near_center,
        df_functions.avg_building_area,
        #
        df_functions.natural_terrain_density,
        df_functions.buildings_density,
        df_functions.avg_dist_between_crossroads,
        df_functions.median_dist_between_crossroads,
        df_functions.mode_dist_between_crossroads,
        df_functions.streets_per_node_avg,
        df_functions.circuity,
        df_functions.avg_distance_to_5_buildings,
        # df_functions.buildings_density_in_2km_radius,
        # df_functions.network_orientation,
        df_functions.circuity_between_crossroads,
        df_functions.average_dist_to_bus_stop,
        df_functions.average_dist_to_park,

        df_functions.bus_routes_to_highways
    ],
    'industrial_and_buses': [
        df_functions.buildings_density,
        df_functions.natural_terrain_density,
        df_functions.average_dist_to_bus_stop,
        df_functions.average_dist_to_park,
        df_functions.bus_routes_to_highways,
    ],
    'roads': [
        df_functions.average_street_length,
        df_functions.intersection_density_km,
        df_functions.street_density_km,
        df_functions.circuity_avg,
        # df_functions.one_way_percentage,
        # df_functions.primary_percentage,
        df_functions.share_of_separated_streets,
        df_functions.streets_in_radius_of_100_m,
        df_functions.avg_dist_between_crossroads,
    ],
    'buildings_and_terrain': [
        df_functions.average_dist_to_park,
        df_functions.average_dist_to_bus_stop,
        df_functions.buildings_density,
        df_functions.natural_terrain_density
    ],
    'buses_and_trams': [
        df_functions.average_dist_to_bus_stop,
        df_functions.bus_routes_to_highways,
        df_functions.cycleways_to_highways,
        df_functions.tram_routes_to_highways,
        df_functions.all_railways_to_highway
    ],
    'subway': [
        graph_functions.average_how_many_subway_routes_are_there_from_one_stop_to_another,
        graph_functions.how_many_failures_can_network_handle,
    ],
    'city_planning': [
        graph_functions.avg_short_distances_between_hospitals,
        graph_functions.avg_short_distances_between_train_stations_and_city_center,
        graph_functions.longest_cycleway_network,
    ],
    'facilities': [
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

        df_functions.cycleways_to_highways
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
        df_functions.avg_dist_between_crossroads,
        #
        df_functions.circuity,
        df_functions.avg_distance_to_5_buildings,
        df_functions.avg_distance_between_buildings,
        df_functions.buildings_density_in_2km_radius,
        df_functions.avg_building_area,
        #
        df_functions.network_orientation,
        df_functions.circuity_between_crossroads,
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
        df_functions.avg_dist_between_crossroads,

        df_functions.circuity,

        df_functions.network_orientation,
        df_functions.circuity_between_crossroads,
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

