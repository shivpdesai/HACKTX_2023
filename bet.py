import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm as tqdm
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

st.title("Sports Betting")

api_key = "Bearer x/c+JqSij5h1DddsMFpx2s35cXs49Xb9wUh0Sya02hnWui1jb/fqkEMKjHPVhTxv"
headers = {"Authorization" : api_key}

#year = 2019
weeks = list(range(0,16))
conference = {'SEC', 'ACC', 'Big_12', 'Big_10', 'Pac-12'}


@st.cache_data
def load_data(year):

    pbp_req = []
    pbp = pd.DataFrame()

    for yr in year:
        for week in weeks:
            parameters = {"year":yr, "week":week}
            pbp_req = requests.get("https://api.collegefootballdata.com/games", 
                                params = parameters, 
                                headers = headers)
            try:
                x = pd.DataFrame(json.loads(pbp_req.text))
                pbp =  pd.concat([pbp,x])
            except IndexError:
                print('error')
                pass
            continue

    
    pbp = pbp.query("away_conference in ('SEC', 'ACC', 'Big 12', 'Big Ten', 'Pac-12')")
    pbp = pbp.filter(items=['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points'])
    return pbp

trainingData = load_data([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
df_2022 = load_data([2022])


st.table(trainingData.head())

y_home_train = trainingData.home_points
y_away_train = trainingData.away_points

#home field, weather, player quality, player health, starting qb rating, fpi data, power ranking,
win_factors = ['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points']
X_train = trainingData[win_factors]
X_test = df_2022['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points']

betting_model_home = DecisionTreeRegressor(random_state=1)
betting_model_away = DecisionTreeRegressor(random_state=1)

betting_model_home.fit(X_train, y_home_train)
betting_model_away.fit(X_train, y_away_train)