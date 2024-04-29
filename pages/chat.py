import streamlit as st

from user import session
from chatbot import admin, chat, config, palm

INTRO_MSG = """
Hi! I'm the University Virtual Assistant. I can help you find or connect to useful resources. How can I assist you?
"""

INTRO_AGAIN_MSG = """
Hello again! I'm the University Virtual Assistant. I can help you find or connect to useful resources. How can I assist you?
"""

if not session.is_logged_in():
    st.switch_page('.\\home.py')

st.session_state.chat = False

if st.session_state.user['is_admin']:
    st.title('Chatbot Configuration')
    bot_name = st.text_area('Chatbot Name', value='University Chatbot')
    training_text = st.text_area("Upload Training Text", height=200)

    if st.button("Train Chatbot"):
        if training_text:
            admin.train_attempt(training_text, bot_id=st.session_state.user['university_id'], bot_name=bot_name)
            st.success("Chatbot training successful!!")
            admin.mark_train_attempt_completed(st.session_state.user['university_id'])

            st.session_state.bot_config = config.get_bot_config(st.session_state.user['university_id'])

if 'bot_config' in st.session_state and st.session_state.bot_config['is_trained']:
    st.title(st.session_state.bot_config['bot_name'])

    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = []
        intro = INTRO_MSG

        chat_logs = chat.get_chats(st.session_state.user)

        if chat_logs and len(chat_logs) > 0:
            intro = INTRO_AGAIN_MSG
            st.session_state.messages = chat_logs

        st.session_state.messages.append({"role": chat.ASSISTANT_ROLE, "content": intro})
        chat.log_chat(intro, user=st.session_state.user, source=chat.ASSISTANT_ROLE, commit=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        # Display user message in chatbot message container
        with st.chat_message(chat.USER_ROLE):
            st.markdown(prompt)
        # Add user message to chatbot history
        st.session_state.messages.append({"role": chat.USER_ROLE, "content": prompt})

        response = chat.chat(prompt, user=st.session_state.user)
        # Display assistant response in chatbot message container
        with st.chat_message(chat.ASSISTANT_ROLE):
            st.markdown(response)
        # Add assistant response to chatbot history
        st.session_state.messages.append({"role": chat.ASSISTANT_ROLE, "content": response})