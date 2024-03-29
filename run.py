import json
import sys
import osmnx as ox

from experiments import get_scores_and_similarity, get_scores
from functions import streets_per_node_avg
from scores import calculate_scores
from util.function_util import timed

# ox.config(log_console=False, use_cache=True, timeout=300)

file_path = sys.argv[1]
output_file_path = sys.argv[2]


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

    # results = process_experiment(file_path, get_scores)
    # file_path_no_format = file_path.split('.')[0]
    # os.mkdir('./results/' + str(file_path_no_format) + datetime.now().strftime("_%H_%M_%S"))
    # results.to_csv(output_file_path if output_file_path is not None else file_path_no_format)
    # pca(results)

