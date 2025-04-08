import streamlit as st
from app import st.session_state

# Verifica autenticazione
if not st.session_state.get('authenticated', False):
    st.switch_page("app.py")

# Configurazione pagina
st.set_page_config(
    page_title="Bundle Creator",
    page_icon="📦",
    layout="centered"
)

# Pulsante ritorno
if st.button("← Back to Hub", type="primary"):
    st.switch_page("app.py")

# Contenuto della pagina
st.title("📦 Bundle & Set Images Creator")
st.write("Your content here...")
