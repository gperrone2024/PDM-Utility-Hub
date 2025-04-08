# app.py
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

# --- SECURE AUTHENTICATION SYSTEM ---
def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'auth_attempted' not in st.session_state:
        st.session_state.auth_attempted = False

def check_auth() -> bool:
    """Check if user is authenticated."""
    init_session_state()
    if not st.session_state.authenticated:
        show_login_form()
        st.stop()
    return True

def show_login_form():
    """Display secure login form."""
    with st.container():
        st.markdown("""
        <div style='max-width: 400px; margin: 2rem auto; padding: 2rem; 
                    border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    background-color: white;'>
            <h2 style='color: #0369a1; text-align: center; margin-bottom: 1.5rem;'>
                🔐 PDM Utility Hub Login
            </h2>
        """, unsafe_allow_html=True)
        
        with st.form("Login"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password").strip()
            
            if st.form_submit_button("Login", use_container_width=True):
                st.session_state.auth_attempted = True
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Secure debug information
        if st.session_state.auth_attempted:
            st.markdown("---")
            st.warning("Troubleshooting tips:")
            st.write("- Check for typos in username/password")
            st.write("- Verify caps lock is off")
            st.write("- Contact admin if you've forgotten credentials")

def authenticate(username: str, password: str) -> bool:
    """Authenticate user against secrets."""
    try:
        stored_username = st.secrets["auth"]["username"]
        stored_hash = st.secrets["auth"]["password_hash"]
        salt = st.secrets["auth"]["salt"]
        
        if not username or not password:
            return False
            
        return (hmac.compare_digest(username, stored_username) and 
                verify_password(password, stored_hash, salt))
    except KeyError:
        st.error("Authentication system not properly configured")
        return False

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Securely verify password against stored hash."""
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        (password + salt).encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return hmac.compare_digest(
        base64.b64encode(new_hash).decode('utf-8'),
        stored_hash
    )

# --- GLOBAL CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
    }
    [data-testid="stSidebarNav"] { display: none; }
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
    .app-button-link {
        background-color: #f0f9ff !important;
        color: #0369a1 !important;
        border: 1px solid #bae6fd !important;
    }
    .app-button-link:hover {
        background-color: #e0f2fe !important;
        border-color: #7dd3fc !important;
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

# --- MAIN APP ---
if not check_auth():
    st.stop()

# Authenticated content below
st.sidebar.page_link("app.py", label="🏠 **PDM Utility Hub**")
st.sidebar.markdown("---")

st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="app-container">
        <a href="Bundle_Set_Images_Creator" target="_self" class="app-button-link">
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
        <a href="Repository_Image_Download_Renaming" target="_self" class="app-button-link">
            🖼️ Repository Image Download & Renaming
        </a>
        <p class="app-description">
            Downloads, resizes, and renames images from selected repositories.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("v1.0 | Secure Access System")
