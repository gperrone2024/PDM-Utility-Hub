# app.py
import streamlit as st
import hashlib

# Page Configuration - MUST BE FIRST
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Force light theme
st._config.set_option("theme.base", "light")

# --- AUTHENTICATION SYSTEM ---
def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def authenticate(username: str, password: str) -> bool:
    try:
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        if (username == st.secrets["auth"]["username"] and 
            input_hash == st.secrets["auth"]["password_hash"]):
            st.session_state.authenticated = True
            return True
        return False
    except:
        return False

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
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Initialize session and check auth
init_session()
if not st.session_state.authenticated:
    show_login_form()
    st.stop()

# Hide sidebar completely
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        .app-button-link {
            background-color: #e0f2fe !important;
            color: #0369a1 !important;
            border: 1px solid #bae6fd !important;
            padding: 1.2rem !important;
            border-radius: 0.5rem !important;
            margin-bottom: 0.75rem !important;
            width: 90% !important;
            min-height: 100px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            text-decoration: none !important;
            font-weight: bold !important;
            font-size: 1.05rem !important;
            transition: all 0.2s ease !important;
        }
        .app-button-link:hover {
            background-color: #bae6fd !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
        }
        .app-button-placeholder {
            background-color: #f8fafc !important;
            color: #64748b !important;
            border: 1px dashed #e2e8f0 !important;
            padding: 1.2rem !important;
            border-radius: 0.5rem !important;
            margin-bottom: 0.75rem !important;
            width: 90% !important;
            min-height: 100px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 0.7;
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

# Main content
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")

# App buttons grid
col1, col2 = st.columns(2)

with col1:
    if st.markdown("""
    <div class="app-container">
        <a href="javascript:void(0)" onclick="window.location.href='Bundle_Set_Images_Creator'" class="app-button-link">
            📦 Bundle & Set Images Creator
        </a>
        <p class="app-description">
            Automatically downloads, processes, and organizes images for product bundles and sets.
        </p>
    </div>
    """, unsafe_allow_html=True):
        st.session_state.page = "Bundle_Set_Images_Creator"
        st.experimental_rerun()

    st.markdown("""
    <div class="app-container">
        <div class="app-button-placeholder">
            🚧 Coming Soon
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.markdown("""
    <div class="app-container">
        <a href="javascript:void(0)" onclick="window.location.href='Repository_Image_Download_Renaming'" class="app-button-link">
            🖼️ Repository Image Download & Renaming
        </a>
        <p class="app-description">
            Downloads, resizes, and renames images from selected repositories.
        </p>
    </div>
    """, unsafe_allow_html=True):
        st.session_state.page = "Repository_Image_Download_Renaming"
        st.experimental_rerun()

st.markdown("""
<script>
// Handle navigation while preserving session state
document.querySelectorAll('.app-button-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = this.getAttribute('onclick').match(/'([^']+)'/)[1];
    });
});
</script>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("v1.0 | Secure Access System")

# Page routing
if 'page' in st.session_state:
    if st.session_state.page == "Bundle_Set_Images_Creator":
        st.switch_page("pages/Bundle_Set_Images_Creator.py")
    elif st.session_state.page == "Repository_Image_Download_Renaming":
        st.switch_page("pages/Repository_Image_Download_Renaming.py")
