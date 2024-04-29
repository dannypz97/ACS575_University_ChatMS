import bcrypt
from pymysql import cursors
import streamlit as st
import uuid
from chatbot import config

from db.conn import get_conn

def generate_session_id():
    return str(uuid.uuid4())

def is_logged_in():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    return st.session_state.is_logged_in

def login():
    email = st.text_input("Email", "", key="email")
    password = st.text_input("Password", "", type="password", key="password")

    if st.button("Login"):
        conn = get_conn()
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = (%s)", (email))
        user = cursor.fetchone()
        print("USER: ", user, "\n\n\n")
        if user:
            is_valid = bcrypt.checkpw(
                password=bytes(password, encoding='utf-8'),
                hashed_password=bytes(user['password'])
            )

            if is_valid:
                st.session_state.user = user
                st.session_state.is_logged_in = True

                bot_config = config.get_bot_config(user['university_id'])
                print(bot_config)

                if bot_config:
                    st.session_state.bot_config = bot_config
                return

        st.error('Invalid credentials!!', icon="🚨")

