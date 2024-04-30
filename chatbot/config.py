from pymysql import cursors

from db.conn import get_conn
def get_bot_config(id):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)

    cursor.execute(
        "SELECT id AS bot_id, name as bot_name, training_text, is_trained FROM chatbots WHERE id = (%s)",
        (id)
    )

    bot_config = cursor.fetchone()

    return bot_config