from scipy import stats
import numpy as np
import pandas as pd
from scipy import spatial

from processing import normalize_series


def positive_pearson(x, y):
    pearson_result = pearson(x, y)
    return pearson_result if pearson_result > 0 else 0


def pearson(x, y):
    return stats.pearsonr(x, y)[0]


def cosine(x, y):
    return 1 - spatial.distance.cosine(x, y)


def angular_similarity(x, y):
    return 1 - np.arccos(cosine(x, y)) / np.pi

# krak_wroc = pd.DataFrame({'Krakow': [221.947849, 0.375124, 0.152036, 0.128238], 'Wroclaw': [234.532927, 0.011988, 0.283432, 0.166200]})


def similarity(scores_df):
    cities = scores_df.columns
    size = len(cities)
    similarity_matrix = np.empty((size, size))

    for first_idx, first_city in enumerate(cities):
        for second_idx, second_city in enumerate(cities):
            similarity_matrix[first_idx][second_idx] = angular_similarity(
                *normalize_series(scores_df[first_city], scores_df[second_city]))

    similarity_df = pd.DataFrame(similarity_matrix, index=cities, columns=cities)
    return similarity_df


# frame = pd.DataFrame({'a': [1, 100000, 8, 100], 'b': [10, 50000, 8, 10]})
# print(similarity(krak_wroc))

# print(pearson([6, 8, 11, 16, 4, 14, 15, 9, 19, 1, 3, 2, 20, 10, 5, 7, 12, 17, 18, 13], [
#             47, 11, 32, 6, 13, 18, 1, 17, 37, 14, 20, 24, 19, 7, 30, 39, 28, 4, 35, 46]))
#
# print(similarity(pd.DataFrame({
#     'first': [6, 8, 11, 16, 4, 14, 15, 9, 19, 1, 3, 2, 20, 10, 5, 7, 12, 17, 18, 13],
#     'second': [47, 11, 32, 6, 13, 18, 1, 17, 37, 14, 20, 24, 19, 7, 30, 39, 28, 4, 35, 46]
# })))
