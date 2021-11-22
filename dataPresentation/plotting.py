import matplotlib.pyplot as plt
import seaborn as sns

def plot_points_with_coloring(df):
    plt.figure(figsize=(15, 8))
    sns.relplot(x='PC1', y='PC2', hue='cluster', data=df, height=8.27, aspect=11.7 / 8.27)
    plt.show()


def plot_points_with_coloring_without_showing(df):
    plt.figure(figsize=(15, 8))
    sns.relplot(x='PC1', y='PC2', hue='cluster', data=df, height=8.27, aspect=11.7 / 8.27)


def plot_points_1_dim_with_coloring(df, palette='cool'):
    plt.figure(figsize=(15, 8))
    sns.relplot(x='PC1', y=1, hue='PC1', palette=palette, data=df, height=8.27, aspect=11.7 / 8.27)
    plt.show()