# pdm_hub.py
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="PDM Utility Hub",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State for Authentication ---
st.session_state.setdefault("authenticated", False)

# --- Function to Verify Login ---
def check_password(username, password):
    """
    Checks the username and password using credentials stored in st.secrets.
    The password is stored in plain text in st.secrets.
    """
    try:
        correct_username = st.secrets["LOGIN_USERNAME"]
        correct_password = st.secrets["LOGIN_PASSWORD"]
        return username == correct_username and password == correct_password
    except KeyError:
        st.error("Error: Login credentials not found in secrets. Ensure .streamlit/secrets.toml is configured.")
        return False
    except Exception as e:
        st.error(f"Error during login verification: {e}")
        return False

# --- Login Screen (shown only when not authenticated) ---
if not st.session_state["authenticated"]:
    # Hide the sidebar while on the login page
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

    # Use .strip() to remove any accidental whitespace
    login_username = st.text_input("Username", key="login_user", value="").strip()
    login_password = st.text_input("Password", type="password", key="login_pass", value="").strip()

    if st.button("Login", key="login_button"):
        if check_password(login_username, login_password):
            st.session_state["authenticated"] = True
            st.rerun()  # Rerun the app to display the authenticated content
        else:
            st.error("Incorrect username or password.")

# --- Main Hub (Authenticated View) ---
else:
    # Global CSS for the authenticated view
    st.markdown(
        """
        <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] > div:first-child {
            width: 540px !important;
            min-width: 540px !important;
            max-width: 540px !important;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Main container styling */
        div[data-testid="stAppViewContainer"] > section > div.block-container,
        .main .block-container {
             background-color: transparent !important;
             padding: 2rem 1rem 1rem 1rem !important;
             border-radius: 0 !important;
        }
        /* App button and placeholder styling */
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

    # Sidebar: Display a link to the hub and a logout button
    st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        st.session_state.pop("login_user", None)
        st.session_state.pop("login_pass", None)
        st.rerun()

    st.sidebar.markdown("---")

    # Main Hub Content
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Column 1: Bundle & Set Images Creator and Coming Soon placeholder
    with col1:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Repository Image Download & Renaming
    with col2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
        st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v.1.0")
