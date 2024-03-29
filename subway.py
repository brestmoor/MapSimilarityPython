import itertools

import networkx as nx
import numpy as np
import osmnx as ox
from osmnx._errors import EmptyOverpassResponse

from ox_api import graph_from_place_or_rel_id
from util.function_util import timed
from util.graphUtils import find_paths_not_longer_than, path_len, path_len_digraph


@timed
def how_many_failures_can_network_handle(place):
    try:
        G = graph_from_place_or_rel_id(place,
                                retain_all=True, truncate_by_edge=True, buffer_dist=500, simplify=False,
                                custom_filter='["railway"~"subway"][!service]')
    except EmptyOverpassResponse:
        return 0
    if not G or G.empty:
        return None
    ox.distance.add_edge_lengths(G)
    subway_stops = ox.geometries_from_place(place, {'railway': 'stop', 'subway': 'yes'})

    if subway_stops.empty:
        return 0

    lists_of_ids_per_station = subway_stops[subway_stops.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)
    actual_stations = _join_stops_with_same_name(G, lists_of_ids_per_station)

    G = nx.MultiDiGraph(G.subgraph(max(nx.weakly_connected_components(G))))

    Gs = nx.MultiGraph(nx.to_undirected(G.copy()))
    edges = list(Gs.edges())
    for u, v in edges:
        while Gs.has_edge(u, v):
            Gs.remove_edge(u, v)
        Gs.add_edge(u, v)

    _contract_all_nodes_between_stations(Gs, actual_stations)
    Gs = nx.Graph(Gs)
    original_size = len(max(nx.connected_components(Gs)))
    not_failed = 0
    for u, v in nx.edges(Gs):
        Gs.remove_edge(u, v)
        current_max_component_size = len(max(nx.connected_components(Gs)))
        Gs.add_edge(u, v)
        if current_max_component_size == original_size:
            not_failed = not_failed + 1

    return not_failed


@timed
def average_how_many_subway_routes_are_there_from_one_stop_to_another(place):
    try:
        G = graph_from_place_or_rel_id(place,
                                retain_all=True, truncate_by_edge=True, buffer_dist=500, simplify=False,
                                custom_filter='["railway"~"subway"][!service]')
    except EmptyOverpassResponse:
        return 0
    if not G or G.empty:
        return None
    ox.distance.add_edge_lengths(G)
    subway_stops = ox.geometries_from_place(place, {'railway': 'stop', 'subway': 'yes'})

    if subway_stops.empty:
        return 0

    lists_of_ids_per_station = subway_stops[subway_stops.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)
    actual_stations = _join_stops_with_same_name(G, lists_of_ids_per_station)

    G = nx.MultiDiGraph(G.subgraph(max(nx.weakly_connected_components(G))))

    Gs = nx.MultiGraph(nx.to_undirected(G.copy()))
    edges = list(Gs.edges())
    for u, v in edges:
        while Gs.has_edge(u, v):
            Gs.remove_edge(u, v)
        Gs.add_edge(u, v)

    actual_stations = [actual_station for actual_station in actual_stations if actual_station in Gs]
    _contract_all_nodes_between_stations(Gs, actual_stations)
    Gs = nx.Graph(Gs)
    _assign_shortest_path_as_length(Gs, G, actual_stations)
    stations_pairs = list(itertools.combinations(actual_stations, 2))
    number_of_routes = [_number_of_routes_not_longer_than_2_times(Gs, station_pair) for station_pair in stations_pairs]

    return np.mean(number_of_routes)


def _assign_shortest_path_as_length(Gs, G, actual_stations):
    for node in actual_stations:
        for u, v in Gs.edges(node):
            Gs[u][v]['length'] = path_len_digraph(G, nx.shortest_path(G, u, v, 'length'))


def _contract_all_nodes_between_stations(Gs, actual_stations):
    for station_id in actual_stations:
        count = 0
        while station_id in Gs and not set(Gs.neighbors(station_id)).issubset(actual_stations):
            count = count + 1
            neighbors_view = [neighbor for neighbor in Gs.neighbors(station_id)]
            for neighbor in neighbors_view:
                if neighbor not in actual_stations:
                    if Gs.degree(neighbor) < 3:
                        nx.contracted_nodes(Gs, station_id, neighbor, self_loops=False, copy=False)
                    else:
                        for u, v in itertools.combinations(Gs.neighbors(neighbor), 2):
                            if not Gs.has_edge(u, v):
                                Gs.add_edge(u, v)
                        Gs.remove_node(neighbor)


def _join_stops_with_same_name(G, lists_of_ids_per_station):
    actual_stations = []
    for osmids in lists_of_ids_per_station:
        actual_stations.append(osmids[0])
        for osmid in osmids[1:len(osmids)]:
            nx.contracted_nodes(G, osmids[0], osmid, self_loops=False, copy=False)
    return actual_stations


def _number_of_routes_not_longer_than_2_times(G, nodes_pair):
    path = nx.shortest_path(G, *nodes_pair, weight='length')
    shortest_path_len = path_len(G, path)
    shortest_paths_count = len(find_paths_not_longer_than(G, nodes_pair, 3, 1.2 * shortest_path_len))
    return shortest_paths_count

