import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# Initialize authentication state if not present
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# If the user is already authenticated, prompt them to go to the Hub
if st.session_state["authenticated"]:
    st.success("Login successful!")
    st.markdown("Go to the [PDM Utility Hub](pdm_hub.py)")
    st.stop()

st.title("🔒 Login to PDM Utility Hub")

# Input fields for username and password with whitespace stripped
username = st.text_input("Username", key="login_user").strip()
password = st.text_input("Password", type="password", key="login_pass").strip()

if st.button("Login"):
    # Compare entered credentials with plain-text values in st.secrets
    if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
        st.session_state["authenticated"] = True
        st.success("Login successful! Redirecting to the Hub...")
        st.rerun()  # This will reload the page; then the above check will show the link to the Hub.
    else:
        st.error("Incorrect username or password.")
