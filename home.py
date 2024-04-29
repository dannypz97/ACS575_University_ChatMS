from user import login
import streamlit as st

st.header('University Chatbot Data Management System', divider='gray')

if not login.is_logged_in():
    st.text('Login to get started.')
    login.login()

    if login.is_logged_in():
        st.switch_page(".\\pages\\chat.py")


