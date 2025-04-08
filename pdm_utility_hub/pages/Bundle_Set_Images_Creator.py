#Bundle_Set_Images_Creator.py
import streamlit as st
from app import get_auth_state, set_auth_state, check_auth

# Esegui il check dell'autenticazione
if not get_auth_state():
    check_auth()

# Il resto del tuo codice...

# Configurazione pagina
st.set_page_config(
    page_title="Bundle Images Creator",
    page_icon="📦",
    layout="centered"
)

# --- CONTENUTO PRINCIPALE ---
st.title("📦 Bundle & Set Images Creator")
st.markdown("---")

# Pulsante per tornare all'Hub
st.markdown("""
<a href="/" class="app-button-link" style="text-decoration: none; margin-bottom: 2rem;">
    ← Back to PDM Hub
</a>
""", unsafe_allow_html=True)

# Il tuo contenuto qui...
st.write("Welcome to the Bundle Image Creator Tool")

# Stile coerente con l'app principale
st.markdown("""
<style>
.app-button-link {
    background-color: #e0f2fe !important;
    color: #0369a1 !important;
    border: 1px solid #bae6fd !important;
    padding: 0.5rem 1rem !important;
    border-radius: 0.5rem !important;
    display: inline-block !important;
    text-align: center !important;
    margin: 0.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)
