# login.py
import streamlit as st

# Se disponibile, importa il componente per il redirect automatico
try:
    from streamlit_extras.switch_page_button import switch_page
except ImportError:
    switch_page = None

st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se l'utente è già loggato, evita di mostrare il form di login
if st.session_state.get("password_correct", False):
    st.success("Hai già effettuato il login!")
    if switch_page:
        switch_page("PDM Utility Hub")  # Assicurati che il nome della pagina dell'HUB sia corretto
    else:
        st.markdown("[Vai all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
    st.stop()

st.title("Login - PDM Utility Hub")
st.write("Inserisci le tue credenziali per accedere all'app.")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Accedi")
    if submitted:
        # Esegui qui il controllo delle credenziali (esempio semplice)
        if username == "PDM-Team" and password == "prova1234":
            st.session_state["password_correct"] = True
            st.success("Login effettuato con successo!")
            # Se disponibile, effettua il redirect automatico
            if switch_page:
                switch_page("PDM Utility Hub")
            else:
                st.markdown("[Clicca qui per andare all'HUB Principale](./pdm_utility_hub/pages/pdm_hub.py)")
            st.stop()
        else:
            st.error("Credenziali non valide. Riprova.")
