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
    df_to_remove_outliers = df.loc[:, (df != 0).any(axis=0)]
    return df[(np.abs(stats.zscore(df_to_remove_outliers)) < 3).all(axis=1)]


def standarize(df):
    standarized_matrix = StandardScaler().fit_transform(df)
    return pd.DataFrame(standarized_matrix, index=df.index, columns=df.columns)


def preprocess(df, should_remove_outliers=True):
    df = df.dropna()
    if df.empty:
        print('Df empty after Nan removal')
        return df

    df_outlier_removed = remove_outliers(df) if should_remove_outliers else df

    if df_outlier_removed.empty:
        print('Df empty after outliers removal')
        return df
    else:
        return standarize(df_outlier_removed)