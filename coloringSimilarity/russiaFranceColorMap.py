import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
from osmnx.plot import _get_colors_by_value

from coloringSimilarity.draw_boundary import display_similarity_on_map2
from pca import calculate_pca
ox.config(log_console=False, timeout=300,
          use_cache=True,
          overpass_endpoint='http://localhost:12346/api',
          overpass_rate_limit=False, max_query_area_size = 2 * 1000 * 50 * 100)

plt.rcParams["figure.dpi"] = 5000

countries = ["Metropolitan France"]

df = pd.read_csv("../out_new/russia_france_new.csv", index_col=0)
# df = df[[
#     'intersection_density_km',
#     'street_density_km',
#     'pubs_dist_to_nearest',
#     'all_railways_to_highway',
#     # 'cycleways_to_highways',
#     'avg_dist_from_building_to_center',
#     'average_dist_to_park',
#     'average_street_length',
#     # 'share_of_separated_streets'
#     'streets_in_radius_of_100_m',
#     'distance_between_buildings',
#     'avg_building_area',
#     'circuity_between_crossroads'
# ]]

df = df[['average_street_length', 'intersection_density_km', 'streets_in_radius_of_100_m']]
df = df[~df.index.duplicated()]

pca = calculate_pca(df, n_components=1)

display_similarity_on_map2(pca, ["Metropolitan France", "Russia"], 3857, linewidth=0.02, scale_cities=4, cmap='cool')
plt.savefig("../coloredMaps/russia_france_streets.png")
