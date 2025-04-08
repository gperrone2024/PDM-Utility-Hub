import streamlit as st

# Configurazione pagina (DEVE essere la prima operazione)
st.set_page_config(
    page_title="Bundle Creator",
    page_icon="📦",
    layout="centered"
)

# Verifica autenticazione
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("app.py")

# Contenuto della pagina
st.title("📦 Bundle & Set Images Creator")

if st.button("← Back to Hub", type="primary"):
    st.switch_page("app.py")

# Il resto del tuo codice...
