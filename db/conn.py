import pymysql
import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

ctx = get_script_run_ctx()

def get_conn():
    creds_base = st.secrets.connections.mysql

    try:
        conn = pymysql.connect(
            host=creds_base.host,
            port=creds_base.port,
            user=creds_base.username,
            passwd=creds_base.password,
            db=creds_base.database
        )

        return conn
    except pymysql.Error as e:
        st.error(f"Error connecting to database:{e}")


def test_conn(conn=None):
    if not conn:
        conn = get_conn()

    cursor = conn.cursor()
    cursor.execute("SELECT 1;")


def get_st_conn():
    conn = st.connection('mysql', type='sql')
    return conn

def test_st_conn(conn=None):
    if not conn:
        conn = get_st_conn()

    conn.query('SELECT 1;')
