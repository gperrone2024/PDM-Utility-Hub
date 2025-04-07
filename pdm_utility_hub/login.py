# login.py
import streamlit as st

# Configura la pagina (deve essere la prima istruzione dopo gli import)
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, mostra il link all'HUB
if st.session_state.get("logged_in", False):
    st.success("Sei già loggato!")
    st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
    st.stop()

# Mostra il form di "login" senza password
st.title("Login (senza password)")
st.write("Clicca sul pulsante per effettuare il login.")

if st.button("Login"):
    st.session_state["logged_in"] = True
    st.success("Login effettuato!")
    st.markdown("[Clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
