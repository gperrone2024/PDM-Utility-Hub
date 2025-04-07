import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# Initialize authentication state if not already set
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# If already logged in, show link to Hub and stop execution
if st.session_state["authenticated"]:
    st.success("Sei già loggato!")
    st.markdown("[Clicca qui per accedere al Hub](/pdm_utility_hub/pdm_hub)")
    st.stop()

st.title("🔒 Login to PDM Utility Hub")
st.markdown("Inserisci le tue credenziali per accedere al Hub.")

# Input fields for username and password
username = st.text_input("Username", key="login_user").strip()
password = st.text_input("Password", type="password", key="login_pass").strip()

if st.button("Login", key="login_button"):
    if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
        st.session_state["authenticated"] = True
        st.success("Login successful! Redirecting to the Hub...")
        # Instead of an automatic redirect, provide a clickable link:
        st.markdown("[Click here to go to the Hub](/pdm_utility_hub/pdm_hub)")
        st.stop()  # Stop further execution to prevent the login form from re-rendering
    else:
        st.error("Incorrect username or password.")
