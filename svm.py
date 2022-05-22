import pandas as pd
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

sample_data = pd.DataFrame({'f1': [1,2,9,10,11], 'f2': [1,2,9,10,11]})


def get_labels_as_numbers(df: pd.DataFrame):
    distinct_labels = set(df['cluster'])
    label_to_number = {}
    count = 0
    for label in distinct_labels:
        label_to_number[label] = count
        count = count + 1

    return df['cluster'].apply(lambda label: label_to_number[label]).to_numpy()

def fit_and_print_precision(df: pd.DataFrame):
    df['cluster'] = get_labels_as_numbers(df)
    train, test = train_test_split(df, test_size=0.2)
    clf = fit_df(train)
    test_data = test[['PC1', 'PC2']].to_numpy()
    predicted_labels = clf.predict(test_data)
    print(precision_score(test['cluster'].to_numpy(), predicted_labels))


def fit_and_plot_decision_boundary(df: pd.DataFrame):
    clf = fit_df(df)
    pd.set_option('display.max_rows', 100)
    boundary = get_decision_boundary(clf, df['PC1'].min(), df['PC1'].max(), df['PC2'].min(), df['PC2'].max())
    plt.plot(boundary[0], boundary[1], color='lightseagreen')


def fit_df(df):
    number_labels = get_labels_as_numbers(df)
    clf = fit_clf(df[['PC1', 'PC2']].to_numpy(), number_labels)
    return clf


def fit_clf(data, labels):
    clf = svm.SVC(kernel='linear')
    clf.fit(data, labels)
    return clf


def get_decision_boundary(clf, xlim1, xlim2, ylim1, ylim2):
    tmp = clf.coef_[0]
    a = - tmp[0] / tmp[1]
    b = - (clf.intercept_[0]) / tmp[1]
    xx = np.linspace(xlim1, xlim2, num=150)
    yy = a * xx + b
    x = [xy[0] for xy in zip(xx, yy) if ylim1 <= xy[1] <= ylim2]
    y = [y for y in yy if ylim1 <= y <= ylim2]
    return x, y

