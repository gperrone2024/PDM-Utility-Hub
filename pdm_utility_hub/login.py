# login.py
import streamlit as st

# Configurazione della pagina: deve essere la prima istruzione
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, mostra il link all'HUB principale
if st.session_state.get("logged_in", False):
    st.success("Sei già loggato!")
    st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
    st.stop()

st.title("Login - PDM Utility Hub")
st.write("Clicca sul pulsante per effettuare il login (senza password).")

if st.button("Login"):
    st.session_state["logged_in"] = True
    st.success("Login effettuato!")
    st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
