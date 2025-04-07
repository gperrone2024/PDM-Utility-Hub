# pdm_hub.py
import streamlit as st
from passlib.hash import pbkdf2_sha256  # Used for password hash verification
import time  # Sometimes needed for st.rerun()

# --- Page Configuration ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State for Authentication Persistently ---
st.session_state.setdefault("authenticated", False)

# --- Function to Verify Login ---
def check_password(username, password):
    """Checks username and password using Streamlit secrets and passlib."""
    try:
        correct_username = st.secrets["LOGIN_USERNAME"]
        hashed_password = st.secrets["LOGIN_HASHED_PASSWORD"]
        return username == correct_username and pbkdf2_sha256.verify(password, hashed_password)
    except KeyError:
        st.error("Error: Login credentials not found in secrets. Ensure .streamlit/secrets.toml is configured.")
        return False
    except Exception as e:
        st.error(f"Error during login verification: {e}")
        return False

# --- Login Screen ---
if not st.session_state["authenticated"]:
    # Hide sidebar when user is not authenticated
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🔒 Login - PDM Utility Hub")
    st.markdown("Enter your credentials to access the hub.")

    login_username = st.text_input("Username", key="login_user", value="")
    login_password = st.text_input("Password", type="password", key="login_pass", value="")

    if st.button("Login", key="login_button"):
        if check_password(login_username, login_password):
            st.session_state["authenticated"] = True
            st.rerun()  # Rerun the app to display the authenticated content
        else:
            st.error("Incorrect username or password.")

# --- Main Hub (Authenticated View) ---
else:
    # Global CSS for the authenticated hub
    st.markdown(
        """
        <style>
        /* Set sidebar width */
        [data-testid="stSidebar"] > div:first-child {
            width: 540px !important;
            min-width: 540px !important;
            max-width: 540px !important;
        }
        /* Hide automatic navigation in sidebar */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Make the main container background transparent and adjust padding */
        div[data-testid="stAppViewContainer"] > section > div.block-container,
        .main .block-container {
             background-color: transparent !important;
             padding: 2rem 1rem 1rem 1rem !important;
             border-radius: 0 !important;
        }
        /* Styles for app buttons and placeholders */
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

    # Sidebar: Hub Link and Logout Button
    st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.sidebar.markdown("---")

    # Main Hub Content
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Column 1: Bundle App and Coming Soon Placeholder
    with col1:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Repository Image Download & Renaming App
    with col2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v.1.0")
