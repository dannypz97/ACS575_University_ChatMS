import streamlit as st
import pymysql
from palm import test
import uuid

# Function to authenticate user login
def authenticate(username, password):
  # Perform user authentication here (e.g., query database)
  # For demonstration purposes, hardcoding username and password
  if username == "user" and password == "password":
    return True
  else:
    return False

# Function to generate a unique conversation ID
def generate_conversation_id():
  return str(uuid.uuid4())

# Function to log question and response into MySQL database
def log_to_database(conversation_id, question, response):
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
    st.error("Error connecting to database:", e)
    return

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

  # Login information stored in session state
  session_state = st.session_state
  session_state.username = session_state.get("username", "")
  session_state.password = session_state.get("password", "")
  session_state.logged_in = session_state.get("logged_in", False)
  session_state.conversation_id = session_state.get("conversation_id", "")

  # Login page
  session_state.username = st.text_input("Username", session_state.username)
  session_state.password = st.text_input("Password", type="password", value=session_state.password)
  if st.button("Login"):
    if authenticate(session_state.username, session_state.password):
      session_state.logged_in = True
      session_state.conversation_id = generate_conversation_id()
      st.success("Login successful!")

  # Logout Button
  if session_state.logged_in:
      logout = st.button("Logout")
      if logout:
          # Reset session state on logout
          session_state.username = ""
          session_state.password = ""
          session_state.logged_in = False
          session_state.conversation_id = ""
          st.success("Logged out successfully!")

  if session_state.logged_in:
    # Continue with chat interactions
    question = st.text_input("Question: ")
    if question:
      response = test(question)
      st.header("Answer")
      st.write(response)

      # Log question and response with stored conversation ID
      log_to_database(session_state.conversation_id, question, response)

if __name__ == "__main__":
  main()
