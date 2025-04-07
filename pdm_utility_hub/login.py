# login.py
import streamlit as st

# Imposta la configurazione della pagina (deve essere la prima istruzione dopo gli import)
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Prova a importare il componente per il cambio pagina
try:
    from streamlit_extras.switch_page_button import switch_page
except ImportError:
    switch_page = None

# Se l'utente è già loggato, reindirizza o mostra il link all'HUB
if st.session_state.get("logged_in", False):
    st.success("Sei già loggato!")
    if switch_page:
        switch_page("PDM Utility Hub")  # Assicurati che il nome corrisponda a quello definito nella pagina HUB
    else:
        st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
    st.stop()

st.title("Login - PDM Utility Hub")
st.write("Clicca sul pulsante per effettuare il login (senza password).")

if st.button("Login"):
    st.session_state["logged_in"] = True
    st.success("Login effettuato con successo!")
    if switch_page:
        switch_page("PDM Utility Hub")
    else:
        st.markdown("[Clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
