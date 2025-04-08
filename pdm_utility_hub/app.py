# app.py
import streamlit as st
import hashlib

# Page Configuration
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- AUTHENTICATION SYSTEM ---
def init_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def check_auth():
    init_auth()
    if not st.session_state.authenticated:
        show_login_form()
        st.stop()

def show_login_form():
    with st.container():
        st.markdown("""
        <div style='max-width: 400px; margin: 2rem auto; padding: 2rem; 
                    border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    background-color: white;'>
            <h2 style='color: #0369a1; text-align: center;'>
                🔐 PDM Utility Hub Login
            </h2>
        """, unsafe_allow_html=True)
        
        with st.form("Login"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password").strip()
            
            if st.form_submit_button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)

def authenticate(username: str, password: str) -> bool:
    try:
        stored_username = st.secrets["auth"]["username"]
        stored_hash = st.secrets["auth"]["password_hash"]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return (username == stored_username and input_hash == stored_hash)
    except Exception:
        st.error("Authentication system error")
        return False

# --- MAIN APP ---
check_auth()

# Fixed sidebar navigation using markdown instead of page_link
st.sidebar.markdown('[🏠 **PDM Utility Hub**](/)', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Main content
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")

# App buttons
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="app-container">
        <a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link">
            📦 Bundle & Set Images Creator
        </a>
        <p class="app-description">
            Automatically downloads, processes, and organizes images for product bundles and sets.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="app-container">
        <a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link">
            🖼️ Repository Image Download & Renaming
        </a>
        <p class="app-description">
            Downloads, resizes, and renames images from selected repositories.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("v1.0 | Secure Access System")

# CSS (same as before)
st.markdown("""
    <style>
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
    }
    [data-testid="stSidebarNav"] { display: none; }
    .app-button-link {
        background-color: #f0f9ff !important;
        color: #0369a1 !important;
        border: 1px solid #bae6fd !important;
        padding: 1.2rem !important;
        border-radius: 0.5rem !important;
        margin-bottom: 1rem !important;
        display: block !important;
        text-align: center !important;
        text-decoration: none !important;
    }
    .app-button-link:hover {
        background-color: #e0f2fe !important;
    }
    .app-description {
        font-size: 0.9em;
        color: #334155;
        padding: 0 15px;
        text-align: justify;
    }
    </style>
""", unsafe_allow_html=True)
