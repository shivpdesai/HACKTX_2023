import streamlit as st
from bet import load_data
from bet import make_prediction

st.title("Betting App")

df_2023 = load_data([2023])
predictions = make_prediction(df_2023)

selected_tab = st.radio("Select a category:", ["Category 1", "Category 2", "Category 3"])

st.table(df_2023)
user_input = st.text_input("Enter your name")


#####################
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
headers = {"Authorization": api_key}

# year = 2019
weeks = list(range(0, 16))
conference = {'SEC', 'ACC', 'Big_12', 'Big_10', 'Pac-12'}


@st.cache_data
def load_data(year):
    pbp_req = []
    pbp = pd.DataFrame()

    for yr in year:
        for week in weeks:
            parameters = {"year": yr, "week": week}
            pbp_req = requests.get("https://api.collegefootballdata.com/games",
                                   params=parameters,
                                   headers=headers)
            try:
                x = pd.DataFrame(json.loads(pbp_req.text))
                pbp = pd.concat([pbp, x])
            except IndexError:
                print('error')
                pass
            continue

    pbp = pbp.query("away_conference in ('SEC', 'ACC', 'Big 12', 'Big Ten', 'Pac-12')")
    pbp = pbp.filter(items=['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points'])
    return pbp

'''
trainingData = load_data([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
df_2022 = load_data([2022])

st.table(trainingData.head())

y_home_train = trainingData.home_points
y_away_train = trainingData.away_points

# home field, weather, player quality, player health, starting qb rating, fpi data, power ranking,
win_factors = ['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points']
X_train = trainingData[win_factors]
X_test = df_2022['home_team', 'away_team', 'neutral_site', 'home_points', 'away_points']

betting_model_home = DecisionTreeRegressor(random_state=1)
betting_model_away = DecisionTreeRegressor(random_state=1)

betting_model_home.fit(X_train, y_home_train)
betting_model_away.fit(X_train, y_away_train)
'''

#st.table((load_data([2023])))
data = load_data([2023])
#data1 = data.dropna(subset=['home_points'])
data1 = data[data['home_points'].isna()]
#st.table(data1)
st.title("My app")
user_input = st.text_input("Enter your name")

# Add a button widget
if st.button("Submit"):
    st.write(f"Hello, {user_input}!")
    # load data is all college football data for 2023



#'''
for index, row in data.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']
    st.markdown(f"""
    <div style="width: 200px; height: 200px; background-color: #FF5733; text-align: center; border-radius: 10px; position: relative; display:inline-block;">
        <div style="position: absolute; top: 35px; left: 0; width: 100%;justify-content: space-between;">
            <span style="font-size: 16px;">{home_team} vs {away_team}</span>
        </div>
        <hr style="position: absolute; width: 100%; top: 50%; margin-top: -1px; border: 2px solid #000;">
        <div style="position: absolute; bottom: 25px; left: 0; width: 100%;">
            <span style="font-size: 16px;">Date: Oct 21 @ 6 pm</span>
            <span style="font-size: 16px;">Location: Oracle Arena</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

#'''





'''
st.markdown("""
<div style="width: 200px; height: 200px; background-color: #FF5733; text-align: center; border-radius: 10px; position: relative;">
    <div style="position: absolute; top: 35px; left: 0; width: 100%;">
        <span style="font-size: 18px;">Team A vs Team B</span>
    </div>
    <hr style="position: absolute; width: 100%; top: 50%; margin-top: -1px; border: 2px solid #000;">
    <div style="position: absolute; bottom: 25px; left: 0; width: 100%;">
        <span style="font-size: 16px;">Date: Oct 21 @ 6 pm</span><br>
        <span style="font-size: 16px;">Location: Oracle Arena</span>
    </div>
</div>
""", unsafe_allow_html=True)
'''

