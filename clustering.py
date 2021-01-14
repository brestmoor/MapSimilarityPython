from sklearn.cluster import KMeans
import pandas as pd


def k_means(df):
    kmeans = KMeans(init="random", n_clusters=2, n_init=10, max_iter=300, random_state=42)
    kmeans.fit(df)
    return pd.Series(kmeans.labels_, index=df.index)


k_means(pd.read_csv("old_and_industrial_buildings.csv", index_col=0))
