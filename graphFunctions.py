import functools
import itertools as itertools

import networkx as nx
import numpy as np
import osmnx as ox
from osmnx import utils_graph

import osmApi as api
from noOfSubwayRoutes import average_how_many_subway_routes_are_there_from_one_stop_to_another
from noOfSubwayRoutes import how_many_failures_can_network_handle

ox.config(log_console=False, use_cache=True)


def _to_coordindates(shape):
    return (shape.y, shape.x)


def avg_short_distances_between_hospitals(place):
    network_graph = ox.graph_from_place(place, network_type='drive')

    hospitals = ox.geometries_from_place(place, {'amenity': 'hospital'})
    hospitals_centroids = hospitals.geometry.centroid
    centroids_as_tuples = [_to_coordindates(centroid) for centroid in hospitals_centroids]
    hospital_nodes = [ox.get_nearest_node(network_graph, coords_tuple) for coords_tuple in centroids_as_tuples]
    hospital_pairs = list(itertools.combinations(hospital_nodes, 2))
    shortest_paths = [ox.shortest_path(network_graph, *pair) for pair in hospital_pairs]
    sums = [sum(ox.utils_graph.get_route_edge_attributes(network_graph, path, 'length')) for path in shortest_paths]
    return np.mean(sums)


def avg_short_distances_between_train_stations_and_city_center(place):
    network_graph = ox.graph_from_place(place, network_type='drive')

    train_stations_centroids = ox.geometries_from_place(place, {'railway': 'station'}).geometry.centroid
    centroids_as_tuples = [_to_coordindates(centroid) for centroid in train_stations_centroids]
    train_station_nodes = [ox.get_nearest_node(network_graph, coords_tuple) for coords_tuple in centroids_as_tuples]

    city_center_node = ox.get_nearest_node(network_graph, api.get_city_center(place))

    pairs = [(city_center_node, train_station_node) for train_station_node in train_station_nodes]
    shortest_paths = [ox.shortest_path(network_graph, *pair) for pair in pairs]
    sums = [sum(ox.utils_graph.get_route_edge_attributes(network_graph, path, 'length')) for path in shortest_paths]
    return np.mean(sums)


def longest_cycleway_network(place):
    other_cycleways = ['["highway"~"cycleway"]', '["cycleway"~"lane|opposite_lane|opposite|shared_lane"]']
    custom_filters = ['["bicycle"~"designated"]']
    graphs = [ox.graph_from_place(place, custom_filter=network_filter, retain_all=True) for network_filter in other_cycleways + custom_filters]
    composed_graph = functools.reduce(lambda g1, g2: nx.compose(g1, g2), graphs)
    composed_graph = utils_graph.remove_isolated_nodes(composed_graph)

    sub_graphs = [ox.utils_graph.add_edge_lengths(nx.MultiDiGraph(composed_graph.subgraph(cc))) for cc in nx.weakly_connected_components(composed_graph)]

    largest_subgraph = max(sub_graphs, key=lambda graph: sum([edge[2] for edge in graph.edges(data='length')]))
    return sum([edge[2] for edge in largest_subgraph.edges(data='length')])

#
# def longest_cycleway():
#     other_cycleways = ['["highway"~"cycleway"]', '["cycleway"~"lane|opposite_lane|opposite|shared_lane"]']
#     custom_filters = ['["bicycle"~"designated"]']
#     graphs = [ox.graph_from_place('Kraków, Poland', custom_filter=network_filter, retain_all=True) for network_filter in other_cycleways + custom_filters]
#     composed_graph = functools.reduce(lambda g1, g2: nx.compose(g1, g2), graphs)
#     composed_graph = utils_graph.remove_isolated_nodes(composed_graph)
#
#     sub_graphs = [ox.utils_graph.add_edge_lengths(nx.MultiDiGraph(composed_graph.subgraph(cc))) for cc in nx.weakly_connected_components(composed_graph)]
#
#     largest_subgraph = max(sub_graphs, key=lambda graph: sum([edge[2] for edge in graph.edges(data='length')]))
#     maxes = []
#     for pair in itertools.combinations([x for x in largest_subgraph.nodes() if len(list(largest_subgraph.neighbors(x))) == 1], 2):
#         maxes.append(max(nx.all_simple_paths(largest_subgraph, *pair), key=len))
#         print("done for " + str(pair))
#     print(max(maxes))

all_functions = [
    avg_short_distances_between_hospitals,
    avg_short_distances_between_train_stations_and_city_center,
    longest_cycleway_network,
    how_many_failures_can_network_handle,
    average_how_many_subway_routes_are_there_from_one_stop_to_another
]


# print([timeit(function, "Krakow, Poland") for function in all_functions])
