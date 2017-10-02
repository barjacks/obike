
# coding: utf-8

import requests
import pandas as pd
import time
import random
import progressbar
from pygeocoder import Geocoder
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point

date = time.strftime("%Y-%m-%d %H:%M:%S")

response = requests.get('https://mobile.o.bike/api/v1/bike/list?longitude=8.541654869914055&latitude=47.37490008461292')
Lil_data = response.json()
df = pd.DataFrame(Lil_data['data']['list'])
df = df.head(0)

a = 47.310255
b = 47.435697
c = 8.433849
d = 8.635678

# Making 2000 Random locations
lat = []
long = []
for x,y in zip(range(2000), range(2000)):
    lat.append(random.uniform(a,b))
    long.append(random.uniform(c,d))

bar = progressbar.ProgressBar()
for x, y, i in zip(long, lat, bar(range(len(long)))):
    response = requests.get('https://mobile.o.bike/api/v1/bike/list?longitude=' + str(x) +'&latitude='+ str(y))
    Lil_data = response.json()

    df_new = pd.DataFrame(Lil_data['data']['list'])
    frames = [df, df_new]
    df = pd.concat(frames)

df = df.drop_duplicates(keep='first')
df = df.reset_index()

geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
df = df.drop(['longitude', 'latitude'], axis=1)
crs = {'init': 'epsg:4326'}
geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)

geo_df.columns = [['index', 'countyId', 'helmet', 'id', 'imei', date]]

geo_df.to_csv(date + '2000obikesZH.csv')
