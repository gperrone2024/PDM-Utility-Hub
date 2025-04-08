import streamlit as st

# Configurazione pagina (DEVE essere la prima operazione)
st.set_page_config(
    page_title="Image Renamer",
    page_icon="🖼️",
    layout="centered"
)

# Verifica autenticazione
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("app.py")

# Contenuto della pagina
st.title("🖼️ Repository Image Download & Renaming")

if st.button("← Back to Hub", type="primary"):
    st.switch_page("app.py")

# Il resto del tuo codice...
