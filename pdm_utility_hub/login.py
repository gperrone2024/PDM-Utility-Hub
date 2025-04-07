import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# Initialize authentication state if not present
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.title("🔒 Login to PDM Utility Hub")

# Input fields for username and password
username = st.text_input("Username", key="login_user").strip()
password = st.text_input("Password", type="password", key="login_pass").strip()

if st.button("Login"):
    if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
        st.session_state["authenticated"] = True
        st.success("Login successful! Redirecting to the Hub...")
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    else:
        st.error("Incorrect username or password.")
