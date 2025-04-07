# auth.py
import streamlit as st

# Only set the key if it does not exist already.
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def require_login():
    """Stops the app if the user is not authenticated."""
    if not st.session_state["authenticated"]:
        st.warning("Please log in first.")
        st.stop()
