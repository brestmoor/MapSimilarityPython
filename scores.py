import pandas as pd
from pathos.pools import ProcessPool


def calculate_scores(places, functions):
    pool = ProcessPool()
    results = list(pool.map(calc_for_city_fn_producer(functions), places))
    result_df = pd.DataFrame(results, columns=[func.original_func_name for func in functions], index=places)
    return result_df.dropna()


def calc_for_city_fn_producer(functions):
    def calc_for_city(place):
        try:
            return [function(place) for function in functions]
        except Exception as e:
            print(str(e) + " for " + place + ". Skipping")
            return []
    return calc_for_city

