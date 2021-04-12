import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataPresentation.plotting import plot_points_with_coloring
from pca import calculate_pca


from util.processing import standarize

ruhr = ["Bochum, Germany","Oberhausen, Germany","Gelsenkirchen, Germany","Bottrop, Germany","Hagen, Germany","Hamm, Germany","Herne, Germany","Witten, Germany","Bergkamen, Germany","Hattingen, Germany","Herten, Germany","Recklinghausen, Germany","Moers, Germany","Dorsten, Germany","Dinslaken, Germany","Castrop-Rauxel, Germany","Gladbeck, Germany","Marl, Germany","Mulheim an der Ruhr, Germany",]

df = pd.read_csv("../ruhr_bavaria_joined.csv", index_col=0)
df = df[[
    'pubs_dist_to_nearest',
    'education_buildings_dist_to_nearest',
    'pubs_share',
    'education_buildings_share',
    'shops_share',
    'distance_between_buildings',
    'avg_building_area',
]]


pcaDf = calculate_pca(df)
pcaDf['cluster'] = [True if place in ruhr else False for place in pcaDf.index]

plot_points_with_coloring(pcaDf)

