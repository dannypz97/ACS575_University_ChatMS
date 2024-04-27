import streamlit as st

from chatbot import model

INTRO_MSG = """
Hi! I'm the University Virtual Assistant. I can help you find or connect to useful resources. How can I assist you?
"""

st.title("Chat")

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

    response = model.chat(prompt)
    # Display assistant response in chatbot message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chatbot history
    st.session_state.messages.append({"role": "assistant", "content": response})