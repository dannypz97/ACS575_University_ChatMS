from pymysql import cursors

from db.conn import get_conn
from chatbot import palm

GET_BOT_ID_QUERY = "SELECT LAST_INSERT_ID()"

LOG_TRAIN_ATTEMPT_QUERY = """
    INSERT INTO chatbots (university_id, name, training_text) VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE training_text = VALUES(training_text), name = VALUES(name), is_trained = False
"""

MARK_TRAIN_ATTEMPT_QUERY = """
    UPDATE chatbots  SET is_trained = True WHERE university_id = (%s)
"""
def train_attempt(training_text, *, university_id, bot_name):
    # Using university_id as the bot_id/model_id.
    bot_id = university_id

    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(LOG_TRAIN_ATTEMPT_QUERY, (university_id, bot_name, training_text))
    # cursor.execute(GET_BOT_ID_QUERY)
    # bot_id = cursor.fetchone()[0]
    conn.commit()

    # Could be asynchronous?
    palm.train(training_text, model_id=bot_id)

def mark_train_attempt_completed(bot_id):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(MARK_TRAIN_ATTEMPT_QUERY, (bot_id))
    conn.commit()