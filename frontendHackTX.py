import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm as tqdm
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score

api_key = "Bearer x/c+JqSij5h1DddsMFpx2s35cXs49Xb9wUh0Sya02hnWui1jb/fqkEMKjHPVhTxv"
headers = {"Authorization": api_key}

# year = 2019
weeks = list(range(0, 16))
conference = {'SEC', 'ACC', 'Big_12', 'Big_10', 'Pac-12'}

st.markdown(
    """
    <style>
        body {
            background-color: black; /* Set the background color to black */
        }
        .nav-container {
            display: flex;
            flex-direction: column;
        }
        .nav-row {
            display: flex;
            justify-content: center;
        }
        .nav-title {
            font-size: 18px;
            margin: 10px 0;
            color: white; /* Set the text color of the titles to white */
        }
        .nav-button {
            display: inline-block;
            width: 100px;
            height: 100px;
            text-align: center;
            line-height: 100px;
            text-decoration: none;
            color: white;
            margin: 10px;
            border: none;
            border-radius: 5px;
        }

        .button-blue {
            background-color: #0074d9; /* Blue */
        }

        .button-green {
            background-color: #2ecc40; /* Green */
        }

        .button-red {
            background-color: #ff4136; /* Red */
        }

        .button-purple {
            background-color: #b10dc9; /* Purple */
        }

        .button-orange {
            background-color: #ff8c00; /* Orange */
        }

        /* first row*/

        .button-bc {

            background-color: #98002E ;
        }

        .button-clemson {
            background-color: #F56600;
        }

        .button-duke {
            background-color: #00539B;
        }

        .button-fsu {
            background-color: #782F40;
        }

        .button-gt {
            background-color: #B3A369;
        }

        /*second row*/

        .button-louisville {

            background-color: #AD0000 ;
        }

        .button-miami {
            background-color: #F47321;
        }

        .button-NorthC {
            background-color: #7BAFD4;
        }

        .button-NC {
            background-color: #CC0000;
        }

        .button-Pitt {
            background-color: #FFB81C;
        }

        /*third row*/

        .button-syracuse {
            background-color: #F76900;
        }

        .button-virginia {
            background-color:  #F84C1E;
        }

        .button-vatech {
            background-color: #630031;
        }

        .button-wf {
            background-color: #9E7E38;
        }

        /*first row*/

        .button-illinios {

            background-color: #E84A27 ;
        }

        .button-indiana {
            background-color: #990000;
        }

        .button-iowa {
            background-color: #FFCD00;
        }

        .button-maryland {
            background-color: #E03A3E;
        }

        .button-michigan {
            background-color: #FFCB05 ;
        }

        /*second row*/

        .button-michstate {

            background-color: #18453B;
        }

        .button-minnesota {
            background-color: #7A0019;
        }

        .button-nebraska {
            background-color: #E41C38;
        }

        .button-northwestern {
            background-color: #4E2A84;
        }

        .button-osu {
            background-color: #BB0000;
        }

        /*third row*/

        .button-penn {

            background-color: #041E42 ;
        }

        .button-purdue {
            background-color: #CEB888;
        }

        .button-rut{
            background-color: #CC0033;
        }

        .button-wis {
            background-color: #C5050C;
        }

        /*first row*/

        .button-baylor {

            background-color: #154734 ;
        }

        .button-byu {
            background-color: #002E5D;
        }

        .button-cinn {
            background-color: #000000;
        }

        .button-uh {
            background-color:  #c8102e;
        }

        .button-iowastate {
            background-color: #C8102E ;
        }

        /*second row*/

        .button-kansas {

            background-color: #0051BA;
        }

        .button-kstate {
            background-color: #512888 ;
        }

        .button-oklahoma {
            background-color: #841617;
        }

        .button-oklastate {
            background-color: #FF7300;
        }

        .button-TCU {
            background-color: #4D1979;
        }

        /*third row*/

        .button-texas {

            background-color: #BF5700;
        }

        .button-ttech {

            background-color: #CC0000;
        }

        .button-ucf {
            background-color: #FFC904;
        }

        .button-wvu {
            background-color: #002855;
        }

        /*first row*/

        .button-ariz {

            background-color: #CC0033;
        }

        .button-astate {
            background-color: #8C1D40 ;
        }

        .button-cal {
            background-color:  #003262;
        }

        .button-ucla {
            background-color: #2D68C4;
        }

        .button-col {
            background-color: #CFB87C;
        }

        .button-ore {

            background-color: #154733;
        }

        /*second row*/

        .button-ostate {

            background-color:  #DC4405;
        }

        .button-usc {
            background-color: #990000 ;
        }

        .button-stanford {
            background-color: #8C1515;
        }

        .button-utah {
            background-color: #808080;
        }

        .button-wash {
            background-color: #4B2E83;
        }

        .button-WSU {

            background-color: #981E32;
        }

        /*first row*/

        .button-bama {

            background-color: #9E1B32  ;
        }

        .button-arkansas {
            background-color: #9D2235;
        }

        .button-aub {
            background-color: #a52a2a;
        }

        .button-flor {
            background-color:  #0021A5;
        }

        .button-geor {
            background-color: #BA0C2F;
        }

        /*second row*/

        .button-kent {

            background-color: #0033A0;
        }

        .button-LSU {
            background-color: 	#461D7C;
        }

        .button-Ole {
            background-color:  #14213D;
        }

        .button-MSU {
            background-color:  #660000;
        }

        .button-Miss {
            background-color: #F1B82D;
        }

        /*third row*/

        .button-SC {

            background-color:  #73000A ;
        }

        .button-tenn {
            background-color:  #FF8200;
        }

        .button-TAMU {
            background-color: #500000;
        }

        .button-vandy {
            background-color:  #866D4B;
        }

        .centered-row {
            justify-content: center;
        }

        header {
            color: white; /* Set the text color of the header to white */
        }
    </style>
    """,
    unsafe_allow_html=True
)


