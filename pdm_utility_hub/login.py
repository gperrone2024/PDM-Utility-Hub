import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# Initialize authentication state if not present
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# If already logged in, redirect to the Hub page immediately
if st.session_state["authenticated"]:
    st.success("You are already logged in!")
    st.markdown(
        '<meta http-equiv="refresh" content="0; url=/pdm_utility_hub/pdm_hub" />',
        unsafe_allow_html=True,
    )
    st.stop()

st.title("🔒 Login to PDM Utility Hub")
st.markdown("Enter your credentials to access the Hub.")

# Input fields for username and password
username = st.text_input("Username", key="login_user").strip()
password = st.text_input("Password", type="password", key="login_pass").strip()

if st.button("Login"):
    if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
        st.session_state["authenticated"] = True
        st.success("Login successful! Redirecting to the Hub...")
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/pdm_utility_hub/pdm_hub" />',
            unsafe_allow_html=True,
        )
        st.stop()  # Stop further execution so the meta refresh takes effect
    else:
        st.error("Incorrect username or password.")
