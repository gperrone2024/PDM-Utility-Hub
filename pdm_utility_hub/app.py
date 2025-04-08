import streamlit as st
import hashlib

# Inizializzazione sessione
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Configurazione pagina (DEVE essere la prima operazione)
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Nascondi sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Sistema di autenticazione
def authenticate(username: str, password: str) -> bool:
    try:
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return (username == st.secrets["auth"]["username"] and 
                input_hash == st.secrets["auth"]["password_hash"])
    except:
        return False

# Mostra form di login se non autenticato
if not st.session_state.authenticated:
    with st.form("Login"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        
        if st.form_submit_button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Credenziali non valide")
    st.stop()

# Contenuto principale
st.title("🛠️ PDM Utility Hub")
st.markdown("---")

# Pulsanti di navigazione
if st.button("📦 Bundle & Set Images Creator", use_container_width=True):
    st.switch_page("pages/Bundle_Set_Images_Creator.py")

if st.button("🖼️ Repository Image Download & Renaming", use_container_width=True):
    st.switch_page("pages/Repository_Image_Download_Renaming.py")

st.markdown("---")
st.caption("v1.0 | Secure Access System")
