# pdm_hub.py
import streamlit as st

st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS Globale ---
st.markdown(
    """
    <style>
    /* Imposta larghezza sidebar a 540px */
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
    }
    /* Nasconde la navigazione automatica della sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Rimosso sfondo forzato per l'area principale */
    /* section.main { background-color: #d8dfe6 !important; } */
    
    /* Imposta il contenitore interno trasparente con padding */
    div[data-testid="stAppViewContainer"] > section > div.block-container,
    .main .block-container {
         background-color: transparent !important;
         padding: 2rem 1rem 1rem 1rem !important;
         border-radius: 0 !important;
    }
    
    /* Stile base per i bottoni e i placeholder */
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
         content: "" !important;
         margin-right: 0 !important;
    }
    
    /* Stile per i bottoni cliccabili */
    .app-button-link {
        cursor: pointer;
    }
    .app-button-link:hover {
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Stile per il placeholder (non cliccabile) */
    .app-button-placeholder {
        opacity: 0.7;
        cursor: default;
        box-shadow: none;
        border-style: dashed;
    }
    .app-button-placeholder .icon {
         font-size: 1.5em;
    }
    
    /* Stile per la descrizione sotto i bottoni */
    .app-description {
        font-size: 0.9em;
        padding: 0 15px;
        text-align: justify;
        width: 90%;
        margin: 0 auto;
    }
    
    /* Stile per i link nella sidebar */
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

# --- Bottone per tornare all'Hub nella Sidebar ---
st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
st.sidebar.markdown("---")

# --- Contenuto Principale Hub ---
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
st.markdown("<br>", unsafe_allow_html=True)

# Layout a 2 colonne per i bottoni principali
col1, col2 = st.columns(2)

# --- Colonna 1: App Bundle e Coming Soon ---
with col1:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown(
        '<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">'
        '📦 Bundle & Set Images Creator'
        '</a>', unsafe_allow_html=True
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

# --- Colonna 2: App Renaming ---
with col2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown(
        '<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">'
        '🖼️ Repository Image Download & Renaming'
        '</a>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.caption("v.1.0")
