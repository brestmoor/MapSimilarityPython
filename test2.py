import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon

parksDf = ox.pois_from_place('Krakow, Poland', {'leisure': ['park', 'garden'], 'natural': ['wood', 'scrub', 'heath', 'grassland'], 'landuse': ['grass', 'forest']})

parks_polygons = parksDf[[isinstance(x, Polygon) for x in parksDf.geometry]]
parks_proj = ox.project_gdf(parks_polygons)

krakow_boundary = ox.project_gdf(ox.geocode_to_gdf('Krakow, Poland'))

contains = [park for park in parks_proj.geometry if ~krakow_boundary.unary_union.contains(park)]
