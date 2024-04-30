from user import session
import streamlit as st

st.header('University Chatbot Data Management System', divider='gray')

if not session.is_logged_in():
    st.text('Login to get started.')
    session.login()

    if session.is_logged_in():
        st.switch_page(".\\pages\\chat.py")
else:
    st.markdown(f"Hello **{st.session_state.user['name']}**. To access **{st.session_state.bot_config['bot_name']}**,"
                f" please switch to the 'chat' tab from the sidebar.")




