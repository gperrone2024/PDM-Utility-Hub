import streamlit as st

st.set_page_config(page_title="PDM Utility Hub", layout="centered")

# Check if user is authenticated; if not, stop and prompt to log in
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Please log in first!")
    st.stop()

# Main Hub Content (displayed only when authenticated)
st.title("🛠️ PDM Utility Hub")
st.markdown("---")
st.markdown("**Welcome to the Product Data Management Utility Hub. Select an application below to get started.**")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Column 1: Example application links
with col1:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<a href="/Bundle_Set_Images_Creator" target="_self" class="app-button-link" data-testid="stPageLink">📦 Bundle & Set Images Creator</a>', unsafe_allow_html=True)
    st.markdown('<p class="app-description">Automatically downloads, processes, and organizes images for product bundles and sets.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<div class="app-button-placeholder"><span class="icon">🚧</span> Coming Soon</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Column 2: Another example application link
with col2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    st.markdown('<a href="/Repository_Image_Download_Renaming" target="_self" class="app-button-link" data-testid="stPageLink">🖼️ Repository Image Download & Renaming</a>', unsafe_allow_html=True)
    st.markdown('<p class="app-description">Downloads, resizes, and renames images from selected repositories (e.g. Switzerland, Farmadati).</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("v.1.0")

# Optionally, add a logout button in the sidebar
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    # Remove stored login fields (if needed)
    st.session_state.pop("login_user", None)
    st.session_state.pop("login_pass", None)
    st.experimental_rerun()
