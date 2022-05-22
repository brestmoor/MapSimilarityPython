from sklearn.decomposition import PCA
import pandas as pd

from util.processing import preprocess


def pca_without_preprocessing(scores_df, n_components):
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scores_df)
    columns = ['PC' + str(num) for num in range(1, n_components + 1)]
    return pd.DataFrame(data=principal_components, index=scores_df.index, columns=columns)


def calculate_pca(df, n_components=2, remove_outliers=True):
    df = preprocess(df, remove_outliers)
    if df.empty:
        return df
    if len(df) < n_components:
        raise Exception("Number of rows must be bigger then " + str(n_components))
    return pca_without_preprocessing(df, n_components)
