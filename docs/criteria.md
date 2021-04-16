### Pojęcia:

Graf (sieć ulic) uproszczony - Usuwane są wszystkie wierzchołki które nie są skrzyżowaniami
(mają mniej niż 3 wychodzące krawędzie i nie są ślepymi zaułkami), a w ich miejsce wstawiana jest krawędź z
geometrią poprzedniej trasy jako atrybut oraz z jej oryginalną długością.

Skonsolidowane skrzyżowania - Pobliskie wierzchołki składające się na skrzyżowanie zastępowane są pojedynczym
wierzchołkiem. Wierzchołki łączone są domyślnie w promieniu 10 metrów.

### Kryteria porównawcze:

Biblioteka OSMnx dostarcza funkcję umożliwiającą policzenie podstawowych parametrów dla miasta:
```python
import osmnx as ox
basic_stats = ox.basic_stats(G, area)
```
gdzie
```G``` to graf NetworkX przedstawiający sieć dróg miasta, a ```area``` to powierzchnia miasta.


Dla danego miasta ```basic_stats``` liczone jest w następujący sposób:

```python
# filtry zawężające typy dróg
custom_filter = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
# pobieranie mapy z OSM do grafu NetworkX. Domyślnie pobierany graf jest grafem uproszczonym
G = ox.graph_from_place(city_name, network_type='drive', custom_filter=custom_filter)
# projekcja do najlepszego lokalnego układu odniesienia (CRS dla strefy UTM w której leży centroid grafu)
G_proj = ox.project_graph(G)
# konwersja wierzchołków z grafu do DataFrame
nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
# wyliczanie powierzchni miasta
graph_area_m = nodes_proj.unary_union.convex_hull.area

# wyliczanie basic_stats. Parametr clean_intersects powoduje uproszczenie skrzyżowań
basic_stats =  ox.basic_stats(G, area=graph_area_m, clean_intersects=True, circuity_dist='euclidean')
```

Wyniki dostępne są jako słownik, i wartości uzyskuje się np. 

```python
basic_stats['...']
```

1. intersection_density_km - gęstość skrzyżowań w uproszczonym grafie ze skonsolidowanymi skrzyżowaniami.
```python
basic_stats['intersection_density_km']
```

2. street_density_km - gęstość ulic, a właściwie gęstość krawędzi które w grafie uproszczonym ze skonsolidowanymi skrzyżowaniami biegną od skrzyżowania do skrzyżowania.
```python
basic_stats['street_density_km']
```

3. street_length_avg - Średnia długość ulicy w uproszczonym grafie ze skonsolidowanymi skrzyżowaniami.
```python
basic_stats['street_length_avg']
```

