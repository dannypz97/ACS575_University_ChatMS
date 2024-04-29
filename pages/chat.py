import streamlit as st

from user import login
from chatbot import admin, config, palm

INTRO_MSG = """
Hi! I'm the University Virtual Assistant. I can help you find or connect to useful resources. How can I assist you?
"""

if not login.is_logged_in():
    st.switch_page('.\\home.py')

st.session_state.chat = False

if st.session_state.user['is_admin']:
    st.title('Chatbot Configuration')
    bot_name = st.text_area('Chatbot Name', value='University Chatbot')
    training_text = st.text_area("Upload Training Text", height=200)

    if st.button("Train Chatbot"):
        if training_text:
            admin.train_attempt(training_text, university_id=st.session_state.user['university_id'], bot_name=bot_name)
            st.success("Chatbot training successful!!")
            admin.mark_train_attempt_completed(st.session_state.user['university_id'])

            st.session_state.bot_config = config.get_bot_config(st.session_state.user['university_id'])

if 'bot_config' in st.session_state and st.session_state.bot_config['is_trained']:
    st.title(st.session_state.bot_config['bot_name'])

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": INTRO_MSG})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        # Display user message in chatbot message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chatbot history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = palm.test(prompt, model_id=st.session_state.bot_config['bot_id'])
        # Display assistant response in chatbot message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chatbot history
        st.session_state.messages.append({"role": "assistant", "content": response})