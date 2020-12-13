import json
import sys
from tabulate import tabulate
from experiments import run_by_str

# file_path = sys.argv[1]

file_path = 'compare_buses.json'

with open(file_path, 'r') as file:
    experiment = json.load(file)
    cities = experiment['cities']
    criteria = experiment['criteria']
    result_df = run_by_str(cities, criteria)
    print(tabulate(result_df, headers='keys', tablefmt='psql'))



