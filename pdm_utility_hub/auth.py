# auth.py
import streamlit as st
def require_login():
    if not st.session_state.get("authenticated", False):
        st.warning("Please login first.")
        st.stop()
