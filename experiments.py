from similarity import similarity
import functions as df_functions
import graphFunctions as graph_functions
import pandas as pd

all_functions = df_functions.all_functions + graph_functions.all_functions

roads = [
    df_functions.average_street_length,
    df_functions.intersection_density_km,
    df_functions.street_density_km,
    df_functions.circuity_avg,
    df_functions.one_way_percentage,
    df_functions.primary_percentage,
    df_functions.share_of_separated_streets,
    df_functions.streets_in_radius_of_100_m,
    df_functions.avg_dist_between_crossroads,
]

buildings_and_terrain = [
    df_functions.average_dist_to_park,
    df_functions.average_dist_to_bus_stop,
    df_functions.buildings_coverage,
    df_functions.natural_terrain_coverage
]

buses_and_cycleways = [
    df_functions.average_dist_to_bus_stop,
    df_functions.bus_routes_to_highways,
    df_functions.cycleways_to_highways,
    df_functions.tram_routes_to_highways
]


def run(places, functions):
    scores = {place: [function(place) for function in functions] for place in places}
    scores_df = pd.DataFrame(scores)
    return similarity(scores_df)


# run(["Krakow, Poland", "Wroclaw, Poland"], buses_and_cycleways)
