from user import login
import streamlit as st

login.login()

if login.is_logged_in():
    st.switch_page(".\\pages\\chat.py")


