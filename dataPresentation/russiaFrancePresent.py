import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataPresentation.plotting import plot_points_with_coloring, plot_points_1_dim_with_coloring
from pca import calculate_pca


from util.processing import standarize, remove_outliers

russia = ["Smolensk, Russia", "Bryansk, Russia", "Kaluga, Russia", "Tula, Russia", "Ryazan, Russia", "Serpunkhov, Russia", "Obninsk, Russia", "Kolomna, Russia", "Ryazan, Russia", "Tver, Russia", "Voronezh, Russia", "Stary Oskol, Russia", "Belgorod, Russia", "Yaroslavl, Russia", "Ivanovo, Russia", "Pskov, Russia", "Veliky Novgorod, Russia", "Volgograd, Russia", "Saratov, Russia", "Engels, Russia", "Balakovo, Russia", "Penza, Russia", "Cheboksary, Russia", "Novocheboksarsk, Russia", "Yoshkar-Ola, Russia", "Vladimir, Russia", "Ulyanovsk, Russia", "Dimitrovgrad, Russia", "Ufa, Russia", "Orenburg, Russia",]

df = pd.read_csv("../russia_france_all.csv", index_col=0)
# df = pd.read_csv("../russia_france_city_facilities.csv", index_col=0)
df = df[[
    'intersection_density_km',
    'street_density_km',
    'pubs_dist_to_nearest',
    'all_railways_to_highway',
    # 'cycleways_to_highways',
    'avg_dist_from_building_to_center',
    'average_dist_to_park',
    'average_street_length',
    # 'share_of_separated_streets'
    'streets_in_radius_of_100_m',
    'distance_between_buildings',
    'avg_building_area',
    'circuity_between_crossroads'
]]

# city_facilities
# df1 = df[['cycleways_to_highways', 'average_dist_to_park', 'crossing_share', 'police_building_share', 'fire_stations_share', 'hospitals_share']]

# streets
df2 = df[['intersection_density_km', 'street_density_km', 'average_street_length', 'streets_in_radius_of_100_m']]

# railways
df3 = df[['all_railways_to_highway']]

# buildings
df4 = df[['avg_dist_from_building_to_center', 'distance_between_buildings', 'avg_building_area']]

df = df.dropna()

pcaDf = calculate_pca(df)
pcaDf['cluster'] = [True if place in russia else False for place in pcaDf.index]

plot_points_with_coloring(pcaDf)

plot_points_1_dim_with_coloring(pcaDf, palette='cool')