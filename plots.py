import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt


import seaborn as sns
import matplotlib as mpl
from clustering import k_means
from util.feature_selection import choose_features

sns.set_theme(style="darkgrid")

north = ["Miedzyzdroje, Poland","Miedzywodzie, Poland","Dziwnowek, Poland","Dziwnow, Poland","Pobierowo, Poland","Pustkowo, Poland","Rewal, Poland","Pogorzelica, Poland","Kolobrzeg, Poland","Ustronie Morskie, Poland","Mielno, Poland","Darlowo, Poland","Dzwirzno, Poland","Grzybowo, Poland","Ustka, Poland","Jaroslawiec, Poland","Rowy, Poland","Leba, Poland","Puck, Poland","Jastarnia, Poland","Debki, Poland","Karwia, Poland","Wiselka, Poland","Lukecin, Poland","Mrzezyno, Poland","Kamien Pomorski, Poland","Jantar, Poland","Krynica Morska, Poland","Niechorze, Poland"]

east = ["Suwalki, Poland","Augustow, Poland","Elk, Poland","Gizycko, Poland","Ketrzyn, Poland","Mragowo, Poland","Bialystok, Poland","Pisz, Poland","Mikolajki, Poland","Lomza, Poland","Zambrow, Poland","Bielsk Podlaski, Poland","Hajnowka, Poland","Sokolow Podlaski, Poland","Siedlce, Poland","Biala Podlaska, Poland","Pulawy, Poland","Lukow, Poland","Wlodawa, Poland","Lubartow, Poland","Lublin, Poland","Swidnik, Poland","Krasnystaw, Poland","Zamosc, Poland","Chelm, Poland","Krasnik, Poland","Bilgoraj, Poland","Stalowa Wola, Poland","Sandomierz, Poland","Tarnobrzeg, Poland","Tomaszow Lubelski, Poland","Rzeszow, Poland","Lancut, Poland","Jaroslaw, Poland","Przemysl, Poland","Sanok, Poland","Krosno, Poland","Jaslo, Poland","Hrubieszow, Poland"]
west = ["Swinoujscie, Poland","Miedzyzdroje, Poland","Gryfice, Poland","Szczecin, Poland","Nowogard, Poland","Gorzow Wielkopolski, Poland","Swiebodzin, Poland","Police, Poland","Goleniow, Poland","Stargard, Poland","Choszczno, Poland","Debno, Poland","Zielona Gora, Poland","Nowa Sol, Poland","Nowogrod Bobrzanski, Poland","Glogow, Poland","Zary, Poland","Zagan, Poland","Swietoszow, Poland","Polkowice, Poland","Boleslawiec, Poland","Chojnow, Poland","Kliczkow, Poland","Nowogrodziec, Poland","Luban, Poland","Lwowek Slaski, Poland","Kamienna Gora, Poland","Bolkow, Poland","Swiebodzice, Poland","Walbrzych, Poland","Swidnica, Poland","Jawor, Poland","Lubin, Poland","Wolsztyn, Poland","Nowy Tomysl, Poland"]

north_italy = [    "Morbegno, Italy","Domodossola, Italy","Bormio, Italy","Lecco, Italy","Aosta, Italy","Neive, Italy","Orta San Giulio, Italy",
"Barolo, Italy","Alba, Italy","Stresa, Italy","Neive, Italy","Bra, Italy","Saluzzo, Italy","Pinerolo, Italy","Giaveno, Italy","Carmagnola, Italy","Ivrea, Italy","Mondovi, Italy","Busca, Italy","Poirino, Italy","Santhia, Italy",]
south_italy = ["Savoca, Sicily, Italy","Catania, Sicily, Italy","Cefalu, Sicily, Italy","Caltanissetta, Sicily, Italy","Barrafranca, Sicily, Italy","Mussomeli, Sicily, Italy","Prizzi, Sicily, Italy","Alcamo, Sicily, Italy","Castelvetrano, Sicily, Italy","Lercara Friddi, Sicily, Italy","Valledolmo, Sicily, Italy","Bisacquino, Sicily, Italy","Menfi, Sicily, Italy","Noto, Sicily, Italy","Palagonia, Sicily, Italy","Leonforte, Sicily, Italy","Sciacca, Sicily, Italy","Scicli, Sicily, Italy","Vittoria, Sicily, Italy","Comiso, Sicily, Italy","Rosolini, Sicily, Italy","Racalmuto, Sicily, Italy","Gela, Sicily, Italy","Ravanusa, Sicily, Italy","Campobello di Licata, Sicily, Italy","Favara, Sicily, Italy","Raffadali, Sicily, Italy"]

