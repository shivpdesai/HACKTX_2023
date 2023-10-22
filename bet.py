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
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score

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
        for week in tqdm(weeks, desc = 'fetching'):
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
    pbp = pbp.query("away_conference in ('SEC', 'ACC', 'Big 12', 'Big Ten', 'Pac-12')")

    pbp = pbp.filter(items=['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points', 'start_date', 'week'])

    return pbp


def make_prediction(test):
    trainingData = load_data([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])

    #home field, weather, player quality, player health, starting qb rating, fpi data, power ranking,
    win_factors = ['home_team', 'away_team', 'neutral_site']
    X_train = trainingData[win_factors]
    
    y_train_away = trainingData['away_points']
    y_train_home = trainingData['home_points']
    
    X_test = test[win_factors]

    #One-Hot Encoding
    cat_cols = ['home_team', 'away_team']
    #num_cols = ['home_points', 'away_points']
    bool_cols = ['neutral_site']

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # numeric_transformer = Pipeline(steps=[
    #     ('scaler', StandardScaler())
    # ])

    # For boolean features, you can apply no preprocessing, as they are already binary.
    boolean_transformer = "passthrough"

    preprocessor = ColumnTransformer(
    transformers=[
        #('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols),
        ('bool', boolean_transformer, bool_cols)
    ])

    betting_model_away = RandomForestRegressor(n_estimators=100, random_state=42)
    betting_model_home = RandomForestRegressor(n_estimators=100, random_state=42)

    regression_pipeline_away = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', betting_model_away)
    ])

    regression_pipeline_home = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', betting_model_home)
    ])

    #get away score predictions
    regression_pipeline_away.fit(X_train, y_train_away)
    away_score_pred = regression_pipeline_away.predict(X_test)

    #get home score predictions
    regression_pipeline_home.fit(X_train, y_train_home)
    home_score_pred = regression_pipeline_home.predict(X_test)

    data = {
        'Away': away_score_pred,
        'Home': home_score_pred
    }
    predictions = pd.DataFrame(data)

    return predictions
