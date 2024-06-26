from pymysql import cursors

from db.conn import get_conn
from chatbot import palm

GET_BOT_ID_QUERY = "SELECT LAST_INSERT_ID()"

LOG_TRAIN_ATTEMPT_QUERY = """
    INSERT INTO chatbots (id, name, training_text) VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE training_text = VALUES(training_text), name = VALUES(name), is_trained = False
"""

MARK_TRAIN_ATTEMPT_QUERY = """
    UPDATE chatbots  SET is_trained = True WHERE id = (%s)
"""

UPDATE_NON_MODEL_DETAILS_QUERY = """
    UPDATE chatbots SET name = (%s) WHERE id = (%s)
"""

def train_attempt(training_text, *, bot_id, bot_name):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(LOG_TRAIN_ATTEMPT_QUERY, (bot_id, bot_name, training_text))
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

def update_non_model_details(name, *, bot_id):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(UPDATE_NON_MODEL_DETAILS_QUERY, (name, bot_id))
    conn.commit()