england = ["Ely, England","Peterborough, England","Thetford, England","Wisbech, England","Spalding, England","King's Lynn, England","Bedford, England","Royston, England","Saffron Walden, England","Bury St Edmunds, England","Stamford, England","Grantham, England","Melton Mowbray, England","Corby, England","Kettering, England","Daventry, England","St Neots, England","Halstead, England","Braintree, England","Colchester, England","Boston, England","Newark-on-Trent, England","Lincoln, England","Gainsborough, England","Scunthorpe, England","North Walsham, England","Luton, England","Rugby, England","Desborough, England","Loughborough, England","Swadlincote, England","Chelmsford, England",]
ruhr = ["Bochum, Germany","Oberhausen, Germany","Gelsenkirchen, Germany","Mulheim, Germany","Bottrop, Germany","Hagen, Germany","Hamm, Germany","Herne, Germany","Witten, Germany","Bergkamen, Germany","Hattingen, Germany","Herten, Germany","Recklinghausen, Germany","Moers, Germany","Dorsten, Germany","Dinslaken, Germany","Castrop-Rauxel, Germany","Gladbeck, Germany","Marl, Germany","Mulheim an der Ruhr, Germany",]

japan = ["Amagasaki, Japan","Kurashiki, Japan","Yokosuka, Japan","Nagasaki, Japan","Hirakata, Japan","Machida, Japan","Gifu-shi, Japan","Fujisawa, Japan","Toyonaka, Japan","Fukuyama, Japan","Toyohashi, Japan","Minato, Japan","Nara-shi, Japan","Toyota, Japan","Nagano, Japan","Iwaki, Japan","Asahikawa, Japan","Takatsuki, Japan","Okazaki, Japan","Suita, Japan","Wakayama, Japan","Koriyama, Japan","Kashiwa, Japan","Tokorozawa, Japan","Kawagoe, Japan","Kochi, Japan","Takamatsu, Japan","Toyama, Japan","Akita, Japan","Koshigaya, Japan","Miyazaki, Japan","Naha, Japan","Kasugai, Japan","Aomori, Japan","Otsu, Japan","Akashi, Japan",]

spain_central_districts = ["Casco Antiguo, Seville, Spain","Centro, Zaragoza, Spain","Centro, Madrid, Spain","Ciutat Vella, Barcelona, Spain","Centro, Malaga, Spain","Murcia, Murcia, Spain","Abando, Bilbao, Spain","Distrito Centro, Gijon, Spain","A Coruna, A Coruna, Spain","Beiro, Granada, Spain","Centro y casco historico, Oviedo, Spain","Centro, Salamanca, Spain",]

from pca import calculate_pca
from util.processing import remove_outliers, standarize

df = remove_outliers(pd.read_csv("./spaind_england_network_orientation.csv", index_col=0))
df = df[['one_way_percentage', 'share_of_separated_streets', 'avg_building_area', 'streets_per_node_avg']]
standarized_df = standarize(df)
standarized_df['is_sicily'] = [True if is_west in south_italy else False for is_west in standarized_df.index]
pcaDf = calculate_pca(df)
k_res = k_means(df)
pcaDf['cluster'] = [True if place in england else False for place in pcaDf.index]
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
