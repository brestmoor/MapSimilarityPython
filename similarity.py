from scipy import stats
import numpy as np
import pandas as pd
from scipy import spatial


def positive_pearson(x, y):
    pearson_result = pearson(x, y)
    return pearson_result if pearson_result > 0 else 0


def pearson(x, y):
    return stats.pearsonr(x, y)[0]


def cosine(x, y):
    return 1 - spatial.distance.cosine(x, y)


def similarity(scores_df):
    cities = scores_df.columns
    size = len(cities)
    similarity_matrix = np.empty((size, size))

    for first_idx, first_city in enumerate(cities):
        for second_idx, second_city in enumerate(cities):
            similarity_matrix[first_idx][second_idx] = pearson(scores_df[first_city], scores_df[second_city])

    similarity_df = pd.DataFrame(similarity_matrix, index=[cities], columns=[cities])
    return similarity_df


# frame = pd.DataFrame({'a': [1, 100, 8, 100], 'b': [10, 50, 8, 10]})
# print(similarity(frame))
