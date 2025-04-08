# app.py
import streamlit as st
import hashlib

# Configurazione pagina
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered"
)

# --- SISTEMA DI AUTENTICAZIONE SEMPLIFICATO ---
def check_auth():
    """Verifica l'autenticazione"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_form()
        st.stop()

def show_login_form():
    """Mostra il form di login"""
    with st.form("Login"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        
        if st.form_submit_button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Credenziali non valide")

def authenticate(username: str, password: str) -> bool:
    """Verifica le credenziali usando solo hash SHA-256"""
    try:
        # Recupera le credenziali dai Secrets
        stored_username = st.secrets["auth"]["username"]
        stored_hash = st.secrets["auth"]["password_hash"]
        
        # Calcola l'hash della password inserita
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        
        return (username == stored_username and 
                input_hash == stored_hash)
    except:
        return False

# --- CONTENUTO PRINCIPALE (solo per utenti autenticati) ---
check_auth()

# Se arriviamo qui, l'utente è autenticato
st.title("🛠️ PDM Utility Hub")
st.write("Benvenuto nell'area riservata")
