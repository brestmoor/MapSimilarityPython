import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
from osmnx.plot import _get_colors_by_value

from coloringSimilarity.draw_boundary import display_similarity_on_map, display_similarity_on_map2
from pca import calculate_pca

plt.rcParams["figure.dpi"] = 500
ox.config(log_console=False, use_cache=True)

names = ['Ustron, Poland', 'Wisla, Poland', 'Szczyrk, Poland', 'Wegierska Gorka, Poland', 'Zywiec, Poland','Zawoja, Poland', 'Sucha Beskidzka, Poland', 'Spytkowice, Poland', 'Rabka-Zdroj, Poland', 'Nowy Targ, Poland','Bialka Tatrzanska, Poland', 'Bukowina Tatrzanska, Poland', 'Kluszkowce, Poland', 'Szczawnica, Poland','Piwniczna-Zdroj, Poland', 'Kasina Wielka, Poland', 'Limanowa, Poland', 'Szaflary, Poland','Ludzmierz, Poland', 'Chlopy, Zachodniopomorskie, Poland', 'Uniescie, Zachodniopomorskie, Poland','Miedzyzdroje, Zachodniopomorskie, Poland', 'Dziwnow, Zachodniopomorskie, Poland','Kolobrzeg, Zachodniopomorskie, Poland', 'Mielno, Zachodniopomorskie, Poland','Darlowo, Zachodniopomorskie, Poland', 'Grzybowo, Zachodniopomorskie, Poland','Kamien Pomorski, Zachodniopomorskie,  Poland', 'Gaski, Zachodniopomorskie, Poland','Sarbinowo, Zachodniopomorskie, Poland', 'Ustka, Pomorskie, Poland', 'Rowy, Pomorskie, Poland','Leba, Pomorskie, Poland', 'Puck, Pomorskie, Poland', 'Jastarnia, Pomorskie, Poland','Karwia, Pomorskie, Poland', 'Karwia, Pomorskie, Poland', 'Jastrzebia Gora, Pomorskie, Poland','Chlapowo, Pomorskie, Poland', 'Hel, Pomorskie, Poland']
countries = ["Poland"]

df = pd.read_csv("../poland_north_south_with_boundaries_de.csv", index_col=0)
df = df[[
    'intersection_density_km',
    'street_density_km',
    'average_dist_to_any_public_transport_stop',
    'average_street_length',
    'circuity_avg',
    'avg_distance_to_5_buildings'
]]
df = df[~df.index.duplicated()]

pca = calculate_pca(df, n_components=1)

display_similarity_on_map2(pca['PC1'], countries, "Poland", linewidth=0.2, scale_cities=2, cmap='cool')
plt.show()