4. circuity_avg - Średnia okrężność - mierzona jako stosunek odległości w lini prostej,
   do odległości jaką trzeba pokonać jadąc ulicami miasta. 
   [Transportation Geography and Network Science/Circuity](https://en.wikibooks.org/wiki/Transportation_Geography_and_Network_Science/Circuity). 
   Okrężność mierzona dla każdej pary wierzchołków w grafie uproszczonym ze skonsolidowanymi skrzyżowaniami.
```python
basic_stats['circuity_avg']
```

5. streets_per_node_avg - Ile średnio krawędzi wychodzi z wierzchołka. Graf uproszczony ze skonsolidowanymi skrzyżowaniami.
```python
basic_stats['streets_per_node_avg']
```

6. one_way_percentage - Udział ulic jednokierunkowych
```python
# Pobieranie dróg z OSM spełniających podane kryteria oraz zwrócenie ich jako DataFrame
highways = ox.geometries_from_place(place, {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
return highways[highways['oneway'] == 'yes'].osmid.count() / highways.osmid.count()
```

7. trunk_percentage - Udział ulic szybkiego ruchu 'trunk' 
```python
highways = ox.geometries_from_place(place, {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
return highways[highways['highway'] == 'trunk'].osmid.count() / highways.osmid.count()
```

8. primary_percentage - Udział ulic pierwszorzędnych
```
kod analogiczny jak powyżej, ale porównujemy highways['highway'] == 'primary'
```

9. secondary_percentage - Udział ulic drugorzędnych


10. tertiary_percentage - Udział ulic trzeciorzędnych


11. traffic_lights_share - Ilość sygnalizacji swietlnych na metr drogi.
```python
highways = ox.project_gdf(ox.geometries_from_place(place, {'highway': ['trunk', 'primary', 'secondary', 'tertiary']}))
traffic_signals = ox.geometries_from_place(place, {'highway': 'traffic_signals'})
return len(traffic_signals) / highways.geometry.length.sum()
```

11. crossing_share - Ilość przejsc dla pieszych na metr drogi.
```python
highways = ox.project_gdf(ox.geometries_from_place(place, {'highway': ['trunk', 'primary', 'secondary', 'tertiary']}))
crossings = ox.geometries_from_place(place, {'highway': 'crossing'})
return len(crossings) / highways.geometry.length.sum()
```

12. average_dist_to_park - Średnia odległosc od budynku mieszkalnego do parku
```python
parksDf = ox.geometries_from_place(place, {'leisure': 'park'})
buildingsDf = ox.geometries_from_place(place, {'building': True})

parks_proj = ox.project_gdf(parksDf)
buildings_proj = ox.project_gdf(buildingsDf)

#funkcja distance_to_nearest znajduje najblizszy obiekt w DataFrame, do obiektu podanego jako drugi argument
distances = buildings_proj.iloc[::5].apply(lambda row: distance_to_nearest(parks_proj, row.geometry), axis=1)  
return distances.mean()
```

13. average_dist_to_greenland - Średnia odległosc od budynku mieszkalnego do dowolnego terenu zielonego

```python
kod identyczny jak powyżej, ale jako kryterium w zapytaniu do OSM używamy
{'leisure': ['park', 'garden'], 'landuse': ['forest', 'grass'], 'natural': 'wood'}
```

14. average_dist_to_bus_stop - Średnia odległosc od budynku mieszkalnego do przystanku autobusowego

```python
kod analogiczny jak powyżej, ale jako kryterium w zapytaniu do OSM używamy
{'highway': 'bus_stop'}
```
15. average_dist_to_bus_stop - Średnia odległosc od budynku mieszkalnego do przystanku autobusowego

```python
kod analogiczny jak powyżej, ale jako kryterium w zapytaniu do OSM używamy
{'highway': 'bus_stop', 'public_transport': 'stop_position'}
```

16. buildings_density - Gęstość budynków
```python
buildingsDf = ox.geometries_from_place(place, {'building': True})
buildings_proj = ox.project_gdf(buildingsDf)
krakow_boundary = ox.project_gdf(ox.geocode_to_gdf(place))
return buildings_proj.area.sum() / krakow_boundary.area[0]
```

17. no_of_streets_crossing_boundary - Ilość ulic które przecinają granicę miasta
```python
boundary = ox.project_gdf(ox.geocode_to_gdf(place))
highwaysDf = ox.project_gdf(ox.geometries_from_place(place, {
'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']}, buffer_dist=400))

return sum(highwaysDf.crosses(boundary.iloc[0].geometry))
```

18. no_of_streets_crossing_boundary_proportional - Iloraz ilości ulic przecinających granicę miasta i obwodu miasta
```python
boundary = ox.project_gdf(ox.geocode_to_gdf(place))
highwaysDf = ox.project_gdf(ox.geometries_from_place(place, {
'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']}, buffer_dist=400))

return sum(highwaysDf.crosses(boundary.iloc[0].geometry)) / boundary.iloc[0].geometry.length
```

19. natural_terrain_density - Powierzchnia terenów zielonych do powierzchni miasta
```python
parksDf = ox.geometries_from_place(place, {'leisure': ['park', 'garden'],
                                           'natural': ['wood', 'scrub', 'heath', 'grassland'],
                                           'landuse': ['grass', 'forest']})

parks_proj = ox.project_gdf(parks_polygons)
boundary = ox.project_gdf(ox.geocode_to_gdf(place))
return parks_proj.area.sum() / boundary.area[0]
```

20. cycleways_to_highways - Stosunek długości alejek rowerowych do długości ulic
```python
cyclewaysDf = ox.geometries_from_place(place, {'highway': 'cycleway',
                                                 'cycleway': ['lane', 'opposite_lane', 'opposite', 'shared_lane'],
                                                 'bicycle': 'designated'})
highwaysDf = ox.geometries_from_place(place, {
    'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})

cycleways_proj = ox.project_gdf(cyclewaysDf)
highways_proj = ox.project_gdf(highwaysDf)

return cycleways_proj.length.sum() / highways_proj.length.sum()
```

21. tram_routes_to_highways - Stosunek długości torów tramwajowych do długości ulic
```python
Kod analogiczny jak powyżej, ale trasy do porównania pobieramy:
ox.geometries_from_place(place, {'railway': 'tram'})

```
22. all_railways_to_highway - Stosunek długości torów tramwajowych do długości ulic
```python
Kod analogiczny jak powyżej, ale trasy do porównania pobieramy:
ox.geometries_from_place(place, {'railway': True})
```

23. bus_routes_to_highway - Stosunek długości tras autobusowych do długości dróg
```python
    bus_routes_ways = get_ways_in_relation(place, '"route"="bus"')
    ids_of_bus_ways = [way['ref'] for way in bus_routes_ways]
    
    poi_highways = ox.geometries_from_place(place, {
    'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
    highways_proj = ox.project_gdf(poi_highways)

    return highways_proj[highways_proj.osmid.isin(ids_of_bus_ways)].length.sum() / highways_proj.length.sum()
```

24. median_dist_between_crossroads - Mediana odległości między skrzyżowaniami - zasada działania podobna do ```street_length_avg```, 
    tylko że konsolidacja skrzyżowań wykonywana jest ręcznie i brane są wierzchołki ze stopniem ```deg > 1``` 
```python
cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
g = ox.graph_from_place(place, network_type='drive', custom_filter=cf)
g_proj = ox.project_graph(g)
consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

outdeg = consolidated.out_degree()
to_keep = [n for (n, deg) in outdeg if deg > 1]

consolidated_subgraph = consolidated.subgraph(to_keep)
undir = ox.get_undirected(consolidated)
return np.median([length_tuple[2] for length_tuple in undir.edges.data('length')])
```

25. mode_dist_between_crossroads - Dominanta odległości między skrzyżowaniami liczona po zaokrągleniu do 10-tek
```python
@timed
cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
g = ox.graph_from_place(place, network_type='drive', custom_filter=cf)
g_proj = ox.project_graph(g)
consolidated = ox.consolidate_intersections(g_proj, rebuild_graph=True, tolerance=15, dead_ends=True)

outdeg = consolidated.out_degree()
to_keep = [n for (n, deg) in outdeg if deg > 1]

consolidated_subgraph = consolidated.subgraph(to_keep)
undir = ox.get_undirected(consolidated)
result_mode = mode(([round(length_tuple[2], -1) for length_tuple in undir.edges.data('length')]))
return result_mode
```

26. streets_in_radius_of_100_m - Ilość ulic w odległości 100 metrów od każdej ulicy:
```python
highwaysDf = ox.geometries_from_place(place, {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
highways_proj = ox.project_gdf(highwaysDf)
no_of_neighbors = highways_proj.apply(lambda row: len(within(highways_proj, row.geometry.buffer(100))), axis=1)
return no_of_neighbors.mean()

```
27. share_of_separated_streets - Ilość ulic w sąsiedztwie których (50 metrów) jest mniej niż cztery ulice
```python
highwaysDf = ox.geometries_from_place(place, {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']})
highways_proj = ox.project_gdf(highwaysDf)
no_of_neighbors = highways_proj.apply(lambda row: len(within(highways_proj, row.geometry.buffer(50))), axis=1)
return no_of_neighbors[no_of_neighbors < 4].count() / highways_proj.osmid.count()
```

28. avg_distance_between_buildings - Srednia odległość mniędzy budynkami
```python
buildingsDf = ox.geometries_from_place(place, {'building': True})
buildings_proj = ox.project_gdf(buildingsDf)

dist_to_nearest_building = buildings_proj.apply(lambda row: distance_to_nearest(buildings_proj, row.geometry), axis=1)
return dist_to_nearest_building.mean()

```
29. avg_dist_from_building_to_center - Srednia odległość od dowolnego budynku do centrum (jak bardzo budynki są skoncentrowane wokół centrum)
```python
buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {'building': True}))

# konwersja  punktu określającego środek miasta do CRS budynków (dla których wybrany był automatycznie najlepszy)
center = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
dist_to_center = buildingsDf.apply(lambda row: row.geometry.centroid.distance(center), axis=1)
return dist_to_center.mean()
```


**Kolejne zapytania** opierają się na funkcji ```amenity_dist_to_nearest``` która oblicza dla każdego amenity o typie 
podanym jako parametr odległość do 3 najblizszych obiektów tego typu (Np, w jakiej odleglosci od danego pubu leżą 3 najbliższe puby)

```python
def amenity_dist_to_nearest(place, amenities):
    amenities_df = ox.project_gdf(ox.geometries_from_place(place, amenities))
    # funkcja distances_to_multiple_nearest zwraca X najbliższych odległości od obiektu podanego jako parametr, do najblizszych obiektów z DataFrame podanego jako parametr
    distances_to_nearest = amenities_df.apply(lambda row: distances_to_multiple_nearest(amenities_df, row.geometry, 3), axis=1)
    # średnia ze wszystkich odległości
    mean_of_distances = distances_to_nearest.explode().mean()
    return mean_of_distances

```


30. pubs_dist_to_nearest - Srednia z odległości od pubu/restauracji/baru do 3 najblizszych pubów/restauracji/barów
```python
return amenity_dist_to_nearest(place, {
    "amenity": ["pub", "bar", "bbq", "cafe", "fast_food", "food_court", "ice_cream", "restaurant", "biergarten"]
})

```
31. education_buildings_dist_to_nearest - Srednia z odległości od budynku związanego z nauką/kulturą do 3 najbliższych takich budynków
```python
return amenity_dist_to_nearest(place, {
    "amenity": ["library", "school", "university", "college", "language_school"],
    "tourism": ["museum"]
})
```


32. entertainment_buildings_dist_to_nearest - Srednia z odległości od budynku związanego z rozrywką do 3 najbliższych takich budynków
```python
return amenity_dist_to_nearest(place, {
    "amenity": ["casino", "cinema", "community_centre", "theatre", "nightclub"],
    "leisure": ["dance", "bowling_alley", "amusement_arcade", "fitness_centre", "fitness_station"]
})
```

33. shops_dist_to_nearest - Srednia z odległości od sklepu do 3 najbliższych sklepów
```python
return amenity_dist_to_nearest(place, {"shop": True})
```

34. office_dist_to_nearest - Srednia z odległości od biura do 3 najbliższych biur
```python
return amenity_dist_to_nearest(place, {"office": True})
```


Poniższe zapytania opierają się na funkcji ```amenity_to_all_buildings``` która oblicza stosunek ilości 
obiektów danego typu do wszystkich budynków

```python
amenities_df = ox.geometries_from_place(place, amenities)
# funkcja get_count wykonuje zapytanie do OSM o ilość obiektów danego typu
return len(amenities_df) / get_count(place, '"building"')
```

35. pubs_share - udział wśród wszystkich budynków obiektów związanych z jedzeniem
```python
return amenity_to_all_buildings(place, {
"amenity": ["pub", "bar", "bbq", "cafe", "fast_food", "food_court", "ice_cream", "restaurant", "biergarten"]
})
```

36. education_buildings_share - udział wśród wszystkich budynków obiektów związanych z edukacją / kulturą
```python
return amenity_to_all_buildings(place, {
"amenity": ["library", "school", "university", "college", "language_school"],
"tourism": ["museum"]
})
```

37. entertainment_buildings_share - udział wśród wszystkich budynków obiektów związanych z rozrywką
```python
return amenity_to_all_buildings(place, {
"amenity": ["casino", "cinema", "community_centre", "theatre", "nightclub"],
"leisure": ["dance", "bowling_alley", "amusement_arcade", "fitness_centre", "fitness_station"]
})
```

38. shops_share - Udział sklepów wśród wszystkich budynków
```python
return amenity_to_all_buildings(place, {"shop": True})
```

39. office_share - Udział biur wśród wszystkich budynków
```python
return amenity_to_all_buildings(place, {"office": True})
```

40. buildings_uniformity - Jak bardzo budynki w mieście są równomiernie rozmieszczone. Srednia odległość od budynku do najbliższych 
    4 budynków porównywana jest z oczekiwaną odległością w "idealnym" mieście, w którym wszystkie budynki byłby w tej samej odległości.
    Im ```uniformity``` jest mniejsze tym bardziej budynki występują w klastrach.
    
```python
buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {'building': True}))
city_boundary = ox.project_gdf(ox.geocode_to_gdf(place))

distances_to_nearest = buildingsDf.apply(lambda row: distances_to_multiple_nearest(buildingsDf, row.geometry, 4), axis=1)

mean_of_distances = distances_to_nearest.explode().mean()

expected_avg_dist_to_nearest = sqrt(city_boundary.area[0] / len(buildingsDf))
return mean_of_distances / expected_avg_dist_to_nearest
```

41. avg_distance_to_5_buildings - Srednia odleglosc od budynku do 5 najblizszych budynków

```kod analogiczny do avg_distance_between_buildings, ale analizujemy 5 najblizszych budynków```

42. share_of_buildings_near_center - Jaki udział w liczbie wszystkich budynków mają budynki znajdujące się w centrum
    (1/10 promienia od centrum, przy przybliżeniu kształtu obwodu miasta do okręgu)

```python
buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {'building': True}))

city_boundary_area = ox.project_gdf(ox.geocode_to_gdf(place)).area[0]

r_of_1_10th_circle = sqrt(city_boundary_area / np.math.pi) / 10

projected_point = convert_crs(Point(get_city_center_coordinates(place)), buildingsDf.crs)
circle = projected_point.buffer(r_of_1_10th_circle)

return sum([circle.contains(building) for building in buildingsDf.geometry.centroid]) / len(buildingsDf)
```

43. avg_building_area - średnia powierzchnia budynku
```python
buildingsDf = ox.project_gdf(ox.geometries_from_place(place, {'building': True}))
return buildingsDf.geometry.area.mean()
```

44. circuity - Okrężność, mierzona podobnie jak ``circuity_avg``, ale w tej funkcji losowane jest 30 punktów, i 
    dla wszystkich tras pomiędzy tymi punktami liczona jest okrężność
```python
cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)

random_node_ids = random.sample(g.nodes, 30)

nodes_pairs = list(itertools.combinations(random_node_ids, 2))

city_paths = [path for path in (shortest_path(g, orig, dest) for orig, dest in nodes_pairs) if path is not None]

nodes_pairs = [(path[0], path[-1]) for path in city_paths]

city_paths_lengths = sum(path_len_digraph(g, path) for path in city_paths)
great_circle_paths_lengths = sum([great_circle_dist(g, orig, dest) for orig, dest in nodes_pairs])

return city_paths_lengths / great_circle_paths_lengths
```

45. network_orientation - Jak jednorodnie ulice są ukierunkowane, biorąc pod uwagę kierunki świata. 
    Dla wszystkich odcinków składających się na drogi liczony jest Namiar (ang. bearing), czyli kąt pod jakim leży odcinek względem północy.
    Następnie odcinki te przydzielane są do przedziałów co 10 stopni. Wynikiem funkcji jest współczynnik zmienności względem oczekiwanej ilości, którą
    jest idealne rozmieszczenie w przedziałach (taka sama ilość odcinków w każdym przedziale).
```python
cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
g = ox.graph_from_place(place, network_type='drive', custom_filter=cf, simplify=False)

# funkcja wbudowana w OSMNX dodaje bearing do każdego odcinka
g = ox.add_edge_bearings(ox.get_undirected(g))
# funkcja simplify_bearing odejmuje 180 od kątów większych od 180. Ignorujemy przez to orientacje ulicy
bearings = pd.Series([simplify_bearing(d['bearing']) for u, v, k, d in g.edges(keys=True, data=True)])
# zaorkąglanie, czyli przydzialenie do przedziałów
bearings = bearings.map(lambda bearing: round(bearing, -1))
# zamiana kątów 180 stopni na 0
bearings = bearings.map(lambda bearing: bearing if bearing != 180 else 0)
expected_number_in_group = len(bearings) / 18
frequency = bearings.groupby(bearings).count()

return stdev(frequency, expected_number_in_group) / expected_number_in_group

```

46. avg_short_distances_between_hospitals - średnie najkrótsze odległości między szpitalami
```python
network_graph = ox.graph_from_place(place, network_type='drive')
hospitals = ox.geometries_from_place(place, {'amenity': 'hospital'})
hospitals_centroids = hospitals.geometry.centroid
# centroidy szpitali jako wspołrzędne geograficzne
centroids_as_tuples = [_to_coordindates(centroid) for centroid in hospitals_centroids]

# w sieci dróg wybierane są wierzchołki leżące najbliżej danego szpitala
hospital_nodes = [ox.get_nearest_node(network_graph, coords_tuple) for coords_tuple in centroids_as_tuples]

# tworzone są wszystkie pary szpitali
hospital_pairs = list(itertools.combinations(hospital_nodes, 2))
shortest_paths = [ox.shortest_path(network_graph, *pair) for pair in hospital_pairs]
sums = [sum(ox.utils_graph.get_route_edge_attributes(network_graph, path, 'length')) for path in shortest_paths]
return np.mean(sums)
```

Poniższe zapytania odnoszą się do sieci metra, lub po pewnych modyfikacjach, do sieci tramwajowej

47. average_how_many_subway_routes_are_there_from_one_stop_to_another - Na ile sposobów można dojechać z jednego przystanku metra do drugiego,
    tak żeby trasa nie przekraczała dwukrotności najkrótszej

Algorytm opiera się na:
- pobraniu sieci metra oraz wszystkich stacji 
- uproszczenie grafu poprzez usunięcie wszystkich wierzchołków które
nie są stacjami i wstawienie pomiędzy stacjami krawędzi o długości najkrótszej trasy między tymi stacjami
- znalezienie i policzenie wszystkich tras pomiędzy dowolnymi wierzchołkami w grafie których długość nie przekrzacza dwókrotności najkrótszej
```python
G = ox.graph_from_place(place, retain_all=True, truncate_by_edge=True, buffer_dist=500, simplify=False, custom_filter='["railway"~"subway"][!service]')
subway_stops = ox.geometries_from_place(place, {'railway': 'stop', 'subway': 'yes'})

lists_of_ids_per_station = subway_stops[subway_stops.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)
actual_stations = _join_stops_with_same_name(G, lists_of_ids_per_station)

G = nx.MultiDiGraph(G.subgraph(max(nx.weakly_connected_components(G))))

Gs = nx.MultiGraph(nx.to_undirected(G.copy()))
edges = list(Gs.edges())

actual_stations = [actual_station for actual_station in actual_stations if actual_station in Gs]
_contract_all_nodes_between_stations(Gs, actual_stations)
Gs = nx.Graph(Gs)
_assign_shortest_path_as_length(Gs, G, actual_stations)
stations_pairs = list(itertools.combinations(actual_stations, 2))
number_of_routes = [_number_of_routes_not_longer_than_2_times(Gs, station_pair) for station_pair in stations_pairs]
    
return np.mean(number_of_routes)
```


48. average_how_many_subway_routes_are_there_from_one_stop_to_another - Na ile sposobów można dojechać z jednego przystanku metra do drugiego,
    tak żeby trasa nie przekraczała dwukrotności najkrótszej

Algorytm opiera się na:
- pobraniu sieci metra oraz wszystkich stacji
- uproszczenie grafu poprzez usunięcie wszystkich wierzchołków które
  nie są stacjami i wstawienie pomiędzy stacjami krawędzi o długości najkrótszej trasy między tymi stacjami
- znalezienie i policzenie wszystkich tras pomiędzy dowolnymi wierzchołkami w grafie których długość nie przekrzacza dwókrotności najkrótszej
```python
G = ox.graph_from_place(place, retain_all=True, truncate_by_edge=True, buffer_dist=500, simplify=False, custom_filter='["railway"~"subway"][!service]')
subway_stops = ox.geometries_from_place(place, {'railway': 'stop', 'subway': 'yes'})

lists_of_ids_per_station = subway_stops[subway_stops.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)
actual_stations = _join_stops_with_same_name(G, lists_of_ids_per_station)

G = nx.MultiDiGraph(G.subgraph(max(nx.weakly_connected_components(G))))

Gs = nx.MultiGraph(nx.to_undirected(G.copy()))
edges = list(Gs.edges())

actual_stations = [actual_station for actual_station in actual_stations if actual_station in Gs]
_contract_all_nodes_between_stations(Gs, actual_stations)
Gs = nx.Graph(Gs)
_assign_shortest_path_as_length(Gs, G, actual_stations)
stations_pairs = list(itertools.combinations(actual_stations, 2))
number_of_routes = [_number_of_routes_not_longer_than_2_times(Gs, station_pair) for station_pair in stations_pairs]
    
return np.mean(number_of_routes)
```

49. how_many_failures_can_network_handle - na awarię w ilu miejscach sieć metra może sobie pozwolić,
    tak żeby dalej można było przejechać z dowolnej jednej stacji do drugiej
```python
G = ox.graph_from_place(place, retain_all=True, truncate_by_edge=True, buffer_dist=500, simplify=False, custom_filter='["railway"~"subway"][!service]')

subway_stops = ox.geometries_from_place(place, {'railway': 'stop', 'subway': 'yes'})

lists_of_ids_per_station = subway_stops[subway_stops.osmid.isin(G.nodes)].groupby('name')['osmid'].apply(list)
actual_stations = _join_stops_with_same_name(G, lists_of_ids_per_station)

G = nx.MultiDiGraph(G.subgraph(max(nx.weakly_connected_components(G))))

Gs = nx.MultiGraph(nx.to_undirected(G.copy()))
edges = list(Gs.edges())

_contract_all_nodes_between_stations(Gs, actual_stations)
Gs = nx.Graph(Gs)
original_size = len(max(nx.connected_components(Gs)))
not_failed = 0

# usuwane są kolejne krawędzie z grafu, i sprawdzane czy największy komponent ma dalej tyle samo wierzchołków
for u, v in nx.edges(Gs):
    Gs.remove_edge(u, v)
    current_max_component_size = len(max(nx.connected_components(Gs)))
    Gs.add_edge(u, v)
    if current_max_component_size == original_size:
        not_failed = not_failed + 1

return not_failed
```

