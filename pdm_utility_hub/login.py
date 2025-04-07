import streamlit as st

st.set_page_config(page_title="PDM Utility Hub", layout="centered")

# Initialize session state if not already set
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Login Section ---
if not st.session_state["authenticated"]:
    st.title("🔒 Login to PDM Utility Hub")
    st.markdown("Enter your credentials to access the Hub.")

    # Input fields for username and password with whitespace stripped
    username = st.text_input("Username", key="login_user").strip()
    password = st.text_input("Password", type="password", key="login_pass").strip()

    if st.button("Login"):
        # Compare entered values to the plain-text credentials in st.secrets
        if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
            st.session_state["authenticated"] = True
            st.success("Login successful!")
            st.experimental_rerun()  # Reload the page to show the hub content
        else:
            st.error("Incorrect username or password.")

# --- Hub Content (Displayed only after successful login) ---
else:
    st.title("🛠️ PDM Utility Hub")
    st.markdown("---")
    st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Column 1: Example application links
    with col1:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown(
            '<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>',
            unsafe_allow_html=True,
        )
        st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Another example application link
    with col2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        st.markdown(
            '<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">🖼️ Repository Image Download & Renaming</a>',
            unsafe_allow_html=True,
        )
        st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v.1.0")

    # Optional Logout Button in the Sidebar
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state.pop("login_user", None)
        st.session_state.pop("login_pass", None)
        st.experimental_rerun()
