import pandas as pd
from pathos.pools import ProcessPool


def calculate_scores(places, functions):
    pool = ProcessPool()
    results = list(pool.map(calc_for_city(functions), places))
    return pd.DataFrame(results, columns=[func.original_func_name for func in functions], index=places)


def calc_for_city(functions):
    return lambda place: [function(place) for function in functions]
