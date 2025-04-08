import streamlit as st

st.set_page_config(page_title="Login - PDM Utility Hub", page_icon="🔑")

# Se già loggato, mostra un link cliccabile (fallback per Cloud)
if st.session_state.get("logged_in", False):
    st.markdown("""
        ✅ Sei già loggato!  
        [Clicca qui per entrare nell'HUB →](./pages/pdm_hub.py)
    """)
else:
    st.title("🔑 Login - PDM Utility Hub")
    st.write("Clicca il pulsante per accedere (senza password).")

    if st.button("Login"):
        st.session_state["logged_in"] = True
        st.success("Accesso effettuato!")
        # Mostra un link cliccabile (fallback per problemi di reindirizzamento)
        st.markdown("[Clicca qui per entrare nell'HUB →](./pages/pdm_hub.py)")
