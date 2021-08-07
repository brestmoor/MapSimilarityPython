import osmnx as ox


def graph_from_place_or_rel_id(place, network_type='all_private', truncate_by_edge=False, buffer_dist=None,
                               custom_filter=None, simplify=True, retain_all=False):
    try:
        if place.isnumeric():
            return _graph_by_rel_id(place, network_type, custom_filter, simplify, retain_all=retain_all)
        else:
            return ox.graph_from_place(place, network_type=network_type, truncate_by_edge=truncate_by_edge,
                                       buffer_dist=buffer_dist, custom_filter=custom_filter, simplify=simplify)
    except Exception as e:
        print(str(e) + ' for: ' + place + ',' + custom_filter)


def geometries_from_place_or_rel_id(place, tags, buffer_dist=None):
    try:
        if place.isnumeric():
            return _geometries_by_rel_id(place, tags, buffer_dist)
        else:
            return ox.geometries_from_place(place, tags=tags, buffer_dist=buffer_dist)
    except Exception as e:
        print(str(e) + ' for: ' + place)


def geocode_to_gdf_by_place_or_rel_id(place):
    try:
        if isinstance(place, list) and all([text.isnumeric() for text in place]):
            return ox.geocode_to_gdf(['R' + place for place in place], by_osmid=True)
        if isinstance(place, list):
            return ox.geocode_to_gdf(place)
        if place.isnumeric():
            return ox.geocode_to_gdf('R' + place, by_osmid=True)
        else:
            return ox.geocode_to_gdf(place)
    except Exception as e:
        print(str(e) + ' for: ' + str(place))


def _graph_by_rel_id(rel_id, network_type, custom_filter, simplify, retain_all):
    gdf = ox.geocode_to_gdf('R' + rel_id, by_osmid=True)
    geometry = gdf.iloc[0].geometry
    return ox.graph_from_polygon(geometry, network_type=network_type, simplify=simplify,
                                 custom_filter=custom_filter, retain_all=retain_all)


def _geometries_by_rel_id(rel_id, tags, buffer):
    gdf = ox.geocode_to_gdf('R' + rel_id, by_osmid=True, buffer_dist=buffer)
    return ox.geometries_from_polygon(gdf.iloc[0].geometry, tags=tags)

