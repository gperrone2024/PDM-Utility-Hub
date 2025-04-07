# access_page.py
import streamlit as st

# Configura la pagina
st.set_page_config(page_title="Accesso HUB", page_icon="🔀")

st.title("Accedi a PDM Utility Hub")
st.write("Premi il pulsante per accedere all'HUB principale.")

# Prova a usare il redirect automatico se disponibile
try:
    from streamlit_extras.switch_page_button import switch_page
    if st.button("Vai all'HUB"):
        switch_page("PDM Utility Hub")
except ImportError:
    # Fallback: mostra un link di navigazione
    if st.button("Vai all'HUB"):
        st.markdown("[Clicca qui per accedere all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
