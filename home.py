from user import session
import streamlit as st

st.header('University Chatbot Data Management System', divider='gray')

if not session.is_logged_in():
    st.text('Login to get started.')
    session.login()

    if session.is_logged_in():
        st.switch_page(".\\pages\\chat.py")


