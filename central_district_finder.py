from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder
from shapely.geometry import shape
from unidecode import unidecode

from osmApi import get_city_center, get_overpass_api


def find_central_district(place):
    nominatim = Nominatim()
    areaId = nominatim.query(place).areaId()

    overpass = get_overpass_api()
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector='"admin_level"="9"', out='geom')
    result = overpass.query(query)
    city_center = shape(get_city_center(place).geometry())
    central_district = next((unidecode(element.tags()['name']) for element in result.elements() if shape(element.geometry()).contains(city_center)), None)
    return central_district


poland = [find_central_district(place) + ", " + place for place in [
    "Lodz, Poland",
    "Krakow, Poland",
    "Wroclaw, Poland",
    "Poznan, Poland",
    "Gdansk, Poland",
    "Szczecin, Poland",
    "Bydgoszcz, Poland",
    "Lublin, Poland",
    "Katowice, Poland",
    "Bialystok, Poland",
    "Gdynia, Poland",
    "Czestochowa, Poland",
    "Sosnowiec, Poland",
    "Radom, Poland",
    "Torun, Poland",
    "Kielce, Poland",
    "Gliwice, Poland",
    "Zabrze, Poland",
    "Bytom, Poland"
] if find_central_district(place) is not None]

spain = [find_central_district(place) + ", " + place for place in [
    "Seville, Spain",
    "Zaragoza, Spain",
    "Madrid, Spain",
    "Barcelona, Spain",
    "Malaga, Spain",
    "Murcia, Spain",
    "Palma, Spain",
    "Bilbao, Spain",
    "Alicante, Spain",
    "Valladolid, Spain",
    "Vigo, Spain",
    "Gijon, Spain",
    "A Coruna, Spain",
    "Granada, Spain",
    "Elche, Spain",
    "Oviedo, Spain",
    "Pamplona, Spain",
    "Burgos, Spain",
    "Salamanca, Spain",
] if find_central_district(place) is not None]
print(spain)
print(poland)

