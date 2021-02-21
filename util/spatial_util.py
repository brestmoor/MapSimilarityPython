from pyproj import Proj, transform
from shapely.geometry import Point


def within(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.intersection(polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_idx]
    return possible_matches[possible_matches.intersects(polygon)]


def distance_to_nearest(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, 6))
    possible_matches = gdf.iloc[possible_matches_idx]
    possible_matches = possible_matches[possible_matches.geometry != polygon]
    return _min_dist_df(polygon.centroid, possible_matches)


def distances_to_multiple_nearest(gdf, polygon, neignours_count):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, neignours_count + 5))
    possible_matches = gdf.iloc[possible_matches_idx]
    possible_matches = possible_matches[possible_matches.geometry != polygon]
    possible_matches['dist_to_polygon'] = possible_matches.apply(
        lambda row: polygon.centroid.distance(row.geometry.centroid), axis=1)
    return list(possible_matches.sort_values('dist_to_polygon')[:neignours_count]['dist_to_polygon'])


def convert_crs(point, out_crs):
    in_proj = Proj('epsg:4326')
    out_proj = Proj(out_crs)
    x1, y1 = list(point.coords[0])
    x2, y2 = transform(in_proj, out_proj, x1, y1, always_xy=True)
    return Point(x2, y2)


def _min_dist_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return distances.min()


def simplify_bearing(bearing):
    return bearing if bearing < 180 else bearing - 180
