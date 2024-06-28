import streamlit as st


class SessionState:
    def __init__(self):
        self.initial_state = dict(st.secrets.sessionstate)
        self.initial_state['messages']=[{"role": "assistant", "content": "Im your personal finance assistant - do you understand? Does that make sense?"}]

    def initialize(self):
        # Once initial state is set - this initializes each key/value pair to the session state
        for key, value in self.initial_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @classmethod
    def get(cls):
        # Class method applies to the class as a whole every time it is called. It prevents a new instance of the class being created each time and instead returns the existing
        if 'session_state_instance' not in st.session_state:
            st.session_state.session_state_instance = cls()
        return st.session_state.session_state_instance
    
    def update(self, **kwargs):
        # Allows to update session state values using keyword arguemnts or KWARGS. Dynamic so that you can literally say update(username= value, ...)
        for key, value in kwargs.items():
            st.session_state[key] = value
    
    def get_value(self, key):
        # Retuns a single key value
        return st.session_state.get(key, None)

    def set_file_content(self, key, filepath):
        # Method that lets a file content be set to a variable
        try:
            with open(file=filepath, mode="r") as file:
                content = file.read()
            st.session_state[key] = content
        except FileNotFoundError:
            st.session_state[key] = "File Not Found"

    def _set_messages(self):
        self.initial_state['messages'] = [{"role": "assistant", "content": "Welcome to SpartakusAI - Are you here to buy insurance?"}]




### EXAMPLE USAGE
# import streamlit as st
# from classes.class0_pagesetup import PageSetup
# from classes.class1_payment import Payment
# from session_state import SessionState  # Adjust the import path as needed

# 1. Set ST PAGE CONFIG
# st.set_page_config(
#     page_icon=st.secrets.app.icon,
#     page_title=st.secrets.app.title,
#     layout=st.secrets.app.layout,
#     initial_sidebar_state=st.secrets.app.sidebar
# )

# # 2. Initialize Session State with values from st.secrets.sessionstate
# initial_state = dict(st.secrets.sessionstate)
# query_params = st.experimental_get_query_params()
# initial_state['userstate'] = 0 if not query_params else 4

# session_state = SessionState.get(**initial_state)

# # 3. Set Page Setup
# PageSetup(pagenumber=session_state.get_value('userstate')).display_manual()

# c = st.checkbox("proceed")
# if c:
#     Payment().display_payment()
#     # Update session state if needed
#     session_state.update(userstate=1)  # Example update

    