import pandas as pd
from scipy import stats
import numpy as np
from sklearn.preprocessing import StandardScaler


def normalize_series(first, second):
    first_normalized = []
    second_normalized = []

    for x, y in zip(first, second):
        max_value = max(x, y)
        first_normalized.append(max_value if max_value == 0 else normalize(x, max_value))
        second_normalized.append(max_value if max_value == 0 else normalize(y, max_value))

    return pd.Series(first_normalized), pd.Series(second_normalized)


def normalize(x, x_max):
    return x / x_max


def remove_outliers(df):
    return df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]


def standarize(df):
    standarized_matrix = StandardScaler().fit_transform(df)
    return pd.DataFrame(standarized_matrix, index=df.index, columns=df.columns)
