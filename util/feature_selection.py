import itertools
from operator import itemgetter
import pandas as pd

from similarity import euclidean

test_df = pd.DataFrame(
    [
        [1, 1, 2],
        [2, 1, 1],
        [1, 1, 2],
        [2, 1, 2],
        [1, 1, 2],
        [1, 9, 12],
        [1, 9, 12],
        [1, 9, 12],
        [1, 9, 12],
        [1, 9, 12],
    ]
)


def choose_features(df, groups):
    columns = df.columns

    features_combinations = []
    results = []
    for features_number in range(1, len(columns)):
        features_combinations += itertools.combinations(columns, features_number)
        for features_combination in features_combinations:
            results.append((
                features_combination,
                sum([cluster_variance(df[list(features_combination)], group) for group in groups])))

    return sorted(list(set(results)), key=lambda result: result[1])


def cluster_variance(df, group):
    distances = 0
    external_distances = 0
    for first_city in group:
        for second_city in group:
            if first_city != second_city:
                distances += euclidean(df.loc[first_city], df.loc[second_city]) ** 2
    external_cities = df.drop(group, axis=0).index
    for first_city in group:
        for external_city in external_cities:
            external_distances += euclidean(df.loc[first_city], df.loc[external_city]) ** 2

    return distances - external_distances


# print(choose_features(test_df, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]))
