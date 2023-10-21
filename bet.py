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

    pbp = pbp.filter(items=['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points'])

    return pbp

trainingData = load_data([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
df_2022 = load_data([2022])

st.table(trainingData)

#home field, weather, player quality, player health, starting qb rating, fpi data, power ranking,
win_factors = ['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points']
X_train = trainingData[win_factors]
X_test = df_2022[win_factors]
y_train_away = trainingData['away_points']
y_test_away = df_2022['away_points']


#One-Hot Encoding
cat_cols = ['home_team', 'away_team']
num_cols = ['home_points', 'away_points']
bool_cols = ['neutral_site']

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

    # For boolean features, you can apply no preprocessing, as they are already binary.
boolean_transformer = "passthrough"

preprocessor = ColumnTransformer(
transformers=[
    ('num', numeric_transformer, num_cols),
    ('cat', categorical_transformer, cat_cols),
    ('bool', boolean_transformer, bool_cols)
])

betting_model_away = RandomForestRegressor(n_estimators=100, random_state=42)

regression_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', betting_model_away)
])

regression_pipeline.fit(X_train, y_train_away)

away_score_pred = regression_pipeline.predict(X_test)

st.table(away_score_pred)

mse = mean_squared_error(y_test_away, away_score_pred)

print("Mean Squared Error: ", mse)

#########


#st.table((load_data([2023])))
data = load_data([2023])
# data1 is the cleaned up dataset for future games
data1 = data[data['home_points'].isna()]

# creating the boxes for eat future game. 
for index, row in data.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']
    st.markdown(f"""
    <div style="width: 200px; height: 200px; background-color: #FF5733; text-align: center; border-radius: 10px;
     position: relative; display:inline-block">
        <div style="position: absolute; top: 35px; left: 0; width: 100%;">
            <span style="font-size: 16px;">{home_team} vs {away_team}</span>
        </div>
        <hr style="position: absolute; width: 100%; top: 50%; margin-top: -1px; border: 2px solid #000;">
        <div style="position: absolute; bottom: 25px; left: 0; width: 100%;">
            <span style="font-size: 16px;">Date: Oct 21 @ 6 pm</span><br>
            <span style="font-size: 16px;">Location: Oracle Arena</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
