import streamlit as st
from passlib.hash import pbkdf2_sha256

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Per forzare il login ad ogni caricamento (solo per test), cancelliamo lo stato.
# In produzione rimuovi questa istruzione per mantenere la sessione autenticata.
st.session_state.clear()

# --- Funzione di Verifica Login ---
def check_password(username, password):
    """Verifica username e password usando Streamlit Secrets e passlib."""
    try:
        correct_username = st.secrets["LOGIN_USERNAME"]
        hashed_password = st.secrets["LOGIN_HASHED_PASSWORD"]
        return username == correct_username and pbkdf2_sha256.verify(password, hashed_password)
    except KeyError as e:
        st.error(
            f"Errore di configurazione: il secret '{e}' non è stato trovato. "
            "Vai nelle impostazioni dell'app su Streamlit Cloud e aggiungilo."
        )
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
    
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_password(login_username, login_password):
            st.session_state["authenticated"] = True
            st.experimental_rerun()  # Ricarica l'app per mostrare il contenuto protetto
        else:
            st.error("Username o Password errati.")
else:
    # --- Contenuto Principale Hub ---
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Benvenuto nel Product Data Management Utility Hub.**")
    st.markdown("Seleziona un'applicazione per iniziare.")
    
    
    # Bottone Logout nella sidebar
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("v.1.0")
