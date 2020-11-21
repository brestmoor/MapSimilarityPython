import osmnx as ox
import geopandas as gpd
from osmnx import utils_graph
from shapely.geometry import Polygon
from timeit import default_timer as timer

from functions import timeit
from osmApi import get_ways_in_relation
import numpy as np
import itertools as itertools
import osmApi as api
import networkx as nx
import functools

ox.config(log_console=True, use_cache=True)


def _to_coordindates(shape):
    return (shape.y, shape.x)


def avg_short_distances_between_hospitals():
    network_graph = ox.graph_from_place('Rzeszów, Poland', network_type='drive')

    hospitals = ox.pois_from_place('Rzeszów, Poland', {'amenity': 'hospital'})
    hospitals_centroids = hospitals.geometry.centroid
    centroids_as_tuples = [_to_coordindates(centroid) for centroid in hospitals_centroids]
    hospital_nodes = [ox.get_nearest_node(network_graph, coords_tuple) for coords_tuple in centroids_as_tuples]
    hospital_pairs = list(itertools.combinations(hospital_nodes, 2))
    shortest_paths = [ox.shortest_path(network_graph, *pair) for pair in hospital_pairs]
    sums = [sum(ox.utils_graph.get_route_edge_attributes(network_graph, path, 'length')) for path in shortest_paths]
    return np.mean(sums)


def avg_short_distances_between_train_stations_and_city_center():
    network_graph = ox.graph_from_place('Rzeszów, Poland', network_type='drive')

    train_stations_centroids = ox.pois_from_place('Rzeszów, Poland', {'railway': 'station'}).geometry.centroid
    centroids_as_tuples = [_to_coordindates(centroid) for centroid in train_stations_centroids]
    train_station_nodes = [ox.get_nearest_node(network_graph, coords_tuple) for coords_tuple in centroids_as_tuples]

    city_center_node = ox.get_nearest_node(network_graph, api.get_city_center("Rzeszów, Poland"))

    pairs = [(city_center_node, train_station_node) for train_station_node in train_station_nodes]
    shortest_paths = [ox.shortest_path(network_graph, *pair) for pair in pairs]
    sums = [sum(ox.utils_graph.get_route_edge_attributes(network_graph, path, 'length')) for path in shortest_paths]
    return np.mean(sums)


def longest_cycleway_network():
    other_cycleways = ['["highway"~"cycleway"]', '["cycleway"~"lane|opposite_lane|opposite|shared_lane"]']
    custom_filters = ['["bicycle"~"designated"]']
    graphs = [ox.graph_from_place('Kraków, Poland', custom_filter=network_filter, retain_all=True) for network_filter in other_cycleways + custom_filters]
    composed_graph = functools.reduce(lambda g1, g2: nx.compose(g1, g2), graphs)
    composed_graph = utils_graph.remove_isolated_nodes(composed_graph)

    sub_graphs = [ox.utils_graph.add_edge_lengths(nx.MultiDiGraph(composed_graph.subgraph(cc))) for cc in nx.weakly_connected_components(composed_graph)]

    largest_subgraph = max(sub_graphs, key=lambda graph: sum([edge[2] for edge in graph.edges(data='length')]))
    return sum([edge[2] for edge in largest_subgraph.edges(data='length')])


def average_how_many_subway_routes_are_there_from_one_stop_to_another():
    G = ox.graph_from_place('Warszawa, Poland',
                            retain_all=True, truncate_by_edge=True, simplify=False,
                            custom_filter='["railway"~"subway"][!service]')
    ox.utils_graph.add_edge_lengths(G)
    subway_stations = ox.pois_from_place('Warszawa, Poland', {'railway': 'stop'})
    stops = [n for n in G.nodes if n in list(subway_stations.osmid)]

    lists = subway_stations[subway_stations.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)

    actual_stations = []
    for osmids in lists:
        actual_stations.append(osmids[0])
        for osmid in osmids[1:len(osmids)]:
            nx.contracted_nodes(G, osmids[0], osmid, self_loops=False, copy=False)

    Gs = G.copy()

    for station_id in actual_stations:
        count = 0
        while not set(Gs.neighbors(station_id)).issubset(actual_stations):
            count = count + 1
            neighbors_view = [neighbor for neighbor in Gs.neighbors(station_id)]
            for neighbor in neighbors_view:
                if neighbor not in actual_stations:
                    nx.contracted_nodes(Gs, station_id, neighbor, self_loops=False, copy=False)
            print('contracting for station ' + str(station_id) + ' iter: ' + str(count))

    Gs = nx.Graph(nx.to_undirected(Gs))

    for node in Gs.nodes:
        for edge in Gs.edges(node):
            Gs[edge[0]][edge[1]]['length'] = _path_len(G, nx.shortest_path(G, *edge, 'length'))

    stations_pairs = list(itertools.combinations(actual_stations, 2))

    number_of_routes = [_number_of_routes_not_longer_than_2_times(Gs, station_pair) for station_pair in stations_pairs]

    print(number_of_routes)



def _number_of_routes_not_longer_than_2_times(G, nodes_pair):
    path = nx.shortest_path(G, *nodes_pair, weight='length')
    shortest_path_len = _path_len(G, path)
    shortest_paths = _find_paths_not_longer_than(G, nodes_pair, 3, 1.2 * shortest_path_len)
    return len(shortest_paths)


def _find_paths_not_longer_than(G, nodes_pair, init_number_of_paths_to_check, length_limit):
    other_paths = [other_path for other_path in ox.k_shortest_paths(G, *nodes_pair, init_number_of_paths_to_check) if
                   _path_len(G, other_path) < length_limit]
    if len(other_paths) == init_number_of_paths_to_check:
        return _find_paths_not_longer_than(G, nodes_pair, init_number_of_paths_to_check + 2, length_limit)
    else:
        return other_paths


def _path_len(G, path):
    return sum(ox.utils_graph.get_route_edge_attributes(G, path, 'length'))


def longest_cycleway():
    other_cycleways = ['["highway"~"cycleway"]', '["cycleway"~"lane|opposite_lane|opposite|shared_lane"]']
    custom_filters = ['["bicycle"~"designated"]']
    graphs = [ox.graph_from_place('Kraków, Poland', custom_filter=network_filter, retain_all=True) for network_filter in other_cycleways + custom_filters]
    composed_graph = functools.reduce(lambda g1, g2: nx.compose(g1, g2), graphs)
    composed_graph = utils_graph.remove_isolated_nodes(composed_graph)

    sub_graphs = [ox.utils_graph.add_edge_lengths(nx.MultiDiGraph(composed_graph.subgraph(cc))) for cc in nx.weakly_connected_components(composed_graph)]

    largest_subgraph = max(sub_graphs, key=lambda graph: sum([edge[2] for edge in graph.edges(data='length')]))
    maxes = []
    for pair in itertools.combinations([x for x in largest_subgraph.nodes() if len(list(largest_subgraph.neighbors(x))) == 1], 2):
        maxes.append(max(nx.all_simple_paths(largest_subgraph, *pair), key=len))
        print("done for " + str(pair))
    print(max(maxes))


print(average_how_many_subway_routes_are_there_from_one_stop_to_another())
