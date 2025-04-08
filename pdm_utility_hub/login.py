# login.py
import streamlit as st

# Configurazione della pagina (deve essere la prima istruzione dopo gli import)
st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, simula il redirect impostando un parametro e ricaricando la pagina
if st.session_state.get("logged_in", False):
    st.query_params.page = "hub"
    st.rerun()

st.title("Login - PDM Utility Hub")
st.write("Clicca sul pulsante per effettuare il login (senza password).")

if st.button("Login"):
    st.session_state["logged_in"] = True
    # Imposta un parametro che indica la pagina di destinazione (qui 'hub')
    st.query_params.page = "hub"
    st.rerun()

# In alternativa, se il redirect non avviene automaticamente, fornisci un link manuale
st.markdown("[Se non vieni reindirizzato automaticamente, clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
