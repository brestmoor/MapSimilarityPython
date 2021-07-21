import math

from pyproj import Proj, transform
from shapely.geometry import Point


def within(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.intersection(polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_idx]
    return possible_matches[possible_matches.intersects(polygon)]


def distance_to_nearest(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, 6))
    possible_matches = gdf.iloc[possible_matches_idx]
    possible_matches = possible_matches[possible_matches.geometry.convex_hull != polygon.convex_hull]
    return _min_dist_df(polygon.centroid, possible_matches)


def distances_to_multiple_nearest(gdf, polygon, neignours_count):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, neignours_count + 5))
    possible_matches = gdf.iloc[possible_matches_idx]
    possible_matches = possible_matches[possible_matches.geometry.convex_hull != polygon.convex_hull]
    if possible_matches.empty:
        return None
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


def circle_radius(p1, p2, p3):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]

    a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2

    b = (x1 * x1 + y1 * y1) * (y3 - y2) + (x2 * x2 + y2 * y2) * (y1 - y3) + (x3 * x3 + y3 * y3) * (y2 - y1)

    c = (x1 * x1 + y1 * y1) * (x2 - x3) + (x2 * x2 + y2 * y2) * (x3 - x1) + (x3 * x3 + y3 * y3) * (x1 - x2)

    try:
        x = -b / (2 * a)
        y = -c / (2 * a)
        return math.hypot(x - x1, y - y1)
    except ZeroDivisionError:
        return None




