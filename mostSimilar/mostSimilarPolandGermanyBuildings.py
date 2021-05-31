import pandas as pd
from mostSimilar.mostSimilarCitiesFinder import find_most_similar_in_df

germany = [ "Hanover, Germany","Bremen, Germany","Dortmund, Germany","Frankfurt, Germany","Leipzig, Germany","Dresden, Germany","Nuremberg, Germany","Stuttgard, Germany","Magdeburg, Germany","Kassel, Germany","Munster, Germany","Bonn, Germany","Stuttgart, Germany","Chemnitz, Germany","Wolfsburg, Germany","Osnabruck, Germany","Brunswick, Germany","Mannheim, Germany","Heidelberg, Germany","Wuppertal, Germany","Monchengladbach, Germany","Aachen, Germany","Duren, Germany","Erfurt, Germany","Rheine, Germany","Neubrandenburg, Germany","Greifswald, Germany","Lubeck, Germany","Mainz, Germany","Wurzburg, Germany","Augsburg, Germany","Regensburg, Germany"]
poland = ["Lodz, Poland","Krakow, Poland","Wroclaw, Poland","Poznan, Poland","Gdansk, Poland","Szczecin, Poland","Bydgoszcz, Poland","Lublin, Poland","Katowice, Poland","Bialystok, Poland","Gdynia, Poland","Czestochowa, Poland","Torun, Poland","Gliwice, Poland","Zabrze, Poland","Bytom, Poland","Kielce, Poland","Rzeszow, Poland","Gorzow Wielkopolski, Poland","Opole, Poland","Sopot, Poland","Bielsko-Biala, Poland","Plock, Poland","Koszalin, Poland","Tarnow, Poland","Siedlce, Poland","Olsztyn, Poland",]

df = pd.read_csv("../poland_germany_buildings_most_similar.csv", index_col=0)
df = df.dropna()

find_most_similar_in_df([poland, germany], df)