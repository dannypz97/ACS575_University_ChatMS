import streamlit as st
from palm import test, train
from function_handler import *


def main():
  st.title("Welcome to the University Database Management System!")

  # Login information stored in session state
  session_state = st.session_state
  session_state.username = session_state.get("username", "")
  # Use secure hashing for password storage (placeholder)
  session_state.password = session_state.get("password", "")
  session_state.logged_in = session_state.get("logged_in", False)
  session_state.conversation_id = session_state.get("conversation_id", "")
  session_state.user_type = session_state.get("user_type", "")

  # Login page
  session_state.username = st.text_input("Username", session_state.username)
  session_state.password = st.text_input("Password", type="password", value="")  # Don't pre-fill password
  user_type_selection = st.selectbox("User Type", ["admin", "student"])
  if st.button("Login"):
    if authenticate(session_state.username, session_state.password, user_type_selection):
      session_state.logged_in = True
      session_state.conversation_id = generate_conversation_id()
      session_state.user_type = user_type_selection
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

  # Continue with chat interactions (if logged in)
  if session_state.logged_in:
    university = st.text_input("University", value="")
    if session_state.user_type == "student":
      # Student conversation
      question = st.text_input("Question: ")
      if question:
        response = test(question,university)
        st.header("Answer")
        st.write(response)

        # Log question and response
        log_to_database(session_state.conversation_id, question=question, response=response, training_text=None,university=university,user_type=session_state.user_type)
        get_and_export_conversation_logs()
    else:  # Admin
      # Admin training section
      training_text = st.text_area("Upload Training Text", height=200)
    #   university = st.text_input("University (Optional)", value="")
      if st.button("Train Chatbot"):
        if training_text:
          train(training_text, university)
          st.success("Chatbot training successful!")
          log_to_database(session_state.conversation_id, question=None, response=None, training_text=training_text, university=university, user_type=session_state.user_type)
          get_and_export_conversation_logs()
      else:
        st.success("Provide the training data and hit the Train button to train your custom model!")

      question = st.text_input("Question: ")
      if question:
        response = test(question,university)
        st.header("Answer")
        st.write(response)
        # Log student question and response
        log_to_database(session_state.conversation_id, question=question, response=response, user_type=session_state.user_type)
        get_and_export_conversation_logs()
if __name__ == "__main__":
  main()

