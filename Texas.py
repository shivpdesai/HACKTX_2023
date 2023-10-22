import streamlit as st
from hacktx import makeGraph

def display_html_content(html_file):
    with open(html_file, "r") as file:
        html_content = file.read()
    st.markdown(html_content, unsafe_allow_html = True)
    df = makeGraph('Texas')
    st.area_chart(df, x='week', y=['played', 'predictions'])

display_html_content("Texas.html")