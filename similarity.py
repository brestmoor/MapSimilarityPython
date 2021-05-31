from scipy import stats
import numpy as np
import pandas as pd
from scipy import spatial
from sklearn.preprocessing import MinMaxScaler

from util.processing import normalize_series


def positive_pearson(x, y):
    pearson_result = pearson(x, y)
    return pearson_result if pearson_result > 0 else 0


def pearson(x, y):
    return stats.pearsonr(x, y)[0]


def cosine(x, y):
    return 1 - spatial.distance.cosine(x, y)

def simple_euclidean(x, y):
    return spatial.distance.euclidean(x, y)

def euclidean(x, y):
    dimension = len(x)
    max_distance = dimension**(1/2)
    return 1 - spatial.distance.euclidean(x, y) / max_distance


def angular_similarity(x, y):
    return 1 - np.arccos(cosine(x, y)) / np.pi

# krak_wroc = pd.DataFrame({'Krakow': [221.947849, 0.375124, 0.152036, 0.128238], 'Wroclaw': [234.532927, 0.011988, 0.283432, 0.166200]})


def calculate_similarity(scores_df_input):
    scores_df = scores_df_input.copy()
    cities = scores_df.index
    size = len(cities)
    similarity_matrix = np.empty((size, size))

    scaler = MinMaxScaler()
    scores_df[scores_df.columns] = scaler.fit_transform(scores_df)

    for first_idx, first_city in enumerate(cities):
        for second_idx, second_city in enumerate(cities):
            similarity_matrix[first_idx][second_idx] = euclidean(
                scores_df.loc[first_city], scores_df.loc[second_city]
                # *normalize_series(scores_df.loc[first_city], scores_df.loc[second_city])
            )

    similarity_df = pd.DataFrame(similarity_matrix, index=cities, columns=cities)
    return similarity_df

def calculate_similarity_to_ndarray(scores_df):
    similarity = calculate_similarity(scores_df)
    return similarity.to_numpy(), similarity.index;