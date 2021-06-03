from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

from util.processing import preprocess


def pca_without_preprocessing(scores_df, n_components):
    # scores_df = scores_df.drop(['primary_percentage', 'one_way_percentage', 'circuity_avg'], axis = 1)
    # stanarized_as_df = pd.DataFrame(scores_df, index=scores_df.index, columns=scores_df.columns)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scores_df)
    columns = ['PC' + str(num) for num in range(1, n_components + 1)]
    return pd.DataFrame(data=principal_components, index=scores_df.index, columns=columns)


def calculate_pca(df, n_components=2, remove_outliers=True):
    df = preprocess(df, remove_outliers)
    return pca_without_preprocessing(df, n_components)
