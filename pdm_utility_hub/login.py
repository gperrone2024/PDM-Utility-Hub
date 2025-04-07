# login_test.py
import streamlit as st

st.set_page_config(page_title="Login Test", page_icon="🔑")
st.title("Login senza Password - Test")

if st.button("Login"):
    st.session_state["password_correct"] = True
    st.write("Login effettuato!")
    st.write("[Vai all'HUB](/pdm_hub.py)")
