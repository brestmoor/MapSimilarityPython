import osmnx as ox


def graph_from_place(place, network_type, custom_filter, simplify=True):
    try:
        return ox.graph_from_place(place, network_type=network_type, custom_filter=custom_filter, simplify=simplify)
    except Exception as e:
        print(str(e) + ' for: ' + place + ',' + custom_filter)