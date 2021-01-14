def within(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.intersection(polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_idx]
    return possible_matches[possible_matches.intersects(polygon)]


def distance_to_nearest(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, 6))
    possible_matches = gdf.iloc[possible_matches_idx]
    possible_matches = possible_matches[possible_matches.geometry != polygon]
    return _min_dist_df(polygon.centroid, possible_matches)


def _min_dist_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return distances.min()
