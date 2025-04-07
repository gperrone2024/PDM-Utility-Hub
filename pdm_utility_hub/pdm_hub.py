import streamlit as st

# --- Configurazione Pagina (DEVE ESSERE LA PRIMA E UNICA chiamata st.*) ---
# Scegli un layout (es. 'wide' o 'centered') che vada bene sia per il login
# che per l'app principale, o quello che preferisci per l'app principale.
st.set_page_config(
    page_title="PDM Utility Hub",
    layout="wide",  # Puoi scegliere 'centered' se preferisci per il login
    initial_sidebar_state="auto" # La sidebar verrà nascosta comunque prima del login
)

# --- Funzione di Controllo Password ---
def check_password():
    """Restituisce True se username e password sono corretti."""
    # Accede ai valori inseriti nel form tramite st.session_state
    # grazie ai 'key' assegnati ai widget di input.
    correct_username = "PDM-Team"
    correct_password = "prova1234"

    if (
        st.session_state.get("username") == correct_username and
        st.session_state.get("password") == correct_password
    ):
        st.session_state["password_correct"] = True
        # Non è strettamente necessario pulire, ma può essere una buona pratica
        # st.session_state.pop("username", None)
        # st.session_state.pop("password", None)
    else:
        st.session_state["password_correct"] = False

# --- Inizializzazione dello stato di Login ---
# Se la chiave 'password_correct' non esiste in session_state, la crea e imposta a False
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

# --- Blocco di Login: Mostrato solo se NON loggato ---
if not st.session_state["password_correct"]:

    # Mostra solo il titolo e il form
    st.title("PDM Utility Hub")
    st.markdown("---")

    # Usa un form per il login
    with st.form("login_form"):
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            check_password() # Verifica le credenziali al submit
            if not st.session_state["password_correct"]:
                st.error("😕 Username o password errati.")
            else:
                # Se le credenziali sono corrette, forza un rerun dell'app.
                # Al prossimo giro, l'if not st.session_state["password_correct"] sarà False
                # e verrà mostrato il contenuto principale.
                st.rerun()

    # --- STOP FONDAMENTALE ---
    # Interrompe l'esecuzione dello script qui se l'utente non è loggato.
    # Questo impedisce la visualizzazione del resto della pagina e
    # impedisce a Streamlit di scoprire/mostrare le pagine nella cartella 'pages'.
    st.stop()

# --- Sezione Principale dell'App (Visibile SOLO DOPO il login) ---
# Se lo script arriva a questo punto, significa che l'utente è loggato.
# Streamlit ora mostrerà anche la sidebar con le pagine della cartella 'pages'.

st.sidebar.success("Login effettuato con successo!")

# Bottone di Logout nella sidebar
if st.sidebar.button("Logout"):
    st.session_state["password_correct"] = False
    # Opzionale: pulisci le credenziali dalla sessione
    st.session_state.pop("username", None)
    st.session_state.pop("password", None)
    st.rerun() # Ricarica per mostrare nuovamente la pagina di login

# --- Contenuto originale della tua pagina pdm_hub.py ---
# Metti qui il codice che vuoi mostrare nella pagina principale dell'hub
# dopo che l'utente ha effettuato il login.

st.title("Benvenuto nel PDM Utility Hub!")
st.markdown("---")
st.write("Seleziona uno strumento dalla barra laterale a sinistra.")
st.info("Questa è la pagina principale dell'hub. Le funzionalità specifiche si trovano nelle pagine elencate nella sidebar.")

# Esempio: Potresti aggiungere qui altre informazioni, immagini, ecc.
# st.image("path/to/your/logo.png")
