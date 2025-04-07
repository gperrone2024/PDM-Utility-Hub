import streamlit as st
from passlib.hash import pbkdf2_sha256

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Non usiamo st.session_state per memorizzare lo stato del login
# Questo fa sì che ad ogni refresh venga visualizzato il form di login

# --- Funzione di Verifica Login ---
def check_password(username, password):
    """Verifica username e password usando Streamlit Secrets e passlib."""
    try:
        correct_username = st.secrets["LOGIN_USERNAME"]
        hashed_password = st.secrets["LOGIN_HASHED_PASSWORD"]
        return username == correct_username and pbkdf2_sha256.verify(password, hashed_password)
    except KeyError as e:
        st.error(f"Errore di configurazione: il secret '{e}' non è stato trovato. "
                 "Vai nelle impostazioni dell'app su Streamlit Cloud e aggiungilo.")
        return False
    except Exception as e:
        st.error(f"Errore durante la verifica del login: {e}")
        return False

# --- Blocco Login ---
st.title("🔒 Login - PDM Utility Hub")
st.markdown("Inserisci le credenziali per accedere.")

login_username = st.text_input("Username")
login_password = st.text_input("Password", type="password")

if st.button("Login"):
    if check_password(login_username, login_password):
        st.success("Login effettuato correttamente!")
        st.markdown("---")
        # --- Contenuto Principale Hub ---
        st.title("🛠️ PDM Utility Hub")
        st.markdown("**Benvenuto nel Product Data Management Utility Hub.**")
        st.markdown("Seleziona un'applicazione per iniziare.")
        # Inserisci qui il contenuto dell'app principale...
    else:
        st.error("Username o Password errati.")

else:
    st.success("DEBUG: ESEGUITO BLOCCO APP PRINCIPALE")
    
    # --- Contenuto Principale Hub ---
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Benvenuto nel Product Data Management Utility Hub.**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Layout a 2 colonne per i bottoni principali (esempio)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Gestisce il download e l\'organizzazione automatica delle immagini per bundle e set di prodotti.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Scarica, ridimensiona e rinomina immagini da repository selezionate.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottone Logout nella sidebar
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("v.1.0")
