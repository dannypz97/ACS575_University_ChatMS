import streamlit as st

from user import session
from chatbot import admin, chat, config, palm

INTRO_MSG = """
Hi! I'm the University Virtual Assistant. I can help you find or connect to useful resources. How can I assist you?
"""

DEFAULT_BOT_NAME = 'University Chatbot'

if not session.is_logged_in():
    st.switch_page('.\\home.py')

st.session_state.chat = False

if st.session_state.user['is_admin']:
    bot_config = config.get_bot_config(st.session_state.user['university_id'])
    if bot_config:
        fetched_bot_name = bot_config['bot_name']
        fetched_training_text = bot_config['training_text']
    else:
        fetched_bot_name = DEFAULT_BOT_NAME
        fetched_training_text = ''

    st.title('Chatbot Configuration')
    bot_name = st.text_area('Chatbot Name', value=fetched_bot_name)
    training_text = st.text_area("Training Text", value=fetched_training_text, height=200)

    if st.button("Save Configuration"):
        if bot_name:
            bot_name = bot_name.strip()
        if training_text:
            training_text = training_text.strip()

        if not bot_name or not training_text:
            if not bot_name:
                st.error("Missing field 'Chatbot Name'", icon="🚨")
            if not training_text:
                st.error("Missing field 'Training Text'", icon="🚨")
        else:
            if training_text != fetched_training_text:
                st.success("Configuration saved. Chatbot training in progress...")
                admin.train_attempt(training_text, bot_id=st.session_state.user['university_id'], bot_name=bot_name)
                admin.mark_train_attempt_completed(st.session_state.user['university_id'])
                st.success("Chatbot training complete!!.")
            else:
                admin.update_non_model_details(bot_name, bot_id=st.session_state.user['university_id'])
                st.success("Configuration saved.")

            st.session_state.bot_config = config.get_bot_config(st.session_state.user['university_id'])

if 'bot_config' in st.session_state and st.session_state.bot_config['is_trained']:
    st.title(st.session_state.bot_config['bot_name'])

    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = []

        chat_logs = chat.get_chats(st.session_state.user)

        if chat_logs and len(chat_logs) > 0:
            st.session_state.messages = chat_logs
        else:
            st.session_state.messages.append({"role": chat.ASSISTANT_ROLE, "content": INTRO_MSG})

        # chat.log_chat(INTRO_MSG, user=st.session_state.user, source=chat.ASSISTANT_ROLE, commit=True)

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