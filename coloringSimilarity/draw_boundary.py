import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import pyproj
from osmnx.plot import _get_colors_by_value

from pca import calculate_pca

# plt.rcParams["figure.dpi"] = 4000
ox.config(log_console=False, use_cache=True)


def display_similarity_on_map(pca_for_countries, crs_reference):
    ax = None
    for key in pca_for_countries:
        crs_reference_gdf = ox.project_gdf(ox.geocode_to_gdf(crs_reference))
        pca = pca_for_countries[key]
        country = ox.project_gdf(ox.geocode_to_gdf(key))
        cities = ox.project_gdf(ox.geocode_to_gdf(list(pca.index)), country.crs)

        cities = _set_index(cities, pca.index)
        cities['PC1'] = pca
        _clean_up(cities)

        ax = country.boundary.plot(ax=ax, edgecolor="black", linewidth=0.5)
        ax = cities.plot(ax=ax, column='PC1', cmap='winter')
        ax = cities.plot(ax=ax, column='PC1', cmap='winter')

    _ = ax.axis("off")



def _set_index(df, index):
    df['index_c'] = index
    return df.set_index('index_c')


def _clean_up(df):
    df = df[~df.index.duplicated()]
    df.dropna()


def display_similarity_on_map2(cities_pca, countries_names, crs_reference, linewidth, scale_cities, cmap='winter'):
    crs =  pyproj.crs.CRS.from_user_input(crs_reference) if isinstance(crs_reference, int) else ox.project_gdf(ox.geocode_to_gdf(crs_reference)).crs

    cities = ox.geocode_to_gdf(list(cities_pca.index))
    poland = ox.geocode_to_gdf(countries_names)

    if scale_cities:
        cities.geometry = cities.geometry.scale(scale_cities, scale_cities, scale_cities)

    cities = ox.project_gdf(cities, crs)
    poland = ox.project_gdf(poland, crs)

    cities['name'] = cities_pca.index
    cities = cities.set_index('name')

    cities['PC1'] = cities_pca

    cities = cities[~cities.index.duplicated()]
    cities.dropna()

    ax = poland.boundary.plot(edgecolor="black", linewidth=linewidth)
    cities.plot(ax=ax, column='PC1', cmap=cmap)
    _ = ax.axis("off")

#
# cities = ox.geocode_to_gdf(list(cities_pca.index))
# poland = ox.geocode_to_gdf(countries_names)
#
# cities = ox.project_gdf(cities)
# poland = ox.project_gdf(poland)
#
# cities['name'] = cities_pca.index
# cities = cities.set_index('name')
#
# cities['PC1'] = cities_pca
#
# cities = cities[~cities.index.duplicated()]
# cities.dropna()
#
# ax = poland.boundary.plot(edgecolor="black", linewidth=0.5)
# cities.plot(ax=ax, column='PC1', cmap='winter')
# _ = ax.axis("off")
# plt.show()
