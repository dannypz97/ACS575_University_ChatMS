from pymysql import cursors

from db.conn import get_conn
from chatbot import palm

LOG_CHAT_QUERY = """
    INSERT INTO user_chats (user_id, message, source) VALUES (%s, %s, %s)
"""
FETCH_CHATS_QUERY = """
    SELECT message AS content, source AS role from user_chats
    WHERE user_id = (%s)
    ORDER BY ID ASC;
"""

DEFAULT_RESPONSE = "I'm sorry but I can't assist you with that right now."

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"

def log_chat(msg, *, user, source, conn=None, commit=False):
    if not conn:
        conn = get_conn()

    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(LOG_CHAT_QUERY, (user['id'], msg, source))

    if commit:
        conn.commit()

def chat(query, *, user):
    conn = get_conn()
    log_chat(query, user=user, source=USER_ROLE, conn=conn, commit=True)

    response = palm.test(query, user['university_id'])

    if not response:
        response = DEFAULT_RESPONSE

    log_chat(response, user=user, source=ASSISTANT_ROLE, conn=conn, commit=True)

    return response

def get_chats(user):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)

    cursor.execute(FETCH_CHATS_QUERY, (user['id']))
    result = cursor.fetchall()

    return result
