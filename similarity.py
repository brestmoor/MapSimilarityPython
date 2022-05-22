import itertools

from scipy import stats
import numpy as np
import pandas as pd
from scipy import spatial
from sklearn.preprocessing import MinMaxScaler



def pearson(x, y):
    return stats.pearsonr(x, y)[0]


def cosine(x, y):
    return 1 - spatial.distance.cosine(x, y)

def euclidean_distance(x, y):
    return spatial.distance.euclidean(x, y)

def euclidean_similarity(x, y):
    dimension = len(x)
    max_distance_after_min_max_scaling = dimension**(1/2)
    return 1 - spatial.distance.euclidean(x, y) / max_distance_after_min_max_scaling


def angular_similarity(x, y):
    return 1 - np.arccos(cosine(x, y)) / np.pi


def scale_min_max(df):
    scaler = MinMaxScaler()
    df[df.columns] = scaler.fit_transform(df)
    return df

def calculate_similarity(scores_df_input, method='euclidean'):
    scores_df = scores_df_input.copy()
    cities = scores_df.index
    size = len(cities)
    similarity_matrix = np.empty((size, size))

    scores_df = scale_min_max(scores_df)

    method_func = pearson if method == 'pearson' else euclidean_similarity

    for first_idx, first_city in enumerate(cities):
        for second_idx, second_city in enumerate(cities):
            similarity_matrix[first_idx][second_idx] = method_func(scores_df.loc[first_city], scores_df.loc[second_city])

    similarity_df = pd.DataFrame(similarity_matrix, index=cities, columns=cities)
    return similarity_df

def silhouette_score(first_df, second_df):
    method_fn = euclidean_distance

    first_intra_cluster_distances = first_df.apply(lambda calc_row: first_df.drop([calc_row.name]).apply(lambda row: method_fn(calc_row, row), axis=1).mean(), axis=1)
    first_nearest_cluster_distances = first_df.apply(lambda calc_row: second_df.apply(lambda row: method_fn(calc_row, row), axis=1).mean(), axis=1)

    second_intra_cluster_distances = second_df.apply(lambda calc_row: second_df.drop([calc_row.name]).apply(lambda row: method_fn(calc_row, row), axis=1).mean(), axis=1)
    second_nearest_cluster_distances = second_df.apply(lambda calc_row: first_df.apply(lambda row: method_fn(calc_row, row), axis=1).mean(), axis=1)


    first_samples_scores = (first_nearest_cluster_distances - first_intra_cluster_distances) / np.maximum(first_nearest_cluster_distances, first_intra_cluster_distances)
    second_samples_scores = (second_nearest_cluster_distances - second_intra_cluster_distances) / np.maximum(second_nearest_cluster_distances, second_intra_cluster_distances)

    return pd.concat([first_samples_scores, second_samples_scores]).mean()

def silhouette_score_series(first_df, second_df):
    method_fn = euclidean_distance

    first_intra_cluster_distances = first_df.apply(lambda calc_row: first_df.drop([calc_row.name]).apply(lambda row: method_fn(calc_row, row)).mean())
    first_nearest_cluster_distances = first_df.apply(lambda calc_row: second_df.apply(lambda row: method_fn(calc_row, row)).mean())

    second_intra_cluster_distances = second_df.apply(lambda calc_row: second_df.drop([calc_row.name]).apply(lambda row: method_fn(calc_row, row)).mean())
    second_nearest_cluster_distances = second_df.apply(lambda calc_row: first_df.apply(lambda row: method_fn(calc_row, row)).mean())


    first_samples_scores = (first_nearest_cluster_distances - first_intra_cluster_distances) / np.maximum(first_nearest_cluster_distances, first_intra_cluster_distances)
    second_samples_scores = (second_nearest_cluster_distances - second_intra_cluster_distances) / np.maximum(second_nearest_cluster_distances, second_intra_cluster_distances)

    return pd.concat([first_samples_scores, second_samples_scores]).mean()


def find_columns_with_best_silhouette_score(first_df, second_df, number_of_columns):
    if list(first_df.columns) != list(second_df.columns):
        raise Exception()
    if len(first_df.columns) > 15:
        print('Too many columns')
        raise Exception('Too many columns')

    columns = first_df.columns
    combinations = []
    max_score = -1
    max_combination = None
    no_of_columns = min(len(columns), number_of_columns)
    combinations = list(itertools.combinations(columns, no_of_columns))
    print("Searching. Combinations:" + str(len(combinations)))
    for combination in combinations:
        score = silhouette_score(first_df[list(combination)], second_df[list(combination)])
        if score > max_score:
            max_score = score
            max_combination = combination
    return max_combination, max_score


def find_individual_columns_with_best_silhouette_score(first_df, second_df, number_of_columns=2):
    if list(first_df.columns) != list(second_df.columns):
        raise Exception()

    columns = first_df.columns
    scores = []
    for column in columns:
        scores.append((silhouette_score(first_df[column].to_frame(0), second_df[column].to_frame(0)), column))
    scores.sort(key=lambda el: el[0])
    scores.reverse()
    return scores[:number_of_columns]


first_df = pd.DataFrame(
    {'a': [1, 1, 1, 1],
     'b': [2, 2, 2, 2],
     'c': [1, 1, 1, 1]}
)
second_df = pd.DataFrame(
        {'a': [6, 6, 6, 6],
         'b': [5, 5, 5, 4],
         'c': [6, 6, 6, 5]}
    )


def calculate_similarity_to_ndarray(scores_df):
    similarity = calculate_similarity(scores_df)
    return similarity.to_numpy(), similarity.index;