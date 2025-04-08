import streamlit as st
import hashlib

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Page config
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Authentication functions
def authenticate(username: str, password: str) -> bool:
    try:
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return (username == st.secrets["auth"]["username"] and 
                input_hash == st.secrets["auth"]["password_hash"])
    except:
        return False

# Show login form if not authenticated
if not st.session_state.authenticated:
    with st.form("Login"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        
        if st.form_submit_button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

# Main app content (only for authenticated users)
st.title("🛠️ PDM Utility Hub")
st.markdown("---")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📦 Bundle & Set Images Creator", use_container_width=True):
        st.session_state.current_page = "Bundle_Set_Images_Creator"
        st.rerun()

with col2:
    if st.button("🖼️ Repository Image Download & Renaming", use_container_width=True):
        st.session_state.current_page = "Repository_Image_Download_Renaming"
        st.rerun()

st.markdown("---")
st.caption("v1.0 | Secure Access System")

# Page routing
if 'current_page' in st.session_state:
    if st.session_state.current_page == "Bundle_Set_Images_Creator":
        from pages.Bundle_Set_Images_Creator import show_page
        show_page()
    elif st.session_state.current_page == "Repository_Image_Download_Renaming":
        from pages.Repository_Image_Download_Renaming import show_page
        show_page()
