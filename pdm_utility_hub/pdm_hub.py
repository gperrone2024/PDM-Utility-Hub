# pdm_hub.py
import streamlit as st
from passlib.hash import pbkdf2_sha256 # Importa per la verifica dell'hash
import time # Necessario per st.rerun()

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Funzione di Verifica Login ---
def check_password(username, password):
    """Verifica username e password usando Streamlit Secrets e passlib."""
    try:
        # Legge i secrets direttamente dalla piattaforma Cloud (o da secrets.toml se esegui localmente)
        correct_username = st.secrets["LOGIN_USERNAME"]
        hashed_password = st.secrets["LOGIN_HASHED_PASSWORD"]

        if username == correct_username and pbkdf2_sha256.verify(password, hashed_password):
            return True
        else:
            return False
    except KeyError as e:
        # Questo errore appare se i secrets non sono definiti nella piattaforma Cloud
        st.error(f"Errore di configurazione: Secret '{e}' non trovato. Vai nelle impostazioni dell'app su Streamlit Cloud e aggiungilo.")
        return False
    except Exception as e:
        st.error(f"Errore durante la verifica del login: {e}")
        return False

# --- Logica di Autenticazione ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.warning("DEBUG: Stato 'authenticated' inizializzato a False.") # Debug 1
else:
    # Mostra lo stato esistente PRIMA del controllo if/else
    st.info(f"DEBUG: Stato 'authenticated' pre-controllo: {st.session_state['authenticated']}") # Debug 2

if not st.session_state["authenticated"]:
    # Questo blocco dovrebbe eseguire se authenticated è False
    st.error("DEBUG: ESEGUITO BLOCCO LOGIN FORM") # Debug 3
    # Mostra il form di login se non autenticato
    st.title("🔒 Login - PDM Utility Hub")
    st.markdown("Inserisci le credenziali per accedere.")

    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_button"):
        if check_password(login_username, login_password):
            st.session_state["authenticated"] = True
            st.session_state["login_user"] = "" # Pulisce i campi dopo il login
            st.session_state["login_pass"] = ""
            st.rerun() # Ricarica l'app per mostrare il contenuto protetto
        else:
            st.error("Username o Password errati.")
else:
    # Questo blocco dovrebbe eseguire se authenticated è True
    st.success("DEBUG: ESEGUITO BLOCCO APP PRINCIPALE") # Debug 4
    # --- L'utente è autenticato, mostra l'app principale ---

    # --- CSS Globale ---
    # CSS con adattamento tema e sidebar 540px
    st.markdown(
        """
        <style>
        /* Imposta larghezza sidebar e FORZA con !important */
        [data-testid="stSidebar"] > div:first-child {
            width: 540px !important;
            min-width: 540px !important;
            max-width: 540px !important;
        }
        /* Nasconde la navigazione automatica generata da Streamlit nella sidebar */
        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* Rimosso sfondo forzato per l'AREA PRINCIPALE - Lascia gestire al tema */
        /* section.main { */
            /* background-color: #d8dfe6 !important; /* RIMOSSO */
        /* } */

        /* Rendi trasparente il contenitore interno e mantieni il padding */
        /* Questo permette allo sfondo del tema di essere visibile */
        div[data-testid="stAppViewContainer"] > section > div.block-container {
             background-color: transparent !important;
             padding: 2rem 1rem 1rem 1rem !important; /* Padding per contenuto */
             border-radius: 0 !important; /* Nessun bordo arrotondato interno */
        }
        .main .block-container {
             background-color: transparent !important;
             padding: 2rem 1rem 1rem 1rem !important;
             border-radius: 0 !important;
        }


        /* Stile base per i bottoni/placeholder delle app */
        .app-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .app-button-link, .app-button-placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.2rem 1.5rem;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.05rem;
            width: 90%;
            min-height: 100px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04); /* Ombra leggera mantenuta */
            margin-bottom: 0.75rem;
            text-align: center;
            line-height: 1.4;
            transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            /* Rimossi color, background-color, border specifici per adattarsi al tema */
            /* color: #343a40; */ /* RIMOSSO */
            border: 1px solid var(--border-color, #cccccc); /* Usa variabile CSS se disponibile o fallback */
        }
         .app-button-link svg, .app-button-placeholder svg,
         .app-button-link .icon, .app-button-placeholder .icon {
             margin-right: 0.6rem;
             flex-shrink: 0;
         }
        .app-button-link > div[data-testid="stText"] > span:before {
            content: "" !important; margin-right: 0 !important;
        }

        /* Stile per bottoni cliccabili - Rimosso colore specifico */
        .app-button-link {
            /* background-color: #f5faff; */ /* RIMOSSO */
            /* border: 1px solid #c4daee; */ /* RIMOSSO - Usato fallback sopra */
            cursor: pointer; /* Mantenuto cursore */
        }
        .app-button-link:hover {
            /* background-color: #eaf2ff; */ /* RIMOSSO */
            /* border-color: #a9cce3; */ /* RIMOSSO */
            box-shadow: 0 2px 4px rgba(0,0,0,0.08); /* Effetto ombra su hover mantenuto */
            /* Streamlit gestirà il cambio colore di sfondo/bordo su hover in base al tema */
        }

        /* Stile Placeholder Coming Soon (non cliccabile) */
        .app-button-placeholder {
            /* background-color: #f1f3f5; */ /* RIMOSSO */
            opacity: 0.7; /* Opacità mantenuta per distinguerlo */
            cursor: default;
            box-shadow: none;
            /* color: #868e96; */ /* RIMOSSO - Lascia gestire al tema il colore testo "disabilitato" */
            border-style: dashed; /* Mantenuto stile tratteggiato per distinguerlo */
            /* border: 1px dashed #cccccc; */ /* RIMOSSO - Usato fallback sopra con stile dashed */
        }
         .app-button-placeholder .icon {
             font-size: 1.5em;
         }


        /* Stile per descrizione sotto i bottoni */
         .app-description {
            font-size: 0.9em;
            /* color: #343a40; */ /* RIMOSSO - Lascia gestire al tema */
            padding: 0 15px;
            text-align: justify;
            width: 90%;
            margin: 0 auto;
         }

        /* Aggiusta colore link nella sidebar per coerenza tema (opzionale ma consigliato) */
        [data-testid="stSidebar"] a:link, [data-testid="stSidebar"] a:visited {
            /* color: inherit; /* Eredita colore dal tema */
            text-decoration: none;
        }
        [data-testid="stSidebar"] a:hover {
            text-decoration: underline; /* O altro effetto hover desiderato */
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Bottone per tornare all'Hub nella Sidebar ---
    st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")

    # --- Bottone Logout ---
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        # Pulisce anche i campi input del login se presenti nello stato
        if "login_user" in st.session_state: del st.session_state["login_user"]
        if "login_pass" in st.session_state: del st.session_state["login_pass"]
        st.rerun()

    st.sidebar.markdown("---") # Separatore opzionale

    # --- Contenuto Principale Hub ---
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
    st.markdown("<br>", unsafe_allow_html=True) # Spazio

    # Layout a 2 colonne per i bottoni principali
    col1, col2 = st.columns(2)

    # --- Colonna 1: App Bundle + Coming Soon ---
    with col1:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Colonna 2: App Renaming ---
    with col2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Footer Modificato ---
    st.markdown("---")
    st.caption("v.1.0")

# --- Fine Blocco Autenticato ---
