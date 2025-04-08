import streamlit as st

# Controlla se l'utente è loggato, altrimenti mostra errore
if not st.session_state.get("logged_in", False):
    st.error("❌ Accesso negato. Effettua il login.")
    st.markdown("[Vai alla pagina di Login →](../login.py)")
    st.stop()  # Blocca l'esecuzione del resto della pagina

# Se l'utente è loggato, mostra la pagina principale
st.set_page_config(page_title="PDM Hub", page_icon="🏠")
st.title("🏠 Benvenuto nel PDM Utility Hub!")
st.write("Accesso autorizzato ✅")

if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.markdown("[Torna al Login →](../login.py)")
