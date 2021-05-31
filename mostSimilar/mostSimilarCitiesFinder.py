import json

from numpy import ndenumerate

from experiments import get_scores_and_similarity
from similarity import calculate_similarity


def find_most_similar_from_json(path):
    with open(path, 'r') as file:
        most_similar_experiment = json.load(file)
        groups = most_similar_experiment['groups']
        criteria = most_similar_experiment['criteria']
        return find_most_similar_in_groups(groups, criteria)


def find_most_similar_in_groups(groups, criteria_string):
    scores, similarity = get_scores_and_similarity([place for group in groups for place in group], criteria_string)
    return find_most_similar_in_df(groups, similarity)


def find_most_similar_in_df(groups, scores):
    similarityDf = calculate_similarity(scores)
    max_similarity = 0
    best_cities = ()
    for first_city in similarityDf.index:
        for second_city in similarityDf.columns:
            similarity = similarityDf[first_city][second_city]
            if _find_group(first_city, groups) != _find_group(second_city, groups) and similarity > max_similarity:
                max_similarity = similarity
                best_cities = (first_city, second_city)
    return best_cities, max_similarity


def _find_group(city, groups):
    for group in groups:
        if city in group:
            return groups.index(group)
    raise Exception("City not found in any group")


