import itertools
import networkx as nx
import osmnx as ox


def sum_edge_attribute(G, route, attribute='length'):
    route_sum = 0
    for u, v in zip(route[:-1], route[1:]):
        if 'length' in G[u][v]:
            route_sum = route_sum + G[u][v][attribute]
        else:
            route_sum = min(G.get_edge_data(u, v).values(), key=lambda x: x[attribute])['attribute']

    return route_sum


def k_shortest_paths(G, orig, dest, k, weight="length"):
    paths_gen = nx.shortest_simple_paths(G, orig, dest, weight)
    for path in itertools.islice(paths_gen, 0, k):
        yield path


def _find_paths_not_longer_than(G, nodes_pair, init_number_of_paths_to_check, length_limit):
    other_paths = [other_path for other_path in k_shortest_paths(G, *nodes_pair, init_number_of_paths_to_check) if
                   _path_len(G, other_path) < length_limit]
    if len(other_paths) == init_number_of_paths_to_check:
        return _find_paths_not_longer_than(G, nodes_pair, init_number_of_paths_to_check + 2, length_limit)
    else:
        return other_paths


def _find_paths_not_longer_than_non_rec(G, nodes_pair, length_limit):
    counter = 0
    for path in nx.shortest_simple_paths(G, *nodes_pair, 'length'):
        if _path_len(G, path) < length_limit:
            counter = counter + 1
        else:
            return counter
    return counter



def _path_len_digraph(G, path):
    return sum(ox.utils_graph.get_route_edge_attributes(G, path, 'length'))


def _path_len(G, path):
    return sum_edge_attribute(G, path)

def get_biggest_SCC(G):
    return max(nx.strongly_connected_components(G))