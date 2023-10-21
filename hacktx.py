import streamlit as st
from bet import load_data
from bet import make_prediction

st.title("Betting App")

df_2023 = load_data([2023])
predictions = make_prediction(df_2023)

selected_tab = st.radio("Select a category:", ["Category 1", "Category 2", "Category 3"])

st.table(df_2023)
user_input = st.text_input("Enter your name")
