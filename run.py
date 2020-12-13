import json
import sys
from tabulate import tabulate
from experiments import run_by_str, run_by_str_with_stats

# file_path = sys.argv[1]

file_path = 'compare_buses.json'

with open(file_path, 'r') as file:
    experiment = json.load(file)
    cities = experiment['cities']
    criteria = experiment['criteria']
    stats_df, similarity_df = run_by_str_with_stats(cities, criteria)
    print(stats_df.to_string())
    print()
    print(similarity_df.to_string())



