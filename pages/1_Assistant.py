import streamlit as st
from openai import OpenAI
import pandas as pd
from classes import sessionstate as ss
import time

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Im your personal finance assistant - do you understand? Does that make sense?"}]
client = OpenAI(api_key=st.secrets.openai.apikey)
assistantid = st.secrets.openai.assistantid
threadid = st.secrets.openai.threadid


# Initial Display
chatcontainer = st.container()
with chatcontainer:
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# Chat input
if prompt := st.chat_input(placeholder="Enter your question or request here..."):
    st.session_state.prompt = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chatcontainer:
        with st.chat_message("user"):
            st.markdown(prompt)
    promptmessage = client.beta.threads.messages.create(thread_id=threadid, content=prompt, role='user')
    promptmessageid = promptmessage.id
    run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
    while run.status == "in_progress" or run.status == "queued":
        st.toast("Running please wait...")
        with chatcontainer:
            status = st.status(label="Running please wait...", expanded=False, state="running")
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
        if run.status == "completed":
            st.toast("Completed!")
            with chatcontainer:
                status.update(label="Completed!", expanded=False, state="complete")
            threadmessages = client.beta.threads.messages.list(thread_id=threadid)
            for tm in threadmessages:
                if tm.role == "assistant" and tm.run_id == run.id:
                    response = tm.content[0].text.value
                    st.session_state.response = response
                    with chatcontainer:
                        with st.chat_message("assistant"):
                            st.markdown(response)

    