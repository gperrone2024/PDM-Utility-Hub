# login.py
import streamlit as st

# Deve essere la prima istruzione dopo gli import!
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Rimuoviamo temporaneamente st.stop() per debug
if st.session_state.get("password_correct", False):
    st.success("Sei già loggato!")
    st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
else:
    st.title("Login senza Password")
    st.write("Clicca il pulsante per effettuare il login (senza password).")
    if st.button("Login"):
        st.session_state["password_correct"] = True
        st.success("Login effettuato con successo!")
        st.markdown("[Clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
st.markdown('<a href="/pdm_utility_hub/pages/pdm_hub" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
