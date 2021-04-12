import pandas as pd
from osmnx.plot import _get_colors_by_value

from dataPresentation.plotting import plot_points_with_coloring, plot_points_1_dim_with_coloring
from pca import calculate_pca

north = ["Chlopy, Zachodniopomorskie, Poland", "Uniescie, Zachodniopomorskie, Poland", "Miedzyzdroje, Zachodniopomorskie, Poland", "Dziwnow, Zachodniopomorskie, Poland", "Kolobrzeg, Zachodniopomorskie, Poland", "Mielno, Zachodniopomorskie, Poland", "Darlowo, Zachodniopomorskie, Poland", "Grzybowo, Zachodniopomorskie, Poland", "Kamien Pomorski, Zachodniopomorskie,  Poland", "Gaski, Zachodniopomorskie, Poland", "Sarbinowo, Zachodniopomorskie, Poland", "Ustka, Pomorskie, Poland", "Rowy, Pomorskie, Poland", "Leba, Pomorskie, Poland", "Puck, Pomorskie, Poland", "Jastarnia, Pomorskie, Poland", "Karwia, Pomorskie, Poland", "Krynica Morska, Pomorskie Poland", "Karwia, Pomorskie, Poland", "Jastrzebia Gora, Pomorskie, Poland", "Chlapowo, Pomorskie, Poland", "Hel, Pomorskie, Poland"]

df = pd.read_csv("../poland_north_south_with_boundaries_de.csv", index_col=0)
df = df[[
    'intersection_density_km',
    'street_density_km',
    'average_dist_to_any_public_transport_stop',
    'average_street_length',
    'circuity_avg',
    'avg_distance_to_5_buildings'
]]

# df = df.dropna()
pcaDf = calculate_pca(df, 1)
pcaDf['cluster'] = [True if place in north else False for place in pcaDf.index]

# pcaDf['colors'] = _get_colors_by_value(pcaDf['PC1'], None, 'cividis', 0, 1, "none", False)

plot_points_1_dim_with_coloring(pcaDf, palette='winter')

