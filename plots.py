import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt

import seaborn as sns
import matplotlib as mpl
from clustering import k_means


sns.set_theme(style="darkgrid")

east = ["Suwalki, Poland","Augustow, Poland","Elk, Poland","Gizycko, Poland","Ketrzyn, Poland","Mragowo, Poland","Bialystok, Poland","Pisz, Poland","Mikolajki, Poland","Lomza, Poland","Zambrow, Poland","Bielsk Podlaski, Poland","Hajnowka, Poland","Sokolow Podlaski, Poland","Siedlce, Poland","Biala Podlaska, Poland","Pulawy, Poland","Lukow, Poland","Wlodawa, Poland","Lubartow, Poland","Lublin, Poland","Swidnik, Poland","Krasnystaw, Poland","Zamosc, Poland","Chelm, Poland","Krasnik, Poland","Bilgoraj, Poland","Stalowa Wola, Poland","Sandomierz, Poland","Tarnobrzeg, Poland","Tomaszow Lubelski, Poland","Rzeszow, Poland","Lancut, Poland","Jaroslaw, Poland","Przemysl, Poland","Sanok, Poland","Krosno, Poland","Jaslo, Poland","Hrubieszow, Poland"]
west = ["Swinoujscie, Poland","Miedzyzdroje, Poland","Gryfice, Poland","Szczecin, Poland","Nowogard, Poland","Gorzow Wielkopolski, Poland","Swiebodzin, Poland","Police, Poland","Goleniow, Poland","Stargard, Poland","Choszczno, Poland","Debno, Poland","Zielona Gora, Poland","Nowa Sol, Poland","Nowogrod Bobrzanski, Poland","Glogow, Poland","Zary, Poland","Zagan, Poland","Swietoszow, Poland","Polkowice, Poland","Boleslawiec, Poland","Chojnow, Poland","Kliczkow, Poland","Nowogrodziec, Poland","Luban, Poland","Lwowek Slaski, Poland","Kamienna Gora, Poland","Bolkow, Poland","Swiebodzice, Poland","Walbrzych, Poland","Swidnica, Poland","Jawor, Poland","Lubin, Poland","Wolsztyn, Poland","Nowy Tomysl, Poland"]

north_italy = [    "Morbegno, Italy","Domodossola, Italy","Bormio, Italy","Lecco, Italy","Aosta, Italy","Neive, Italy","Orta San Giulio, Italy",
"Barolo, Italy","Alba, Italy","Stresa, Italy","Neive, Italy","Bra, Italy","Saluzzo, Italy","Pinerolo, Italy","Giaveno, Italy","Carmagnola, Italy","Ivrea, Italy","Mondovi, Italy","Busca, Italy","Poirino, Italy","Santhia, Italy",]
south_italy = ["Savoca, Sicily, Italy","Catania, Sicily, Italy","Cefalu, Sicily, Italy","Caltanissetta, Sicily, Italy","Barrafranca, Sicily, Italy","Mussomeli, Sicily, Italy","Prizzi, Sicily, Italy","Alcamo, Sicily, Italy","Castelvetrano, Sicily, Italy","Lercara Friddi, Sicily, Italy","Valledolmo, Sicily, Italy","Bisacquino, Sicily, Italy","Menfi, Sicily, Italy","Noto, Sicily, Italy","Palagonia, Sicily, Italy","Leonforte, Sicily, Italy","Sciacca, Sicily, Italy","Scicli, Sicily, Italy","Vittoria, Sicily, Italy","Comiso, Sicily, Italy","Rosolini, Sicily, Italy","Racalmuto, Sicily, Italy","Gela, Sicily, Italy","Ravanusa, Sicily, Italy","Campobello di Licata, Sicily, Italy","Favara, Sicily, Italy","Raffadali, Sicily, Italy"]



from pca import pca
from util.processing import remove_outliers, standarize

df = remove_outliers(pd.read_csv("italy_piedmon_sicily_city_structure_extended.csv", index_col=0))
standarized_df = standarize(df)
standarized_df['is_sicily'] = [True if is_west in south_italy else False for is_west in standarized_df.index]
pcaDf = pca(df)
k_res = k_means(df)
pcaDf['cluster'] = [True if is_west in south_italy else False for is_west in pcaDf.index]
# pcaDf['cluster'] = k_res


def plot_points_with_labels(df):
    mpl.rcParams['figure.dpi'] = 340
    fig, ax = plt.subplots()
    df.plot('PC1', 'PC2', kind='scatter', ax=ax)

    for k, v in df.iterrows():
        ax.annotate(k, v, fontsize=3)
    plt.show()


def plot_points_with_coloring(df):
    plt.figure(figsize=(15, 8))
    sns.relplot(x='PC1', y='PC2', hue='cluster', data=df, height=8.27, aspect=11.7 / 8.27)
    plt.show()


plot_points_with_coloring(pcaDf)
# plot_points_with_labels(pcaDf)
