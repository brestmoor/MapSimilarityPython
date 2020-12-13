def _min_dist_df(point, df):
    distances = df.apply(lambda row: point.distance(row.geometry.centroid), axis=1)
    return distances.min()


def _within(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.intersection(polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_idx]
    return possible_matches[possible_matches.intersects(polygon)]


def _distance_to_nearest(gdf, polygon):
    possible_matches_idx = list(gdf.sindex.nearest(polygon.bounds, 5))
    possible_matches = gdf.iloc[possible_matches_idx]
    return _min_dist_df(polygon.centroid, possible_matches)
