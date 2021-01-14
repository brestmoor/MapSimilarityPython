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
        df_functions.distance_between_buildings,
        df_functions.natural_terrain_density,
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
        df_functions.distance_between_buildings,
        # df_functions.avg_dist_between_crossroads,
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
    'buses_and_cycleways': [
        df_functions.average_dist_to_bus_stop,
        df_functions.bus_routes_to_highways,
        df_functions.cycleways_to_highways,
        df_functions.tram_routes_to_highways
    ],
    'subway': [
        graph_functions.average_how_many_subway_routes_are_there_from_one_stop_to_another,
        graph_functions.how_many_failures_can_network_handle,
    ],
    'facilities': [
        graph_functions.avg_short_distances_between_hospitals,
        graph_functions.avg_short_distances_between_train_stations_and_city_center,
        graph_functions.longest_cycleway_network,
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

