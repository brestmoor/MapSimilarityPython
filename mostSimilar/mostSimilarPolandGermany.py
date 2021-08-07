import pandas as pd

from most_similar import find_most_similar_in_df

germany = ["Cologne, Germany","Frankfurt am Main, Germany","Stuttgart, Germany","Dusseldorf, Germany","Dortmund, Germany","Essen, Germany","Leipzig, Germany","Bremen, Germany","Dresden, Germany","Hanover, Germany","Nuremberg, Germany","Duisburg, Germany","Bochum, Germany","Wuppertal, Germany","Bielefeld, Germany","Bonn, Germany","Munster, Germany","Karlsruhe, Germany","Mannheim, Germany","Augsburg, Germany","Wiesbaden, Germany","Gelsenkirchen, Germany","Monchengladbach, Germany","Braunschweig, Germany","Chemnitz, Germany","Kiel, Germany","Aachen, Germany","Halle, Germany","Magdeburg, Germany","Freiburg im Breisgau, Germany","Krefeld, Germany","Lubeck, Germany","Oberhausen, Germany","Erfurt, Germany","Mainz, Germany","Rostock, Germany","Kassel, Germany","Hagen, Germany","Hamm, Germany","Saarbrucken, Germany","Mulheim an der Ruhr, Germany","Potsdam, Germany","Ludwigshafen am Rhein, Germany","Oldenburg, Germany","Leverkusen, Germany","Osnabruck, Germany","Solingen, Germany","Heidelberg, Germany","Herne, Germany","Neuss, Germany","Darmstadt, Germany","Paderborn, Germany","Regensburg, Germany","Ingolstadt, Germany","Wurzburg, Germany","Fürth, Germany","Wolfsburg, Germany","Offenbach am Main, Germany","Ulm, Germany","Heilbronn, Germany","Pforzheim, Germany","Gottingen, Germany","Bottrop, Germany","Trier, Germany","Recklinghausen, Germany","Reutlingen, Germany","Bremerhaven, Germany","Koblenz, Germany","Bergisch Gladbach, Germany","Jena, Germany","Remscheid, Germany","Erlangen, Germany","Moers, Germany","Siegen, Germany","Hildesheim, Germany","Salzgitter, Germany","Kaiserslautern, Germany",]
poland = ["Krakow, Poland", "lodz, Poland", "Wroclaw, Poland", "Poznań, Poland", "Gdańsk, Poland", "Szczecin, Poland", "Bydgoszcz, Poland", "Lublin, Poland", "Bialystok, Poland", "Katowice, Poland", "Gdynia, Poland", "Czestochowa, Poland", "Radom, Poland", "Torun, Poland", "Sosnowiec, Poland", "Rzeszow, Poland", "Kielce, Poland", "Gliwice, Poland", "Olsztyn, Poland", "Zabrze, Poland", "Bielsko-Biala, Poland", "Bytom, Poland", "Zielona Gora, Poland", "Rybnik, Poland", "Ruda slaska, Poland", "Opole, Poland", "Tychy, Poland", "Gorzow Wielkopolski, Poland", "Elblag, Poland", "Plock, Poland", "Dabrowa Gornicza, Poland", "Walbrzych, Poland", "Wloclawek, Poland", "Tarnow, Poland", "Chorzow, Poland", "Koszalin, Poland", "Kalisz, Poland", "Legnica, Poland", "Grudziadz, Poland", "Jaworzno, Poland", "Slupsk, Poland", "Jastrzebie Zdroj, Poland", "Nowy Sacz, Poland", "Jelenia Gora, Poland", "Siedlce, Poland", "Myslowice, Poland", "Konin, Poland", "Pila, Poland", "Piotrkow Trybunalski, Poland", "Inowroclaw, Poland", "Lubin, Poland", "Ostrow Wielkopolski, Poland", "Suwalki, Poland", "Ostrowiec Swietokrzyski, Poland", "Gniezno, Poland", "Stargard, Poland", "Glogow, Poland", "Siemianowice Slaskie, Poland", "Pabianice, Poland", "Leszno, Poland", "Zamosc, Poland", "Lomza, Poland", "Zory, Poland", "Pruszkow, Poland", "Elk, Poland", "Tarnowskie Gory, Poland", "Tomaszow Mazowiecki, Poland", "Chelm, Poland", "Przemysl, Poland", "Kedzierzyn-Kozle, Poland", "Mielec, Poland", "Stalowa Wola, Poland", "Tczew, Poland", "Biala Podlaska, Poland", "Belchatow, Poland", "Swidnica, Poland", "Bedzin, Poland", "Zgierz, Poland", "Piekary Slaskie, Poland", "Raciborz, Poland"]

df = pd.read_csv("../out/poland_germany_streets_top80.csv", index_col=0)
df = df.dropna()

print(find_most_similar_in_df([poland, germany], df, 'pearson', True))