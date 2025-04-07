# login.py
import streamlit as st

st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, mostra un messaggio e il link per andare all'HUB
if st.session_state.get("password_correct", False):
    st.success("Sei già loggato!")
    st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
    st.stop()

st.title("Login senza Password")
st.write("Clicca il pulsante per effettuare il login (senza password).")

if st.button("Login"):
    st.session_state["password_correct"] = True
    st.success("Login effettuato con successo!")
    st.markdown("[Clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
