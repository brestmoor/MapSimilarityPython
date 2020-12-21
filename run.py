import json

from experiments import run_by_str_with_stats
# file_path = sys.argv[1]
from util.function_util import timed

file_path = './notebook/compare_subway.json'


@timed
def run(path):
    with open(path, 'r') as file:
        experiment = json.load(file)
        cities = experiment['cities']
        criteria = experiment['criteria']
        return run_by_str_with_stats(cities, criteria)


if __name__ == '__main__':
    stats_df, similarity_df = run(file_path)
    print(stats_df.to_string())
    print()
    print(similarity_df.to_string())



