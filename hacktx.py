import streamlit as st
from bet import load_data
from bet import make_prediction
import pandas as pd
import numpy as np

st.title("Betting App")

df_2023 = load_data([2023])


predictions = make_prediction(df_2023)

@st.cache_data
def team_schedule(name):
    home_schedule = df_2023[df_2023["home_team"] == name]
    away_schedule = df_2023[df_2023["away_team"] == name]
    team_schedule = pd.concat([away_schedule, home_schedule])
    team_schedule = team_schedule.sort_values(by=['week'])
    return team_schedule

def is_played(schedule):
    played = []
    for game in schedule.iterrows():
        if game['home_points'].empty:
            played.concat(False)
        else:
            played.concat(True)

    return played

schedule = team_schedule('Texas')
played = is_played(schedule)
print(played)


st.table(schedule)

