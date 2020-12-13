import pandas as pd

def normalize_series(first, second):
    first_normalized = []
    second_normalized = []

    for x, y in zip(first, second):
        if True:
            max_value = max(x, y)
            first_normalized.append(max_value if max_value == 0 else normalize(x, max_value))
            second_normalized.append(max_value if max_value == 0 else normalize(y, max_value))
        else:
            first_normalized.append(x)
            second_normalized.append(y)

    return pd.Series(first_normalized), pd.Series(second_normalized)


def normalize(x, x_max):
    return x/x_max
