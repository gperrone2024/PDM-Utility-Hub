# login.py
import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, reindirizza
if st.session_state.get("logged_in", False):
    st.switch_page("pages/pdm_hub.py")  # Assicurati che il percorso sia corretto

st.title("Login - PDM Utility Hub")
st.write("Clicca sul pulsante per effettuare il login (senza password).")

if st.button("Login"):
    st.session_state["logged_in"] = True
    st.switch_page("pages/pdm_hub.py")  # Reindirizza alla pagina principale

# Link manuale se il reindirizzamento non funziona
st.markdown("[Se non vieni reindirizzato automaticamente, clicca qui per andare all'HUB Principale](pages/pdm_hub.py)")
