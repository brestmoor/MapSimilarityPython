import pandas as pd
from pathos.pools import ProcessPool
import traceback


def calculate_scores(places, functions):
    pool = ProcessPool(nodes=2)
    results = list(pool.map(calc_for_city_fn_producer(functions), places))
    result_df = pd.DataFrame(results, columns=[func.original_func_name for func in functions], index=places)
    return result_df


def calc_for_city_fn_producer(functions):
    def calc_for_city(place):
        return [nan_on_error(lambda: function(place)) for function in functions]
    return calc_for_city


def nan_on_error(func):
    try:
        return func()
    except Exception as e:
        print(str(e) + " returning None")
        return None
