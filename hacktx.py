import streamlit as st
st.title("My app")

user_input = st.text_input("Enter your name")

# Add a button widget
if st.button("Submit"):
    st.write(f"Hello, {user_input}!")
    # load data is all college football data for 2023


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


