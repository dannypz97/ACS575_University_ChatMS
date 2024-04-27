import streamlit as st


def get_conn():
    conn = st.connection('mysql', type='sql')
    return conn

def test_conn(conn=None):
    if not conn:
        conn = get_conn()

    conn.query('SELECT 1;')
