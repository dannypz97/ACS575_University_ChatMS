import streamlit as st
import pymysql
import uuid
import pandas as pd
# Function to authenticate user login
def authenticate(username, password, user_type):
  # Perform user authentication here (e.g., query database)
  # For demonstration purposes, hardcoding username and password
  if user_type == "admin" and username == "admin" and password == "adminpassword":
    return True
  elif user_type == "student" and username == "student" and password == "studentpassword":
    return True
  else:
    return False

# Function to generate a unique conversation ID
def generate_conversation_id():
  return str(uuid.uuid4())

# Function to log conversation/training data into MySQL database
def log_to_database(conversation_id, question, response, user_type, training_text="", university=""):
  # Database credentials (replace with yours if different)
  db_user = "root"
  db_password = "rootroot@123"
  db_host = "127.0.0.1"
  db_name = "bank"

  # Establish connection to the database
  try:
    conn = pymysql.connect(
        host=db_host,
        port=3306,
        user=db_user,
        passwd=db_password,
        db=db_name
    )
  except pymysql.Error as e:
    st.error(f"Error connecting to database:{e}")
    return

  # Create a cursor object
  cursor = conn.cursor()

  # SQL query to insert data
  sql_query = "INSERT INTO question_response (conversation_id, question, response,training_text, university) VALUES (%s, %s, %s,%s, %s)"
  data = (conversation_id, question, response,training_text, university)

  try:
    # Execute the SQL query
    cursor.execute(sql_query, data)
    # Commit the transaction
    conn.commit()
    if user_type == "student":
      st.success("Question and response logged successfully!")
    else:
      st.success("Training data logged successfully!")
  except Exception as e:
    # Rollback the transaction in case of error
    conn.rollback()
    st.error(f"Error occurred while logging data:{e}")
  finally:
    # Close cursor and connection
    cursor.close()
    conn.close()
    
def get_and_export_conversation_logs():
  """
  Connects to the database, retrieves the last 5 conversation logs,
  stores them in a Pandas DataFrame, and exports the DataFrame to an Excel file.

  Returns:
      None
  """

  # Database connection details (replace with yours)
  db_user = "root"
  db_password = "rootroot@123"
  db_host = "127.0.0.1"
  db_name = "bank"

  try:
    # Connect to the database
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # SQL query to retrieve conversation logs
    sql_query = """SELECT * FROM question_response
                    ORDER BY id DESC
                    LIMIT 5;"""

    # Execute the query and store results in a DataFrame
    df = pd.read_sql(sql_query, conn)

  except pymysql.Error as e:
    print(f"Error connecting to database:{e}")
    return

  finally:
    # Close the connection (always execute, even in case of errors)
    conn.close()

  # Export DataFrame to Excel (assuming successful database connection)
  df.to_excel("backend/database_logs/conversation_logs.xlsx", index=False)