import json
import sys
from OSMPythonTools.nominatim import Nominatim

file_path = sys.argv[1]


def validate_places(places):
    failed = [place for place in places if not validate(place)]
    return failed


def validate(place):
    try:
        nominatim = Nominatim()
        nominatim.query(place).areaId()
        return True
    except Exception as e:
        print("Validator: " + str(e))
        return False


with open(file_path, 'r') as file:
    experiment = json.load(file)
    cities = experiment['cities']
    print(str(validate_places(cities)))