import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Login", layout="centered")

# Inizializza lo stato di autenticazione se non presente
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Se già autenticato, reindirizza subito al Hub
if st.session_state["authenticated"]:
    st.success("Sei già loggato!")
    components.html(
        """
        <script>
            window.location.href = "/pdm_utility_hub/pdm_hub";
        </script>
        """,
        height=0,
    )
    st.stop()

st.title("🔒 Login to PDM Utility Hub")
st.markdown("Inserisci le tue credenziali per accedere al Hub.")

# Campi di input per username e password
username = st.text_input("Username", key="login_user").strip()
password = st.text_input("Password", type="password", key="login_pass").strip()

if st.button("Login", key="login_button"):
    if username == st.secrets["LOGIN_USERNAME"] and password == st.secrets["LOGIN_PASSWORD"]:
        st.session_state["authenticated"] = True
        st.success("Login successful! Redirecting to the Hub...")
        # Redirect con JavaScript
        components.html(
            """
            <script>
                window.location.href = "/pdm_utility_hub/pdm_hub";
            </script>
            """,
            height=0,
        )
        st.stop()  # Ferma l'esecuzione per consentire il redirect
    else:
        st.error("Incorrect username or password.")
