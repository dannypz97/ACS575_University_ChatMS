import streamlit as st

from user import session

if session.is_logged_in():
    session.logout()

st.switch_page("home.py")
