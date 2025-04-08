import streamlit as st
import hashlib

# Configurazione sessione multi-pagina
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Forza tema light e nascondi sidebar
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Nascondi sidebar via CSS
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION SYSTEM ---
def authenticate(username: str, password: str) -> bool:
    try:
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return (username == st.secrets["auth"]["username"] and 
                input_hash == st.secrets["auth"]["password_hash"])
    except:
        return False

def show_login_form():
    with st.form("Login"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        
        if st.form_submit_button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- MAIN APP ---
if not st.session_state.authenticated:
    show_login_form()
    st.stop()

# Contenuto principale (solo per utenti autenticati)
st.title("🛠️ PDM Utility Hub")
st.markdown("---")

# Pulsanti di navigazione
col1, col2 = st.columns(2)

with col1:
    if st.button("📦 Bundle & Set Images Creator", 
                use_container_width=True,
                key="bundle_btn"):
        st.switch_page("pages/Bundle_Set_Images_Creator.py")

with col2:
    if st.button("🖼️ Repository Image Download & Renaming", 
                use_container_width=True,
                key="repo_btn"):
        st.switch_page("pages/Repository_Image_Download_Renaming.py")

st.markdown("---")
st.caption("v1.0 | Secure Access System")
