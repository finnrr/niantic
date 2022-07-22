import numpy as np
import pandas as pd
import requests
import json
from sklearn_pandas import DataFrameMapper, CategoricalImputer, FunctionTransformer
from poke_values import google_types

#this is not a working part of the app, just expanding on the data given.

#load cvs data file, setup in pandas dataframe
df = pd.read_csv('data/pokemon_go.csv')
df['city'].unique()
df = df[df['city']=='Toronto']
df.reset_index(inplace=True)
df.drop('index',axis=1, inplace=True)
df['google_types'] = ''

#quick exploration of data
df
len(google_types)

#get a google location type from latitude/longitude.
def scrape_place(lat, long):
    base_url = "https://maps.googleapis.com/maps/api/place/search/json?location="
    key = ""
    complete_url = base_url +  f'{lat}' + "," + f'{long}' + "&radius=100&key=" + key
    response = requests.get(complete_url)
    x = response.json()
    y = x['results']
    y
    types = set([])
    for i in y:
        for h in i['types']:
            if h in google_types:
                types.add(h)
    return list(types)

#testing above   
google_types
place_ = scrape_place(43.770318,-79.212555)
place_

#make a dataframe transformer for location to location type
def list_place(dfx,i):
    x = dfx.latitude[i]
    y = dfx.longitude[i]
    df['google_types'][i] = scrape_place(x, y)


#transform values in dataframe
list_place(df,1)
for rows in range(len(df)):
    list_place(df,rows)

#view results
df
df.iloc[[3581]]
df.shape

#fix value back to row
len(df)
for row in range(len(df)):
    list_place(df,row)
df

#write to new cvs file
df.to_csv('scraped_df2.csv', index_label=False)



#old workings 

# pd.read_csv('scraped_df.csv')
#
# pd.set_option('display.max_columns', 500)
# list_place(df,17)
# df['pokedex_id'][1]


#for i in df.index:
#    list_place(df,-79.211497 i)
# ​
# df1 = df.copy(deep=True)
# df1.head()
# ​
# r = pd.DataFrame({
#       col:np.repeat(df1[col].values, df1[google_types].str.len())
#       for col in df1.columns.drop(google_types)}
#     ).assign(**{google_types:np.concatenate(df1[google_types].values)})[df1.columns]
# ​
# df1['list'] = 1
# mapper = DataFrameMapper([
#      #('latitude', None),
#      #('longitude',None),
#      #('hour', LabelBinarizer()),
#      #('day', LabelBinarizer()),
#      #('close_to_water', LabelEncoder()),
#      # ('city',LabelBinarizer()),
#      #('weather',LabelBinarizer()),
#      #(['temperature'],StandardScaler()),
#      # (['population_density'], StandardScaler()),
#      ], df_out=True)
# ​
# Z_train = mapper.fit_transform(X_train)
# Z_test = mapper.transform(X_test)
# ​
