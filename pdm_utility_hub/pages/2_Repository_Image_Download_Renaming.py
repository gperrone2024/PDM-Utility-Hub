# pages/2_Repository_Image_Download_Renaming.py
import streamlit as st
import pandas as pd
import csv
import os
import zipfile
import shutil
from PIL import Image, ImageOps, ImageChops, UnidentifiedImageError
from io import BytesIO
import tempfile
import uuid
import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import requests
from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
from zeep.cache import InMemoryCache
from zeep.plugins import HistoryPlugin
# NOTA: import time NON è presente nel codice fornito, quindi non viene aggiunto.

st.set_page_config(
    page_title="Image Download & Renaming",
    layout="centered", # O 'wide'
    initial_sidebar_state="expanded" # Sidebar visibile
)

# --- CSS Globale per nascondere navigazione default e impostare larghezza sidebar ---
# *** CSS MODIFICATO PER ADATTAMENTO TEMA E LARGHEZZA 540px ***
st.markdown(
    """
    <style>
    /* Imposta larghezza sidebar a 540px e FORZA con !important */
    [data-testid="stSidebar"] > div:first-child {
        width: 540px !important;
        min-width: 540px !important;
        max-width: 540px !important;
        /* background-color: #ecf0f1 !important; */ /* RIMOSSO - Lascia gestire al tema */
        padding: 10px !important; /* Mantenuto padding */
    }
    /* Nasconde la navigazione automatica generata da Streamlit nella sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Rimosso sfondo forzato per l'AREA PRINCIPALE - Lascia gestire al tema */
    /* section.main {
        background-color: #d8dfe6 !important; /* RIMOSSO */
    /* } */

    /* Rendi trasparente il contenitore interno e mantieni il padding */
    /* Questo permette allo sfondo del tema di essere visibile */
    div[data-testid="stAppViewContainer"] > section > div.block-container {
         background-color: transparent !important;
         padding: 2rem 1rem 1rem 1rem !important; /* Padding per contenuto */
         border-radius: 0 !important; /* Nessun bordo arrotondato interno */
    }
    .main .block-container {
         background-color: transparent !important;
         padding: 2rem 1rem 1rem 1rem !important;
         border-radius: 0 !important;
    }


    /* Stile base per i bottoni/placeholder delle app (dall'hub) - MODIFICATO */
    /* Anche se non usati direttamente qui, li adattiamo per coerenza */
    .app-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .app-button-link, .app-button-placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.2rem 1.5rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.05rem;
        width: 90%;
        min-height: 100px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        margin-bottom: 0.75rem;
        text-align: center;
        line-height: 1.4;
        transition: background-color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        /* Rimossi color, background-color, border specifici */
        /* color: #343a40; */ /* RIMOSSO */
        border: 1px solid var(--border-color, #cccccc); /* Usa variabile CSS o fallback */
    }
     .app-button-link svg, .app-button-placeholder svg,
     .app-button-link .icon, .app-button-placeholder .icon {
         margin-right: 0.6rem;
         flex-shrink: 0;
     }
    .app-button-link > div[data-testid="stText"] > span:before {
        content: "" !important; margin-right: 0 !important;
    }

    /* Stile per bottoni cliccabili (dall'hub) - Rimosso colore specifico */
    .app-button-link {
        /* background-color: #f5faff; */ /* RIMOSSO */
        /* border: 1px solid #c4daee; */ /* RIMOSSO */
        cursor: pointer;
    }
    .app-button-link:hover {
        /* background-color: #eaf2ff; */ /* RIMOSSO */
        /* border-color: #a9cce3; */ /* RIMOSSO */
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    /* Stile Placeholder Coming Soon (non cliccabile) (dall'hub) - MODIFICATO */
    .app-button-placeholder {
        /* background-color: #f1f3f5; */ /* RIMOSSO */
        opacity: 0.7;
        cursor: default;
        box-shadow: none;
        /* color: #868e96; */ /* RIMOSSO */
        border-style: dashed;
        /* border: 1px dashed #cccccc; */ /* RIMOSSO - Usa border generico sopra */
    }
     .app-button-placeholder .icon {
         font-size: 1.5em;
     }


    /* Stile per descrizione sotto i bottoni (dall'hub) - MODIFICATO */
     .app-description {
        font-size: 0.9em;
        /* color: #343a40; */ /* RIMOSSO */
        padding: 0 15px;
        text-align: justify;
        width: 90%;
        margin: 0 auto;
     }

     /* Stili specifici di QUESTA app (Renaming) - MODIFICATO */
     /* --- MODIFICA: Aumentata dimensione font titolo sidebar --- */
     /* Rimossi colori specifici, mantenute dimensioni/pesi */
     .sidebar-title {font-size: 36px; font-weight: bold; /* color: #2c3e50; */ margin-bottom: 0px;}
     .sidebar-subtitle {font-size: 18px; /* color: #2c3e50; */ margin-top: 10px; margin-bottom: 5px;}
     .sidebar-desc {font-size: 16px; /* color: #2c3e50; */ margin-top: 5px; margin-bottom: 20px;}
     .server-select-label {font-size: 20px; font-weight: bold; margin-bottom: 5px;}

     /* Rimossi colori specifici per il bottone download, mantenuto resto stile */
     /* Lasciamo che Streamlit gestisca i colori dei bottoni standard */
     /* .stDownloadButton>button {
         background-color: #3498db; /* RIMOSSO */
         /* color: black; */ /* RIMOSSO */
         /* font-weight: bold;
         border: none;
         padding: 10px 24px;
         font-size: 16px;
         border-radius: 4px;
     } */

     /* Aggiusta colore link nella sidebar per coerenza tema (opzionale ma consigliato) */
    [data-testid="stSidebar"] a:link, [data-testid="stSidebar"] a:visited {
        /* color: inherit; */ /* Eredita colore dal tema */
        text-decoration: none;
    }
    [data-testid="stSidebar"] a:hover {
        text-decoration: underline; /* O altro effetto hover desiderato */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Bottone per tornare all'Hub nella Sidebar ---
st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
st.sidebar.markdown("---") # Separatore opzionale

# ----- LOGIN RIMOSSO -----

# ----- Sidebar Content -----
# --- MODIFICA: Titolo sidebar (nessuna modifica al codice, solo CSS) ---
st.sidebar.markdown("<div class='sidebar-title'>PDM Image Download and Renaming App</div>", unsafe_allow_html=True)
# --- MODIFICA: Sottotitolo in grassetto ---
st.sidebar.markdown("<div class='sidebar-subtitle'>**What This App Does**</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class='sidebar-desc'>
- 📥 Downloads images from the selected server<br>
- 🔄 Resizes images to 1000x1000 in JPEG<br>
- 🏷️ Renames with a '-h1' suffix
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<div class='server-select-label'>Select Server Image</div>", unsafe_allow_html=True)
server_country = st.sidebar.selectbox("", options=["Switzerland", "Farmadati", "coming soon"], index=0, key="server_select_renaming")

# ----- Session State (Originale) -----
if "renaming_uploader_key" not in st.session_state:
    st.session_state.renaming_uploader_key = str(uuid.uuid4())
if "renaming_session_id" not in st.session_state:
     st.session_state.renaming_session_id = str(uuid.uuid4())

# Function to combine SKUs from file and manual input (Originale)
def get_sku_list(uploaded_file_obj, manual_text):
    # ... (codice funzione invariato) ...
    sku_list = []
    df_file = None
    if uploaded_file_obj is not None:
        try:
            if uploaded_file_obj.name.lower().endswith("csv"):
                uploaded_file_obj.seek(0)
                sample = uploaded_file_obj.read(1024).decode("utf-8", errors='ignore')
                uploaded_file_obj.seek(0)
                delimiter = ';' # Default
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=';,\t')
                    delimiter = dialect.delimiter
                except Exception:
                    pass # Use default
                df_file = pd.read_csv(uploaded_file_obj, delimiter=delimiter, dtype=str)
            else:
                df_file = pd.read_excel(uploaded_file_obj, dtype=str)

            sku_column = None
            for col in df_file.columns:
                if col.strip().lower() == "sku":
                    sku_column = col
                    break
            if sku_column:
                file_skus = df_file[sku_column].dropna().astype(str).str.strip()
                sku_list.extend(file_skus[file_skus != ''].tolist())
            else:
                 st.warning("Column 'sku' not found in file.")

        except Exception as e:
            st.error(f"Error reading file: {e}")

    if manual_text:
        manual_skus = [line.strip() for line in manual_text.splitlines() if line.strip()]
        sku_list.extend(manual_skus)

    unique_sku_list = list(dict.fromkeys(sku for sku in sku_list if sku))
    return unique_sku_list

# ======================================================
# SECTION: Switzerland
# ======================================================
if server_country == "Switzerland":
    # ... (Codice sezione Svizzera invariato, incluso il bottone Reset) ...
    st.header("Switzerland Server Image Processing")
    st.markdown("""
    :information_source: **How to use:**

    - :arrow_right: **Create a list of products:** Rename the column **sku** or use the Quick Report in Akeneo.
    - :arrow_right: **In Akeneo, select the following options:**
        - **File Type:** CSV or Excel
        - **All Attributes or Grid Context:** (for Grid Context, select ID)
        - **With Codes**
        - **Without Media**
    """)

    # --- Bottone Reset SPOSTATO QUI ---
    if st.button("🧹 Clear Cache and Reset Data"):
        keys_to_remove = [k for k in st.session_state.keys() if k.startswith("renaming_") or k in ["uploader_key", "session_id", "processing_done", "zip_path", "error_path", "farmadati_zip", "farmadati_errors", "farmadati_ready", "process_images_switzerland", "process_images_farmadati"]]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.renaming_uploader_key = str(uuid.uuid4())
        st.info("Cache cleared. Please re-upload your file.")
        # NOTA: time.sleep(1) è stato rimosso perché 'time' non è importato nel codice fornito
        st.rerun()

    manual_input = st.text_area("Or paste your SKUs here (one per line):", key="manual_input_switzerland")
    uploaded_file = st.file_uploader("Upload file (Excel or CSV)", type=["xlsx", "csv"], key=st.session_state.renaming_uploader_key)

    if st.button("Search Images", key="process_switzerland"):
        st.session_state.renaming_start_processing_ch = True
        st.session_state.renaming_processing_done_ch = False
        if "renaming_zip_path_ch" in st.session_state: del st.session_state.renaming_zip_path_ch
        if "renaming_error_path_ch" in st.session_state: del st.session_state.renaming_error_path_ch


    if st.session_state.get("renaming_start_processing_ch") and not st.session_state.get("renaming_processing_done_ch", False):
        sku_list = get_sku_list(uploaded_file, manual_input)
        if not sku_list:
            st.warning("Please upload a file or paste some SKUs to process.")
            st.session_state.renaming_start_processing_ch = False
        else:
            st.info(f"Processing {len(sku_list)} SKUs for Switzerland...")
            error_codes = []
            total_count = len(sku_list)
            progress_bar = st.progress(0, text="Starting processing...")

            def get_image_url(product_code):
                pharmacode = str(product_code)
                if pharmacode.upper().startswith("CH"):
                    pharmacode = pharmacode[2:].lstrip("0")
                else:
                    pharmacode = pharmacode.lstrip("0")
                if not pharmacode: return None
                return f"https://documedis.hcisolutions.ch/2020-01/api/products/image/PICFRONT3D/Pharmacode/{pharmacode}/F"

            def process_and_save(original_sku, content, download_folder):
                try:
                    img = Image.open(BytesIO(content))
                    if img.mode != 'L': gray = img.convert("L")
                    else: gray = img
                    extrema = gray.getextrema()
                    if extrema == (0, 0): raise ValueError("Empty image (black)")
                    if extrema == (255, 255): raise ValueError("Empty image (white)")

                    img = ImageOps.exif_transpose(img)
                    bg = Image.new(img.mode, img.size, (255, 255, 255))
                    diff = ImageChops.difference(img, bg)
                    bbox = diff.getbbox()
                    if bbox: img = img.crop(bbox)

                    if img.width == 0 or img.height == 0: raise ValueError("Image empty after trim")

                    img.thumbnail((1000, 1000), Image.LANCZOS)
                    canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
                    offset_x = (1000 - img.width) // 2
                    offset_y = (1000 - img.height) // 2
                    canvas.paste(img, (offset_x, offset_y))
                    new_filename = f"{original_sku}-h1.jpg"
                    img_path = os.path.join(download_folder, new_filename)
                    canvas.save(img_path, "JPEG", quality=95)
                    return True
                except Exception as e:
                    return False

            async def fetch_and_process_image(session, product_code, download_folder):
                image_url = get_image_url(product_code)
                if image_url is None:
                    error_codes.append(product_code)
                    return
                try:
                    async with session.get(image_url, timeout=30) as response:
                        if response.status == 200:
                            content = await response.read()
                            if not content:
                                error_codes.append(product_code)
                                return
                            success = await asyncio.to_thread(process_and_save, product_code, content, download_folder)
                            if not success:
                                error_codes.append(product_code)
                        else:
                            error_codes.append(product_code)
                except Exception as e:
                    error_codes.append(product_code)

            async def run_processing(download_folder):
                connector = aiohttp.TCPConnector(limit=50)
                async with aiohttp.ClientSession(connector=connector) as session:
                    tasks = [fetch_and_process_image(session, sku, download_folder) for sku in sku_list]
                    processed_count = 0
                    for f in asyncio.as_completed(tasks):
                        await f
                        processed_count += 1
                        progress_bar.progress(processed_count / total_count)
                progress_bar.progress(1.0)


            with st.spinner("Processing images, please wait..."):
                with tempfile.TemporaryDirectory() as download_folder:
                    asyncio.run(run_processing(download_folder))

                    zip_path_ch = None
                    if any(os.scandir(download_folder)):
                         with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip_file:
                            zip_path_ch = tmp_zip_file.name
                         shutil.make_archive(zip_path_ch[:-4], 'zip', download_folder)
                         st.session_state["renaming_zip_path_ch"] = zip_path_ch
                    else:
                         st.session_state["renaming_zip_path_ch"] = None


                    error_path_ch = None
                    if error_codes:
                        error_df = pd.DataFrame(sorted(list(set(error_codes))), columns=["sku"])
                        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="", encoding="utf-8-sig") as tmp_error_file:
                            error_df.to_csv(tmp_error_file, index=False, sep=';')
                            error_path_ch = tmp_error_file.name
                        st.session_state["renaming_error_path_ch"] = error_path_ch
                    else:
                        st.session_state["renaming_error_path_ch"] = None

            st.session_state["renaming_processing_done_ch"] = True
            st.session_state.renaming_start_processing_ch = False


    if st.session_state.get("renaming_processing_done_ch", False):
        # ... (codice download Svizzera invariato) ...
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            zip_path_dl = st.session_state.get("renaming_zip_path_ch")
            if zip_path_dl and os.path.exists(zip_path_dl):
                with open(zip_path_dl, "rb") as f:
                    st.download_button(
                        label="Download Images",
                        data=f,
                        file_name=f"switzerland_images_{st.session_state.renaming_session_id[:6]}.zip",
                        mime="application/zip",
                        key="dl_ch_zip"
                    )
            else:
                 st.info("No images processed.")
        with col2:
            error_path_dl = st.session_state.get("renaming_error_path_ch")
            if error_path_dl and os.path.exists(error_path_dl):
                with open(error_path_dl, "rb") as f_error:
                    st.download_button(
                        label="Download Missing Image List",
                        data=f_error,
                        file_name=f"errors_switzerland_{st.session_state.renaming_session_id[:6]}.csv",
                        mime="text/csv",
                        key="dl_ch_err"
                    )
            else:
                st.info("No errors found.")


# ======================================================
# SECTION: Farmadati
# ======================================================
elif server_country == "Farmadati":
    # ... (Codice sezione Farmadati invariato, incluso il bottone Reset e la funzione get_farmadati_mapping) ...
    st.header("Farmadati Server Image Processing")
    st.markdown("""
    :information_source: **How to use:**

    - :arrow_right: **Create a list of products:** Rename the column **sku** or use the Quick Report in Akeneo.
    - :arrow_right: **In Akeneo, select the following options:**
        - **File Type:** CSV or Excel
        - **All Attributes or Grid Context:** (for Grid Context, select ID)
        - **With Codes**
        - **Without Media**
    """)

    # --- Bottone Reset SPOSTATO QUI ---
    if st.button("🧹 Clear Cache and Reset Data"):
        keys_to_remove = [k for k in st.session_state.keys() if k.startswith("renaming_") or k in ["uploader_key", "session_id", "processing_done", "zip_path", "error_path", "farmadati_zip", "farmadati_errors", "farmadati_ready", "process_images_switzerland", "process_images_farmadati"]]
        # Clear the cached Farmadati mapping if the function exists and has clear method
        if 'get_farmadati_mapping' in globals() and hasattr(get_farmadati_mapping, 'clear'):
            get_farmadati_mapping.clear()
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.renaming_uploader_key = str(uuid.uuid4())
        st.info("Cache cleared. Please re-upload your file.")
        # NOTA: time.sleep(1) è stato rimosso perché 'time' non è importato nel codice fornito
        st.rerun()

    manual_input_fd = st.text_area("Or paste your SKUs here (one per line):", key="manual_input_farmadati")
    farmadati_file = st.file_uploader("Upload file (column 'sku')", type=["xlsx", "csv"], key=st.session_state.renaming_uploader_key)

    if st.button("Search Images", key="process_farmadati"):
         st.session_state.renaming_start_processing_fd = True
         st.session_state.renaming_processing_done_fd = False
         if "renaming_zip_buffer_fd" in st.session_state: del st.session_state.renaming_zip_buffer_fd
         if "renaming_error_data_fd" in st.session_state: del st.session_state.renaming_error_data_fd


    if st.session_state.get("renaming_start_processing_fd") and not st.session_state.get("renaming_processing_done_fd", False):
        sku_list_fd = get_sku_list(farmadati_file, manual_input_fd)
        if not sku_list_fd:
            st.warning("Please upload a file or paste some SKUs to process.")
            st.session_state.renaming_start_processing_fd = False
        else:
            st.info(f"Processing {len(sku_list_fd)} SKUs for Farmadati...")

            USERNAME = "BDF250621d" # Consider using st.secrets for credentials
            PASSWORD = "wTP1tvSZ" # Consider using st.secrets for credentials
            WSDL_URL = 'http://webservices.farmadati.it/WS2/FarmadatiItaliaWebServicesM2.svc?wsdl'
            DATASET_CODE = "TDZ"

            @st.cache_resource(ttl=3600, show_spinner=False)
            def get_farmadati_mapping(_username, _password):
                # st.info(f"Fetching Farmadati dataset '{DATASET_CODE}'...") # COMMENTATO
                history = HistoryPlugin()
                transport = Transport(cache=InMemoryCache(), timeout=180)
                settings = Settings(strict=False, xml_huge_tree=True)
                try:
                    client = Client(wsdl=WSDL_URL, wsse=UsernameToken(_username, _password), transport=transport, plugins=[history], settings=settings)
                    response = client.service.GetDataSet(_username, _password, DATASET_CODE, "GETRECORDS", 1)
                except Exception as e:
                    st.error(f"Farmadati Connection/Fetch Error: {e}")
                    st.stop()

                if response.CodEsito != "OK" or response.ByteListFile is None:
                    st.error(f"Farmadati API Error: {response.CodEsito} - {response.DescEsito}")
                    st.stop()

                # st.info("Parsing Farmadati XML mapping...") # COMMENTATO
                code_to_image = {}
                try:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        zip_path_fd = os.path.join(tmp_dir, f"{DATASET_CODE}.zip")
                        with open(zip_path_fd, "wb") as f: f.write(response.ByteListFile)
                        with zipfile.ZipFile(zip_path_fd, 'r') as z:
                            xml_file = next((name for name in z.namelist() if name.upper().endswith('.XML')), None)
                            if not xml_file: raise FileNotFoundError("XML not in ZIP")
                            z.extract(xml_file, tmp_dir)
                            xml_full_path = os.path.join(tmp_dir, xml_file)

                        # Efficient XML parsing for large files
                        context = ET.iterparse(xml_full_path, events=('end',))
                        for _, elem in context:
                             if elem.tag == 'RECORD':
                                t218 = elem.find('FDI_T218')
                                t438 = elem.find('FDI_T438')
                                if t218 is not None and t438 is not None and t218.text and t438.text:
                                    aic = t218.text.strip().lstrip("0")
                                    if aic: code_to_image[aic] = t438.text.strip()
                                # Clear processed elements to free memory
                                elem.clear()
                                while elem.getprevious() is not None:
                                    del elem.getparent()[0]
                        del context

                    # st.success(f"Farmadati mapping loaded ({len(code_to_image)} codes).") # COMMENTATO
                    return code_to_image
                except Exception as e:
                    st.error(f"Error parsing Farmadati XML: {e}")
                    st.stop()

            def process_image_fd(img_bytes):
                try:
                    img = Image.open(BytesIO(img_bytes))
                    if img.mode != 'L': gray = img.convert("L")
                    else: gray = img
                    extrema = gray.getextrema()
                    if extrema == (0, 0) or extrema == (255, 255): raise ValueError("Empty image")

                    img = ImageOps.exif_transpose(img)
                    bg_white = Image.new(img.mode, img.size, (255, 255, 255))
                    diff = ImageChops.difference(img, bg_white)
                    bbox = diff.getbbox()
                    if bbox: img = img.crop(bbox)
                    if img.width == 0 or img.height == 0: raise ValueError("Empty after trim")

                    # Farmadati specific cropping/padding
                    if img.width > 1000:
                        left = (img.width - 1000) // 2
                        img = img.crop((left, 0, left + 1000, img.height))
                    if img.height > 1000:
                        top = (img.height - 1000) // 2
                        img = img.crop((0, top, img.width, top + 1000))
                    if img.width < 1000 or img.height < 1000:
                        # Ensure RGB before pasting on white canvas
                        if img.mode != "RGB": img = img.convert("RGB")
                        canvas = Image.new("RGB", (1000, 1000), "white")
                        left = (1000 - img.width) // 2
                        top = (1000 - img.height) // 2
                        canvas.paste(img, (left, top))
                        final_img = canvas
                    else:
                        final_img = img

                    buffer = BytesIO()
                    # Ensure RGB before saving as JPEG
                    if final_img.mode != "RGB": final_img = final_img.convert("RGB")
                    final_img.save(buffer, "JPEG", quality=95)
                    buffer.seek(0)
                    return buffer
                except Exception as e:
                     raise RuntimeError(f"Processing failed: {e}")

            try:
                with st.spinner("Loading Farmadati mapping (this may take a minute)..."):
                    aic_to_image = get_farmadati_mapping(USERNAME, PASSWORD)

                if not aic_to_image:
                     st.error("Farmadati mapping failed.")
                     st.session_state.renaming_start_processing_fd = False
                else:
                    total_fd = len(sku_list_fd)
                    progress_bar_fd = st.progress(0, text="Starting Farmadati processing...")
                    error_list_fd = []
                    processed_files_count = 0
                    zip_buffer = BytesIO()

                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                         with requests.Session() as http_session: # Use session for potential keep-alive
                            for i, sku in enumerate(sku_list_fd):
                                progress_bar_fd.progress((i+1)/total_fd, text=f"Processing {sku} ({i+1}/{total_fd})")
                                clean_sku = str(sku).strip()
                                if clean_sku.upper().startswith("IT"): clean_sku = clean_sku[2:]
                                clean_sku = clean_sku.lstrip("0")

                                if not clean_sku:
                                    error_list_fd.append((sku, "Invalid AIC"))
                                    continue

                                image_name = aic_to_image.get(clean_sku)
                                if not image_name:
                                    error_list_fd.append((sku, "AIC not in mapping"))
                                    continue

                                from urllib.parse import quote
                                image_url = f"https://ws.farmadati.it/WS_DOC/GetDoc.aspx?accesskey={PASSWORD}&tipodoc=Z&nomefile={quote(image_name)}"

                                try:
                                    r = http_session.get(image_url, timeout=45) # Increased timeout
                                    r.raise_for_status() # Check for HTTP errors
                                    if not r.content:
                                         error_list_fd.append((sku, "Empty download"))
                                         continue

                                    processed_buffer = process_image_fd(r.content)
                                    zipf.writestr(f"{sku}-h1.jpg", processed_buffer.read())
                                    processed_files_count += 1

                                except requests.exceptions.RequestException as req_e:
                                     reason = f"Network Error: {req_e}"
                                     if req_e.response is not None: reason = f"HTTP {req_e.response.status_code}"
                                     error_list_fd.append((sku, reason))
                                except RuntimeError as proc_e: # Catch processing errors
                                     error_list_fd.append((sku, f"Processing Error: {proc_e}"))
                                except Exception as e: # Catch other unexpected errors
                                     error_list_fd.append((sku, f"Unexpected Error: {e}"))


                    progress_bar_fd.progress(1.0, text="Farmadati processing complete!")

                    if processed_files_count > 0:
                        zip_buffer.seek(0)
                        st.session_state["renaming_zip_buffer_fd"] = zip_buffer
                    else:
                        st.session_state["renaming_zip_buffer_fd"] = None

                    if error_list_fd:
                        error_df = pd.DataFrame(error_list_fd, columns=["SKU", "Reason"])
                        error_df = error_df.drop_duplicates().sort_values(by="SKU")
                        csv_error = error_df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
                        st.session_state["renaming_error_data_fd"] = csv_error
                    else:
                        st.session_state["renaming_error_data_fd"] = None

            except Exception as critical_e:
                 st.error(f"Critical Error during Farmadati processing: {critical_e}")

            st.session_state["renaming_processing_done_fd"] = True
            st.session_state.renaming_start_processing_fd = False


    if st.session_state.get("renaming_processing_done_fd"):
        # ... (codice download Farmadati invariato) ...
        st.markdown("---")
        col1_fd_dl, col2_fd_dl = st.columns(2)
        with col1_fd_dl:
            zip_data = st.session_state.get("renaming_zip_buffer_fd")
            if zip_data:
                st.download_button(
                    "Download Images (ZIP)",
                    data=zip_data,
                    file_name=f"farmadati_images_{st.session_state.renaming_session_id[:6]}.zip",
                    mime="application/zip",
                    key="dl_fd_zip"
                )
            else:
                 st.info("No images processed.")
        with col2_fd_dl:
            error_data = st.session_state.get("renaming_error_data_fd")
            if error_data:
                st.download_button(
                    "Download Error List",
                    data=error_data,
                    file_name=f"errors_farmadati_{st.session_state.renaming_session_id[:6]}.csv",
                    mime="text/csv",
                    key="dl_fd_err"
                )
            else:
                st.info("No errors found.")


# ======================================================
# SECTION: coming soon (Originale)
# ======================================================
elif server_country == "coming soon":
    st.header("coming soon")
    st.info("This section is under development.")
