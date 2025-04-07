# pdm_hub.py
import streamlit as st
from passlib.hash import pbkdf2_sha256  # Importa per la verifica dell'hash

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# *Per forzare il login ad ogni caricamento, cancelliamo lo stato della sessione.*
# Attenzione: questa operazione è utile per il testing, ma in produzione
# potrebbe essere indesiderata perché impedisce la persistenza dello stato.
st.session_state.clear()

# --- Funzione di Verifica Login ---
def check_password(username, password):
    """Verifica username e password usando Streamlit Secrets e passlib."""
    try:
        correct_username = st.secrets["LOGIN_USERNAME"]
        hashed_password = st.secrets["LOGIN_HASHED_PASSWORD"]
        if username == correct_username and pbkdf2_sha256.verify(password, hashed_password):
            return True
        else:
            return False
    except KeyError as e:
        st.error(f"Errore di configurazione: il secret '{e}' non è stato trovato. "
                 "Vai nelle impostazioni dell'app su Streamlit Cloud e aggiungilo.")
        return False
    except Exception as e:
        st.error(f"Errore durante la verifica del login: {e}")
        return False

# --- Inizializza lo stato di autenticazione se non presente ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Blocco Login ---
if not st.session_state["authenticated"]:
    st.title("🔒 Login - PDM Utility Hub")
    st.markdown("Inserisci le credenziali per accedere.")
    
    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login", key="login_button"):
        if check_password(login_username, login_password):
            # Imposta lo stato di autenticazione a True
            st.session_state["authenticated"] = True
            # Non usiamo st.experimental_rerun(), così il passaggio alla pagina principale
            # avviene nello stesso run (tuttavia, se l'utente ricarica la pagina il form riapparirà)
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
