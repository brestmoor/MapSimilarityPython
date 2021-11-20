import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import pyproj
from osmnx.plot import _get_colors_by_value
import re

from ox_api import geocode_to_gdf_by_place_or_rel_id
from pca import calculate_pca

# plt.rcParams["figure.dpi"] = 4000
# ox.config(log_console=False, use_cache=True)
ox.config(log_console=False, timeout=300,
          use_cache=True,
          overpass_endpoint='http://localhost:12346/api',
          overpass_rate_limit=False, max_query_area_size = 2 * 1000 * 50 * 100)

def _set_index(df, index):
    df['index_c'] = index
    return df.set_index('index_c')


def _clean_up(df):
    df = df[~df.index.duplicated()]
    df.dropna()

def extract_osm_id(text):
    if '(' in text and ')' in text:
        return re.split(r"([()])", text)[-3]
    else:
        return text

def display_similarity_on_map2(cities_pca, countries_names, crs_reference, linewidth, scale_cities, cmap='winter'):
    crs =  pyproj.crs.CRS.from_user_input(crs_reference) if isinstance(crs_reference, int) else ox.project_gdf(ox.geocode_to_gdf(crs_reference)).crs

    cities_names = [extract_osm_id(name) for name in cities_pca.index]
    cities = geocode_to_gdf_by_place_or_rel_id(cities_names)
    poland = geocode_to_gdf_by_place_or_rel_id(countries_names)

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


gdf = geocode_to_gdf_by_place_or_rel_id(["Meaux, France",
    "Coulommiers, France",
    "Compiegne, France",
    "Chauny, France",
    "Soissons, France",
    "Sezanne, France",
    "Troyes, France",
    "Reims, France",
    "Montargis, France",
    "Evreux, France",
    "Beauvais, France",
    "Amiens, France",
    "L'aigle, France",
    "Lisieux, France",
    "Laval, France",
    "Lamballe, France",
    "Saint-Malo, France",
    "Dinan, France",
    "Saint-Brieuc, France",
    "Guingamp, France",
    "Lannion, France",
    "Morlaix, France",
    "Landivisiau, France",
    "Landerneau, France",
    "Chateau-Gontier, France",
    "Angers, France",
    "Nantes, France",
    "Tours, France",
    "La Roche-Sur-Yon, France",
    "Challans, France",
    "Cholet, France",
    "Thouars, France",
    "Niort, France"])

print()