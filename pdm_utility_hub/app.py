# app.py (main page)
import streamlit as st
import hashlib
import hmac
import base64
import os
from typing import Tuple

# Page configuration
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)
# Debug temporaneo (rimuovi dopo)

# --- SECURE AUTHENTICATION SYSTEM ---
def init_session_state():
    """Initialize session state for authentication."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def check_auth() -> bool:
    """Check if user is authenticated across all pages."""
    init_session_state()
    if not st.session_state.authenticated:
        show_login_form()
        st.stop()  # Stop execution if not authenticated
    return True

def show_login_form():
    """Display the login form with custom styling."""
    with st.container():
        st.markdown("""
        <div style='max-width: 400px; margin: 0 auto; padding: 2rem; 
                    border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    background-color: white;'>
            <h2 style='color: #0369a1; text-align: center; margin-bottom: 1.5rem;'>
                🔐 PDM Utility Hub Login
            </h2>
        """, unsafe_allow_html=True)
        
        with st.form("Login"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)

def authenticate(username: str, password: str) -> bool:
    """Authenticate user against secrets."""
    stored_username = st.secrets.get("auth.username", "")
    stored_password_hash = st.secrets.get("auth.password_hash", "")
    salt = st.secrets.get("auth.salt", "")
    
    if (username == stored_username and 
        verify_password(password, stored_password_hash, salt)):
        return True
    return False

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Securely verify password against stored hash."""
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)

def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """Generate secure password hash with salt."""
    if salt is None:
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')
    
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        (password + salt).encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return base64.b64encode(hashed).decode('utf-8'), salt
    st.write("Debug auth values:")
st.write(f"Input username: {username}")
st.write(f"Stored username: {st.secrets['auth']['username']}")
st.write(f"Salt match: {salt == st.secrets['auth']['salt']}")

# --- GLOBAL CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    div[data-testid="stAppViewContainer"] > section > div.block-container,
    .main .block-container {
        background-color: transparent !important;
        padding: 2rem 1rem 1rem 1rem !important;
        border-radius: 0 !important;
    }
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
        transition: all 0.2s ease;
        border: 1px solid #c4daee;
    }
    .app-button-link {
        background-color: #f0f9ff !important;
        color: #0369a1 !important;
        border: 1px solid #bae6fd !important;
    }
    .app-button-link:hover {
        background-color: #e0f2fe !important;
        border-color: #7dd3fc !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .app-button-placeholder {
        background-color: #f8fafc !important;
        color: #64748b !important;
        opacity: 0.7;
        cursor: default;
        box-shadow: none;
        border-style: dashed;
        border-color: #e2e8f0;
    }
    .app-description {
        font-size: 0.9em;
        color: #334155;
        padding: 0 15px;
        text-align: justify;
        width: 90%;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP CONTENT ---
if not check_auth():
    st.stop()  # This will show login form and stop execution

# Only authenticated users will see content below

# Sidebar navigation
st.sidebar.page_link("app.py", label="🏠 **PDM Utility Hub**")
st.sidebar.markdown("---")

# Main content
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
st.markdown("<br>", unsafe_allow_html=True)

# App buttons in columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<a href="Bundle_Set_Images_Creator" target="_self" class="app-button-link">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
    st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<a href="Repository_Image_Download_Renaming" target="_self" class="app-button-link">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
    st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("v1.0")

