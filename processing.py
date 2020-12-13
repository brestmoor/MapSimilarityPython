import pandas as pd

def normalize_series(first, second):
    first_normalized = []
    second_normalized = []

    for x, y in zip(first, second):
        if x > 1 or y > 1:
            max_value = max(x, y)
            first_normalized.append(normalize(x, max_value))
            second_normalized.append(normalize(y, max_value))
        else:
            first_normalized.append(x)
            second_normalized.append(y)

    return pd.Series(first_normalized), pd.Series(second_normalized)


def normalize(x, x_max):
    return x/x_max
