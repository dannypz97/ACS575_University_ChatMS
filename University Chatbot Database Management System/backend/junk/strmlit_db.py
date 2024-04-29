import streamlit as st
import pymysql
from palm import test
import uuid

# Generate a unique conversation ID
conversation_id = str(uuid.uuid4())
# Function to log question and response into MySQL database
def log_to_database(question, response):
    # Database credentials
    db_user = "root"
    db_password = "rootroot@123"
    db_host = "127.0.0.1"
    db_name = "bank"

    # Establish connection to the database
    conn = pymysql.connect(
        host=db_host,
        port=3306,
        user=db_user,
        passwd=db_password,
        db=db_name
    )

    # Create a cursor object
    cursor = conn.cursor()

    # SQL query to insert data into the database
    sql_query = "INSERT INTO question_response (conversation_id, question, response) VALUES (%s, %s, %s)"
    data = (conversation_id, question, response)

    try:
        # Execute the SQL query
        cursor.execute(sql_query, data)
        # Commit the transaction
        conn.commit()
        st.success("Question and response logged successfully!")
    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        st.error("Error occurred while logging question and response:", e)
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

def main():
    st.title("Bank query")
    question = st.text_input("Question: ")

    if question:
        response = test(question)
        st.header("Answer")
        st.write(response)

        # Log question and response to the database
        log_to_database(question, response)

if __name__ == "__main__":
    main()