def display_html_content(html_file):
    with open(html_file, "r") as file:
        html_content = file.read()
    st.markdown(html_content, unsafe_allow_html=True)


# Define the main page content
def home():
    st.title("Home Page")
    st.write("Welcome to the Scoreboard Savant!")
    st.write("Click a button to navigate to another page.")


# Define Page 1 content
def acc():
    st.title("ACC")
    st.markdown('''
    <nav class="nav-container">
        <div class="nav-row">
            <a href="page1.html" class="nav-button button-bc">Boston College</a>
            <a href="page2.html" class="nav-button button-clemson">Clemson</a>
            <a href="page3.html" class="nav-button button-duke">Duke</a>
            <a href="page4.html" class="nav-button button-fsu">Florida State</a>
            <a href="page5.html" class="nav-button button-gt">Georgia Tech</a>
        </div>
    </nav>
''', unsafe_allow_html=True)
    st.markdown('''
    <nav class="nav-container">
        <div class="nav-row">
            <a href="page5.html" class="nav-button button-louisville">Louisville</a>
            <a href="page6.html" class="nav-button button-miami">Miami (FL)</a>
            <a href="page7.html" class="nav-button button-NorthC">North Carolina</a>
            <a href="page8.html" class="nav-button button-NC">NC State</a>
            <a href="page5.html" class="nav-button button-Pitt">Pittsburgh</a>
        </div>
    </nav>
    ''', unsafe_allow_html=True)
    st.markdown('''
        <nav class="nav-container">
            <div class="nav-row centered-row">
            <a href="page5.html" class="nav-button button-syracuse">Syracuse</a>
            <a href="page6.html" class="nav-button button-virginia">Virginia</a>
            <a href="page7.html" class="nav-button button-vatech">Virginia Tech</a>
            <a href="page8.html" class="nav-button button-wf">Wake Forest</a>
        </div>
        </nav>
        ''', unsafe_allow_html=True)


# Define Page 2 content
def big10():
    st.title("Big 10")
    st.markdown('''
            <nav class="nav-container">
                <div class="nav-row">
            <a href="page5.html" class="nav-button button-illinios">Illinios</a>
            <a href="page6.html" class="nav-button button-indiana">Indiana</a>
            <a href="page7.html" class="nav-button button-iowa">Iowa</a>
            <a href="page8.html" class="nav-button button-maryland">Maryland</a>
            <a href="page5.html" class="nav-button button-michigan">Michigan</a>
        </div>
            </nav>
            ''', unsafe_allow_html=True)
    st.markdown('''
                <nav class="nav-container">
                    <div class="nav-row">
            <a href="page5.html" class="nav-button button-michstate">Michigan State</a>
            <a href="page6.html" class="nav-button button-minnesota">Minnesota</a>
            <a href="page7.html" class="nav-button button-nebraska">Nebraska</a>
            <a href="page8.html" class="nav-button button-northwestern">Northwestern</a>
            <a href="page5.html" class="nav-button button-osu">Ohio State</a>
        </div>
                </nav>
                ''', unsafe_allow_html=True)
    st.markdown('''
                <nav class="nav-container">
                    <div class="nav-row">
            <a href="page5.html" class="nav-button button-penn">Penn State</a>
            <a href="page6.html" class="nav-button button-purdue">Purdue</a>
            <a href="page7.html" class="nav-button button-rut">Rutgers</a>
            <a href="page8.html" class="nav-button button-wis">Wisconson</a>
        </div>
                </nav>
                ''', unsafe_allow_html=True)


