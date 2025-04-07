import streamlit as st

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Funzione di Controllo Password (dal primo script) ---
def check_password():
    """Restituisce True se username e password sono corretti."""
    correct_username = "PDM-Team"
    correct_password = "prova1234"

    if (
        st.session_state.get("username") == correct_username and
        st.session_state.get("password") == correct_password
    ):
        st.session_state["password_correct"] = False
    else:
        st.session_state["password_correct"] = False

# --- Inizializzazione dello stato di Login ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

# --- Blocco di Login: Visualizzato solo se NON loggato ---
if not st.session_state["password_correct"]:
    st.title("PDM Utility Hub")
    st.markdown("---")
    with st.form("login_form"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            check_password()
            if not st.session_state["password_correct"]:
                st.error("😕 Username o password errati.")
            else:
                st.rerun()
    st.stop()

# --- Sidebar: Messaggio di login e Logout ---
st.sidebar.success("Login effettuato con successo!")
if st.sidebar.button("Logout"):
    st.session_state["password_correct"] = False
    st.session_state.pop("username", None)
    st.session_state.pop("password", None)
    st.rerun()

st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
st.sidebar.markdown("---")

# --- CSS Globale (dal secondo script) ---
st.markdown(
    """
    <style>
    /* Imposta larghezza sidebar a 540px e FORZA con !important */
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
    }
    /* Nasconde la navigazione automatica generata da Streamlit nella sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    /* Rendi trasparente il contenitore interno e mantieni il padding */
    div[data-testid="stAppViewContainer"] > section > div.block-container {
         background-color: transparent !important;
         padding: 2rem 1rem 1rem 1rem !important;
         border-radius: 0 !important;
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
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        margin-bottom: 0.75rem;
        text-align: center;
        line-height: 1.4;
        transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        border: 1px solid var(--border-color, #cccccc);
    }
    .app-button-link svg, .app-button-placeholder svg,
     .app-button-link .icon, .app-button-placeholder .icon {
         margin-right: 0.6rem;
         flex-shrink: 0;
     }
    .app-button-link > div[data-testid="stText"] > span:before {
        content: "" !important; margin-right: 0 !important;
    }
    .app-button-link {
        cursor: pointer;
    }
    .app-button-link:hover {
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .app-button-placeholder {
        opacity: 0.7;
        cursor: default;
        box-shadow: none;
        border-style: dashed;
    }
     .app-button-placeholder .icon {
         font-size: 1.5em;
     }
    .app-description {
        font-size: 0.9em;
        padding: 0 15px;
        text-align: justify;
        width: 90%;
        margin: 0 auto;
     }
    [data-testid="stSidebar"] a:link, [data-testid="stSidebar"] a:visited {
        text-decoration: none;
    }
    [data-testid="stSidebar"] a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Contenuto Principale (dal secondo script) ---
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
st.markdown("<br>", unsafe_allow_html=True)

# Layout a 2 colonne per i bottoni principali
col1, col2 = st.columns(2)

# Colonna 1: App Bundle e Coming Soon
with col1:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown(
        '<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">'
        '📦 Bundle & Set Images Creator'
        '</a>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Colonna 2: App Renaming
with col2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown(
        '<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">'
        '🖼️ Repository Image Download & Renaming'
        '</a>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.caption("v.1.0")
