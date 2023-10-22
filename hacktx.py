import streamlit as st
from bet import load_data
from bet import make_prediction
import pandas as pd
import numpy as np
import math


@st.cache_data
def team_schedule(name):
    df_2023 = load_data([2023])
    home_schedule = df_2023[df_2023["home_team"] == name]
    away_schedule = df_2023[df_2023["away_team"] == name]
    team_schedule = pd.concat([away_schedule, home_schedule])
    team_schedule = team_schedule.sort_values(by=['week'])
    return team_schedule

def is_played(schedule):
    played = []
    for game in schedule.iterrows():
        if math.isnan(game[1]['home_points']):
            played.append(False)
        else:
            played.append(True)

    return played

def is_not_played(schedule):
    played = []
    for game in schedule.iterrows():
        if math.isnan(game[1]['home_points']):
            played.append(True)
        else:
            played.append(False)

    return played

def winPCT_played(played, team):
    winPCT = []
    weeks = 0
    wins = 0

    for game in played.iterrows():
        weeks = weeks + 1
        if (game[1]['home_team'] == team):
            if game[1]['home_points'] > game[1]['away_points']:   
                wins = wins + 1

            
        if (game[1]['away_team'] == team):
            if game[1]['home_points'] < game[1]['away_points']:   
                wins = wins + 1
        
        winPCT.append(wins/weeks)
    
    winPCT.insert(0, 1.0)
    return winPCT

def winPCT_played(played, team):
    winPCT = []
    weeks = 0
    wins = 0

    for game in played.iterrows():
        weeks = weeks + 1
        if (game[1]['home_team'] == team):
            if game[1]['home_points'] > game[1]['away_points']:   
                wins = wins + 1 
        if (game[1]['away_team'] == team):
            if game[1]['home_points'] < game[1]['away_points']:   
                wins = wins + 1
        
        winPCT.append(wins/weeks)
    
    return winPCT

def winPCT_to_play(played, team, pred):
    winPCT = []
    weeks = 0
    wins = 0

    for game in played.iterrows():
        weeks = weeks + 1
        i = weeks -1
        if (game[1]['home_team'] == team):
            if (game[1]['is_played']):
                if game[1]['home_points'] > game[1]['away_points']:   
                    wins = wins + 1
            else:
                if pred['Home'][i] > pred['Away'][i]:   
                    wins = wins + 1
                winPCT.append(wins/weeks)

        if (game[1]['away_team'] == team):
            if (game[1]['is_played']):
                if game[1]['home_points'] < game[1]['away_points']:   
                    wins = wins + 1
            else:
                if pred['Home'][i] < pred['Away'][i]:   
                    wins = wins + 1
                winPCT.append(wins/weeks)
        
    return winPCT

def makeGraph(team):
    schedule = team_schedule(team)

    played = is_played(schedule)
    schedule['is_played'] = played

    predictions = make_prediction(schedule)

    played_weeks = (schedule['is_played'] == True).sum()
    not_played_weeks = schedule.shape[0] - played_weeks

    winPCTS_played = winPCT_played(schedule, team)
    winPCTS_played = winPCTS_played[:played_weeks]
    for i in range(not_played_weeks):
        winPCTS_played.append(np.nan)
    
    winPCTS_to_play = winPCT_to_play(schedule, team, predictions)
    for i in range(played_weeks):
        winPCTS_to_play.insert(0,np.nan)
    winPCTS_to_play[played_weeks - 1] = winPCTS_played[played_weeks - 1]
    
    schedule['winPCT_played'] = winPCTS_played
    schedule['winPCT_to_played'] = winPCTS_to_play

    weeks = []
    for i in range(schedule.shape[0]):
        weeks.append(i+1)
    
    data = {
        'week': weeks,
        'played': schedule['winPCT_played'], 
        'predictions': schedule['winPCT_to_played']}

    df = pd.DataFrame(data)

    return df

def comp_games(team):
    schedule = team_schedule(team)
    play = is_played(schedule)
    schedule['is_played'] = play
    schedule = schedule[schedule['is_played'] == True]


    return schedule
    

def future_games(team):
    schedule = team_schedule(team)
    play = is_played(schedule)
    schedule['is_played'] = play
    schedule = schedule[schedule['is_played'] == False]
    preds = make_prediction(schedule)
    away = preds['Away'].values
    home = preds['Home'].values

    schedule['away_pred'] = away
    schedule['home_pred'] = home

    return schedule