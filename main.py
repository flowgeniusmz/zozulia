import streamlit as st
from classes import sessionstate as ss

st.set_page_config(page_title="Zozulia Finances", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")

ss.SessionState.get()

st.switch_page(page="pages/1_Assistant.py")