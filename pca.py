from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd


def pca(scores_df):
    # scores_df = scores_df.drop(['primary_percentage', 'one_way_percentage', 'circuity_avg'], axis = 1)
    standarized_df = StandardScaler().fit_transform(scores_df)
    stanarized_as_df = pd.DataFrame(standarized_df, index=scores_df.index, columns=scores_df.columns)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(standarized_df)
    return pd.DataFrame(data=principalComponents, index=scores_df.index, columns=['PC1', 'PC2'])
