# login_and_hub.py
import streamlit as st

st.set_page_config("PDM Utility Hub", "🔑")

# Gestione login/logout
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Pagina di Login
if not st.session_state.logged_in:
    st.title("🔑 Login")
    if st.button("Accedi"):
        st.session_state.logged_in = True
        st.rerun()  # Ricarica la pagina

# Pagina Principale (dopo login)
else:
    st.title("🏠 PDM Utility Hub")
    st.write("Benvenuto!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
