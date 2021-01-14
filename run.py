import json
import sys

from experiments import get_scores_and_similarity, get_scores
from util.function_util import timed

file_path = sys.argv[1]
output_file_path = sys.argv[2]
# file_path = './notebook/compare_subway.json'


def process_experiment(path, processing_fn):
    with open(path, 'r') as file:
        experiment = json.load(file)
        cities = experiment['cities']
        criteria = experiment['criteria']
        return processing_fn(cities, criteria)

@timed
def run(path):
    process_experiment(path, get_scores_and_similarity)


if __name__ == '__main__':
    process_experiment(file_path, get_scores).to_csv(output_file_path)



