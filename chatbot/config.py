from pymysql import cursors

from db.conn import get_conn
def get_bot_config(id):
    conn = get_conn()
    cursor = conn.cursor(cursors.DictCursor)

    cursor.execute(
        "SELECT university_id AS bot_id, name as bot_name, is_trained FROM chatbots WHERE university_id = (%s)",
        (id)
    )

    bot_config = cursor.fetchone()

    return bot_config