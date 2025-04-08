# pages/pdm_hub.py
import streamlit as st

# Verifica se l'utente è loggato, altrimenti reindirizza
if not st.session_state.get("logged_in", False):
    st.switch_page("login.py")  # Torna al login se non autenticato

# Pagina principale
st.set_page_config(page_title="PDM Utility Hub", page_icon="🏠")
st.title("Benvenuto nel PDM Utility Hub! 🎉")
st.write("Sei correttamente loggato.")

if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.switch_page("login.py")  # Torna al login
