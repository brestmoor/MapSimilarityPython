import logging
import sys
import traceback
import os

import pandas as pd
from OSMPythonTools.api import Api
from pathos.pools import ProcessPool

logging.basicConfig(stream=sys.__stdout__, level=logging.INFO)
logger = logging.getLogger('MapSimilarityPython')


def calculate_scores(places, functions):
    logger.info(" Calculating parameters for " + str(len(places)) + ' places')
    pool = ProcessPool(nodes=8)

    results = list(pool.map(calc_for_city_fn_producer(functions), places))
    result_df = pd.DataFrame(results, columns=[func.original_func_name for func in functions], index=places)
    result_df = result_df.set_index(
        result_df.apply(
            lambda r: _translate_rel_ids_to_names(r.name) + ' (' + r.name + ')' if r.name.isnumeric() else r.name,
            axis=1)
    )
    return result_df


def calc_for_city_fn_producer(functions):
    def calc_for_city(place):
        results_for_city = [nan_on_error(lambda: function(place), place) for function in functions]
        logger.info(" Finished for " + place)
        return results_for_city

    return calc_for_city


def nan_on_error(func, place):
    try:
        return func()
    except Exception as e:
        message = str(e) + '. Occurred for ' + place + '. Returning None'
        logger.error(message)
        # traceback.print_exc()
        return None


def _translate_rel_ids_to_names(rel_id):
    api = Api()
    rel = api.query('relation/' + str(rel_id))
    return rel.tag('name')