# Define Page 3 content
def big12():
    st.title("Big 12")
    st.markdown('''
                    <nav class="nav-container">
                        <div class="nav-row">
            <a href="page5.html" class="nav-button button-baylor">Baylor</a>
            <a href="page6.html" class="nav-button button-byu">BYU</a>
            <a href="page7.html" class="nav-button button-cinn">Cincinnati</a>
            <a href="page8.html" class="nav-button button-uh">Houston</a>
            <a href="page5.html" class="nav-button button-iowastate">Iowa State</a>
        </div>
                    </nav>
                    ''', unsafe_allow_html=True)
    st.markdown('''
                    <nav class="nav-container">
                        <div class="nav-row">
            <a href="page5.html" class="nav-button button-kansas">Kansas</a>
            <a href="page6.html" class="nav-button button-kstate">Kansas State</a>
            <a href="page7.html" class="nav-button button-oklahoma">Oklahoma</a>
            <a href="page7.html" class="nav-button button-oklastate">OSU</a>
            <a href="page8.html" class="nav-button button-TCU">TCU</a>

        </div>
                    </nav>
                    ''', unsafe_allow_html=True)
    st.markdown('''
                    <nav class="nav-container">
                        <div class="nav-row">
            <a href="Texas.html" class="nav-button button-texas">Texas</a>
            <a href="page5.html" class="nav-button button-ttech">Texas Tech</a>
            <a href="page6.html" class="nav-button button-ucf">UCF</a>
            <a href="page7.html" class="nav-button button-wvu">West Virginia</a>
        </div>
                    </nav>
                    ''', unsafe_allow_html=True)


def pac12():
    st.title("Pac 12")
    st.markdown('''
                        <nav class="nav-container">
                            <div class="nav-row">
            <a href="page5.html" class="nav-button button-ariz">Arizona</a>
            <a href="page6.html" class="nav-button button-astate">Arizona State</a>
            <a href="page7.html" class="nav-button button-cal">California</a>
            <a href="page8.html" class="nav-button button-ucla">UCLA</a>
            <a href="page5.html" class="nav-button button-col">Colarado</a>
            <a href="page5.html" class="nav-button button-ore">Oregon</a>
        </div>
                        </nav>
                        ''', unsafe_allow_html=True)
    st.markdown('''
                        <nav class="nav-container">
                            <div class="nav-row">
            <a href="page6.html" class="nav-button button-ostate">Oregon State</a>
            <a href="page7.html" class="nav-button button-usc">USC</a>
            <a href="page8.html" class="nav-button button-stanford">Stanford</a>
            <a href="page5.html" class="nav-button button-utah">Utah</a>
            <a href="page5.html" class="nav-button button-wash">Washington</a>
            <a href="page5.html" class="nav-button button-WSU">WSU</a>
        </div>
                        </nav>
                        ''', unsafe_allow_html=True)


def sec():
    st.title("SEC")
    st.markdown('''
                        <nav class="nav-container">
                            <div class="nav-row">
            <a href="page6.html" class="nav-button button-bama">Alabama</a>
            <a href="page7.html" class="nav-button button-arkansas">Arkansas</a>
            <a href="page8.html" class="nav-button button-aub">Auburn</a>
            <a href="page5.html" class="nav-button button-flor">Florida</a>
            <a href="page5.html" class="nav-button button-geor">Georgia</a>
        </div>
                        </nav>
                        ''', unsafe_allow_html=True)
    st.markdown('''
                        <nav class="nav-container">
                            <div class="nav-row">
            <a href="page6.html" class="nav-button button-kent">Kentucky</a>
            <a href="page7.html" class="nav-button button-LSU">LSU</a>
            <a href="page8.html" class="nav-button button-Ole">Ole Miss</a>
            <a href="page5.html" class="nav-button button-MSU">MSU</a>
            <a href="page5.html" class="nav-button button-Miss">Missouri</a>
        </div>
                        </nav>
                        ''', unsafe_allow_html=True)
    st.markdown('''
            <nav class="nav-container">
                <div class="nav-row">
            <a href="page6.html" class="nav-button button-SC">South Carolina</a>
            <a href="page7.html" class="nav-button button-tenn">Tennessee</a>
            <a href="page8.html" class="nav-button button-TAMU">Texas A&M</a>
            <a href="page5.html" class="nav-button button-vandy">Vanderbilt</a>
        </div>
        </nav>
                        ''', unsafe_allow_html=True)



# Sidebar navigation
page = st.sidebar.radio("Select a page", ["Home", "ACC", "Big 10", "Big 12", "Pac 12", "SEC","Graph"])

# Display the selected page based on the choice
if page == "Home":
    home()
elif page == "ACC":
    acc()
elif page == "Big 10":
    big10()
elif page == "Big 12":
    big12()
elif page == "Pac 12":
    pac12()
elif page == "SEC":
    sec()
elif page == "Graph":
    pic()