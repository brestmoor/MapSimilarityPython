import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataPresentation.plotting import plot_points_with_coloring
from pca import calculate_pca


from util.processing import standarize

italy_north = ["Lecco, Italy", "Valmadrera, Italy", "Nembro, Italy", "Albino, Italy", "Alzano Lombardo, Italy", "Clusone, Italy", "Pergine Valsugana, Italy", "Trento, Italy", "Borgo Valsugana, Italy", "Feltre, Italy", "Maniago, Italy", "San Daniele del Friuli, Italy", "Udine, Italy", "Pordenone, Italy", "Oderzo, Italy", "Treviso, Italy", "Brescia, Italy", "Rezzato, Italy", "Cremona, Italy", "Mantova, Italy", "Asti, Italy", "Alessandria, Italy", "Pavia, Italy", "Lodi, Italy", "Biella, Italy", "Vercelli, Italy", "Novara, Italy", "Varese, Italy", "Como, Italy", "Mondovi, Italy", "Fossano, Italy", "Piacenza, Italy",]

df = pd.read_csv("../italy_north_south.csv", index_col=0)
df = df[[
    'average_street_length',
    'share_of_separated_streets',
    'streets_in_radius_of_100_m',
    'streets_per_node_avg',

    # 'share_of_buildings_near_center',
    # 'circuity_avg'
]]

df = df.dropna()
pcaDf = calculate_pca(df)
pcaDf['cluster'] = [True if place in italy_north else False for place in pcaDf.index]

plot_points_with_coloring(pcaDf)

