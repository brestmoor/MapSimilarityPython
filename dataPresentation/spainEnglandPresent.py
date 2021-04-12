import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataPresentation.plotting import plot_points_with_coloring
from pca import calculate_pca


from util.processing import standarize

england = ["Ely, England","Peterborough, England","Thetford, England","Wisbech, England","Spalding, England","King's Lynn, England","Bedford, England","Royston, England","Saffron Walden, England","Bury St Edmunds, England","Stamford, England","Grantham, England","Melton Mowbray, England","Corby, England","Kettering, England","Daventry, England","St Neots, England","Halstead, England","Braintree, England","Colchester, England","Boston, England","Newark-on-Trent, England","Lincoln, England","Gainsborough, England","Scunthorpe, England","North Walsham, England","Luton, England","Rugby, England","Desborough, England","Loughborough, England","Swadlincote, England","Chelmsford, England",]

df = pd.read_csv("../spain_england_osm_de.csv", index_col=0)
df = df[[
    'one_way_percentage',
    'share_of_separated_streets',
    'streets_in_radius_of_100_m',
    'streets_per_node_avg'
]]

df = df.dropna()
pcaDf = calculate_pca(df)
pcaDf['cluster'] = [True if place in england else False for place in pcaDf.index]

plot_points_with_coloring(pcaDf)

