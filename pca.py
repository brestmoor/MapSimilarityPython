from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

from util.processing import preprocess


def pca_without_preprocessing(scores_df):
    # scores_df = scores_df.drop(['primary_percentage', 'one_way_percentage', 'circuity_avg'], axis = 1)
    # stanarized_as_df = pd.DataFrame(scores_df, index=scores_df.index, columns=scores_df.columns)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scores_df)
    return pd.DataFrame(data=principal_components, index=scores_df.index, columns=['PC1', 'PC2'])


def calculate_pca(df):
    df = preprocess(df)
    return pca_without_preprocessing(df)
