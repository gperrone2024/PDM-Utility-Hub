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
import xml.etree.ElementTree as ET # Usiamo la libreria standard
import requests
from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
from zeep.cache import InMemoryCache
from zeep.plugins import HistoryPlugin
import time # Import aggiunto nella correzione precedente

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
    sku_list = []
    df_file = None
    if uploaded_file_obj is not None:
        try:
            # Ensure file pointer is at the beginning
            uploaded_file_obj.seek(0)
            if uploaded_file_obj.name.lower().endswith("csv"):
                # Read a sample to sniff delimiter
                sample = uploaded_file_obj.read(1024).decode("utf-8", errors='ignore')
                uploaded_file_obj.seek(0) # Reset pointer again after reading sample
                delimiter = ';' # Default delimiter
                try:
                    # Sniff the delimiter from the sample
                    dialect = csv.Sniffer().sniff(sample, delimiters=';,\t|') # Add more potential delimiters if needed
                    delimiter = dialect.delimiter
                    # st.info(f"Detected delimiter: '{delimiter}'") # Optional: Inform user
                except csv.Error:
                    # If sniffing fails, stick to the default and inform the user
                    # st.warning("Could not automatically detect delimiter, using ';'. Ensure your CSV uses this delimiter.")
                    pass # Use default ';'

                # Read the full CSV with the detected or default delimiter
                df_file = pd.read_csv(uploaded_file_obj, delimiter=delimiter, dtype=str, keep_default_na=False)
            elif uploaded_file_obj.name.lower().endswith(("xlsx", "xls")):
                df_file = pd.read_excel(uploaded_file_obj, dtype=str, keep_default_na=False)
            else:
                st.error("Unsupported file type. Please upload a CSV or Excel file.")
                return [], None # Return empty list and None for df

            # Find the 'sku' column (case-insensitive)
            sku_column = None
            for col in df_file.columns:
                if str(col).strip().lower() == "sku":
                    sku_column = col
                    break

            if sku_column:
                # Extract SKUs, convert to string, strip whitespace, and filter out empty strings
                file_skus = df_file[sku_column].astype(str).str.strip()
                sku_list.extend(file_skus[file_skus != ''].tolist())
            else:
                 st.warning("Column 'sku' not found in the uploaded file. Please ensure the column exists and is named 'sku'.")

        except Exception as e:
            st.error(f"Error reading file: {e}")
            return [], None # Return empty list on error

    # Process manual input
    if manual_text:
        manual_skus = [line.strip() for line in manual_text.splitlines() if line.strip()]
        sku_list.extend(manual_skus)

    # Remove duplicates while preserving order and filter out any remaining empty/falsy values
    unique_sku_list = list(dict.fromkeys(sku for sku in sku_list if sku))
    # st.info(f"Found {len(unique_sku_list)} unique SKUs.") # Optional feedback
    return unique_sku_list


# ======================================================
# SECTION: Switzerland
# ======================================================
if server_country == "Switzerland":
    st.header("Switzerland Server Image Processing")
    st.markdown("""
    :information_source: **How to use:**

    - :arrow_right: **Prepare your list:** Upload an Excel or CSV file with a column named `sku`, or paste SKUs directly into the text area below (one SKU per line).
    - :arrow_right: **Akeneo Quick Export (Optional):**
        - **File Type:** CSV or Excel
        - **Attributes:** Include at least the `sku` attribute (or Identifier).
        - **Options:** Use 'Codes', 'Without Media'.
    - :arrow_right: Click **Search Images**.
    - :arrow_right: Download the results (ZIP file with images, CSV with errors).
    - :warning: Click **Clear Cache and Reset Data** before starting a new search with different inputs.
    """)
    st.markdown("---") # Separator

    # --- Bottone Reset SPOSTATO QUI ---
    if st.button("🧹 Clear Cache and Reset Data", key="reset_ch"):
        # Clear specific session state keys related to Switzerland processing
        keys_to_remove = [
            "renaming_uploader_key", "renaming_session_id",
            "manual_input_switzerland", "process_switzerland",
            "renaming_start_processing_ch", "renaming_processing_done_ch",
            "renaming_zip_path_ch", "renaming_error_path_ch"
        ]
        # Also clear general keys if they exist from other sections
        keys_to_remove.extend([
            "manual_input_farmadati", "process_farmadati",
            "renaming_start_processing_fd", "renaming_processing_done_fd",
            "renaming_zip_buffer_fd", "renaming_error_data_fd"
        ])

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        # Reset the uploader key to force re-render
        st.session_state.renaming_uploader_key = str(uuid.uuid4())
        # Generate a new session ID for the next run
        st.session_state.renaming_session_id = str(uuid.uuid4())

        st.success("Cache and session data cleared. Ready for a new task.")
        time.sleep(1) # Short pause before rerun
        st.rerun()

    # Input Methods
    uploaded_file = st.file_uploader("Upload file (Excel or CSV with 'sku' column)", type=["xlsx", "csv"], key=st.session_state.renaming_uploader_key)
    manual_input = st.text_area("Or paste your SKUs here (one per line):", key="manual_input_switzerland", height=150)

    # Process Button
    if st.button("Search Images", key="process_switzerland", use_container_width=True):
        # Reset state for this run
        st.session_state.renaming_start_processing_ch = True
        st.session_state.renaming_processing_done_ch = False
        if "renaming_zip_path_ch" in st.session_state: del st.session_state.renaming_zip_path_ch
        if "renaming_error_path_ch" in st.session_state: del st.session_state.renaming_error_path_ch


    # Processing Logic Trigger
    if st.session_state.get("renaming_start_processing_ch") and not st.session_state.get("renaming_processing_done_ch", False):
        sku_list = get_sku_list(uploaded_file, manual_input)
        if not sku_list:
            st.warning("Please upload a file or paste some SKUs to process.")
            st.session_state.renaming_start_processing_ch = False # Stop processing if no SKUs
        else:
            st.info(f"Processing {len(sku_list)} SKUs for Switzerland...")
            error_codes = [] # List to store SKUs that failed
            total_count = len(sku_list)
            progress_bar = st.progress(0, text="Initializing...")

            # --- Helper Functions for Switzerland ---
            def get_image_url(product_code):
                """Constructs the Documedis image URL from a product code (Pharmacode/SKU)."""
                pharmacode = str(product_code).strip()
                # Remove 'CH' prefix and leading zeros if present
                if pharmacode.upper().startswith("CH"):
                    pharmacode = pharmacode[2:].lstrip("0")
                else:
                    pharmacode = pharmacode.lstrip("0")
                # Return None if the resulting pharmacode is empty
                if not pharmacode: return None
                # Construct the URL
                return f"https://documedis.hcisolutions.ch/2020-01/api/products/image/PICFRONT3D/Pharmacode/{pharmacode}/F"

            def process_and_save(original_sku, content, download_folder):
                """Processes downloaded image content and saves it."""
                try:
                    img = Image.open(BytesIO(content))

                    # Check for completely black or white images (often indicate errors)
                    if img.mode != 'L': gray = img.convert("L")
                    else: gray = img
                    extrema = gray.getextrema()
                    if extrema == (0, 0): raise ValueError("Empty image (all black)")
                    if extrema == (255, 255): raise ValueError("Empty image (all white)")

                    # Handle image orientation based on EXIF data
                    img = ImageOps.exif_transpose(img)

                    # Trim whitespace (using white background as reference)
                    bg = Image.new(img.mode, img.size, (255, 255, 255))
                    diff = ImageChops.difference(img, bg)
                    bbox = diff.getbbox()
                    if bbox: img = img.crop(bbox)

                    # Check if image is empty after trimming
                    if img.width == 0 or img.height == 0: raise ValueError("Image became empty after trimming whitespace")

                    # Resize while maintaining aspect ratio to fit within 1000x1000
                    img.thumbnail((1000, 1000), Image.LANCZOS)

                    # Create a 1000x1000 white canvas
                    canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))

                    # Calculate position to paste the resized image centered on the canvas
                    offset_x = (1000 - img.width) // 2
                    offset_y = (1000 - img.height) // 2
                    canvas.paste(img, (offset_x, offset_y))

                    # Define the new filename with -h1 suffix
                    new_filename = f"{original_sku}-h1.jpg"
                    img_path = os.path.join(download_folder, new_filename)

                    # Save the final image as JPEG
                    canvas.save(img_path, "JPEG", quality=95) # Quality 95 is a good balance
                    return True # Indicate success
                except UnidentifiedImageError:
                    # Handle cases where the downloaded content is not a valid image
                    st.warning(f"SKU {original_sku}: Downloaded content is not a valid image.")
                    return False
                except ValueError as ve:
                    # Handle specific value errors like empty images
                    st.warning(f"SKU {original_sku}: Image processing error - {ve}")
                    return False
                except Exception as e:
                    # Catch other potential errors during processing
                    st.warning(f"SKU {original_sku}: Unexpected error during image processing - {e}")
                    return False

            async def fetch_and_process_image(session, product_code, download_folder):
                """Fetches an image URL and processes it."""
                image_url = get_image_url(product_code)
                if image_url is None:
                    st.warning(f"Invalid SKU format for Switzerland: {product_code}")
                    error_codes.append(product_code)
                    return # Skip processing for invalid SKUs

                try:
                    # Make async GET request
                    async with session.get(image_url, timeout=30) as response:
                        if response.status == 200:
                            content = await response.read()
                            if not content:
                                # Handle empty response content
                                st.warning(f"SKU {product_code}: Received empty content from server.")
                                error_codes.append(product_code)
                                return

                            # Run the synchronous processing function in a separate thread
                            success = await asyncio.to_thread(process_and_save, product_code, content, download_folder)
                            if not success:
                                error_codes.append(product_code)
                        elif response.status == 404:
                             # Handle 'Not Found' specifically
                             # st.warning(f"SKU {product_code}: Image not found on server (404).") # Optional: less verbose
                             error_codes.append(product_code)
                        else:
                            # Handle other non-200 status codes
                            st.warning(f"SKU {product_code}: Failed to download image (Status: {response.status})")
                            error_codes.append(product_code)
                except asyncio.TimeoutError:
                     st.warning(f"SKU {product_code}: Download timed out.")
                     error_codes.append(product_code)
                except aiohttp.ClientError as ce:
                     st.warning(f"SKU {product_code}: Network/Client error during download - {ce}")
                     error_codes.append(product_code)
                except Exception as e:
                    # Catch unexpected errors during download/processing call
                    st.warning(f"SKU {product_code}: Unexpected error during download/processing - {e}")
                    error_codes.append(product_code)

            async def run_processing(download_folder):
                """Runs the asynchronous fetching and processing for all SKUs."""
                connector = aiohttp.TCPConnector(limit=50) # Adjust concurrency limit as needed
                async with aiohttp.ClientSession(connector=connector) as session:
                    tasks = [fetch_and_process_image(session, sku, download_folder) for sku in sku_list]
                    processed_count = 0
                    for f in asyncio.as_completed(tasks):
                        await f # Wait for task completion (and handle potential exceptions)
                        processed_count += 1
                        # Update progress bar
                        progress_text = f"Processed {processed_count}/{total_count} SKUs..."
                        progress_bar.progress(processed_count / total_count, text=progress_text)
                progress_bar.progress(1.0, text="Processing complete!") # Final update

            # --- Execute Processing ---
            with st.spinner("Processing images, please wait... This might take a while depending on the number of SKUs."):
                # Use a temporary directory for downloads
                with tempfile.TemporaryDirectory() as download_folder:
                    # Run the main async processing function
                    asyncio.run(run_processing(download_folder))

                    # --- Create ZIP file ---
                    zip_path_ch = None
                    # Check if any files were actually downloaded and saved
                    if any(os.scandir(download_folder)):
                         # Create a temporary file path for the zip archive
                         with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip_file:
                            zip_path_ch = tmp_zip_file.name
                         # Create the zip archive from the download folder contents
                         try:
                             shutil.make_archive(zip_path_ch[:-4], 'zip', download_folder) # base_name excludes .zip
                             st.session_state["renaming_zip_path_ch"] = zip_path_ch
                         except Exception as zip_e:
                              st.error(f"Failed to create ZIP file: {zip_e}")
                              st.session_state["renaming_zip_path_ch"] = None
                              if zip_path_ch and os.path.exists(zip_path_ch): os.remove(zip_path_ch) # Clean up temp file if zip failed
                    else:
                         st.session_state["renaming_zip_path_ch"] = None # No files downloaded

                    # --- Create Error CSV file ---
                    error_path_ch = None
                    if error_codes:
                        # Create DataFrame from unique error codes
                        error_df = pd.DataFrame(sorted(list(set(error_codes))), columns=["sku"])
                        # Create a temporary file path for the error CSV
                        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="", encoding="utf-8-sig") as tmp_error_file:
                            try:
                                error_df.to_csv(tmp_error_file, index=False, sep=';')
                                error_path_ch = tmp_error_file.name
                                st.session_state["renaming_error_path_ch"] = error_path_ch
                            except Exception as csv_e:
                                 st.error(f"Failed to create error CSV file: {csv_e}")
                                 st.session_state["renaming_error_path_ch"] = None
                                 if error_path_ch and os.path.exists(error_path_ch): os.remove(error_path_ch) # Clean up temp file
                    else:
                        st.session_state["renaming_error_path_ch"] = None # No errors

            # Mark processing as done and stop the trigger
            st.session_state["renaming_processing_done_ch"] = True
            st.session_state.renaming_start_processing_ch = False
            st.rerun() # Rerun to show download buttons immediately


    # --- Download Buttons Section (Switzerland) ---
    if st.session_state.get("renaming_processing_done_ch", False):
        st.markdown("---")
        st.subheader("Download Results (Switzerland)")
        col1, col2 = st.columns(2)

        # Download Images Button
        with col1:
            zip_path_dl = st.session_state.get("renaming_zip_path_ch")
            if zip_path_dl and os.path.exists(zip_path_dl):
                try:
                    with open(zip_path_dl, "rb") as f:
                        st.download_button(
                            label="Download Images (ZIP)",
                            data=f,
                            file_name=f"switzerland_images_{st.session_state.renaming_session_id[:6]}.zip",
                            mime="application/zip",
                            key="dl_ch_zip",
                            use_container_width=True
                        )
                except FileNotFoundError:
                    st.error("Error: ZIP file not found. Please try processing again.")
                except Exception as e:
                    st.error(f"Error reading ZIP file: {e}")
            else:
                 st.info("No images were successfully processed and saved.")

        # Download Error List Button
        with col2:
            error_path_dl = st.session_state.get("renaming_error_path_ch")
            if error_path_dl and os.path.exists(error_path_dl):
                try:
                    with open(error_path_dl, "rb") as f_error:
                        st.download_button(
                            label="Download Missing/Error List (CSV)",
                            data=f_error,
                            file_name=f"errors_switzerland_{st.session_state.renaming_session_id[:6]}.csv",
                            mime="text/csv",
                            key="dl_ch_err",
                            use_container_width=True
                        )
                except FileNotFoundError:
                     st.error("Error: Error CSV file not found. Please try processing again.")
                except Exception as e:
                    st.error(f"Error reading error CSV file: {e}")
            else:
                st.success("No errors reported during processing.")


# ======================================================
# SECTION: Farmadati
# ======================================================
elif server_country == "Farmadati":
    st.header("Farmadati Server Image Processing")
    st.markdown("""
    :information_source: **How to use:**

    - :arrow_right: **Prepare your list:** Upload an Excel or CSV file with a column named `sku` (containing Italian AIC codes, with or without 'IT' prefix), or paste AICs directly into the text area below (one AIC per line).
    - :arrow_right: **Akeneo Quick Export (Optional):**
        - **File Type:** CSV or Excel
        - **Attributes:** Include at least the `sku` attribute (or Identifier).
        - **Options:** Use 'Codes', 'Without Media'.
    - :arrow_right: Click **Search Images**. This involves fetching a mapping file first, which might take a minute.
    - :arrow_right: Download the results (ZIP file with images, CSV with errors).
    - :warning: Click **Clear Cache and Reset Data** before starting a new search with different inputs.
    """)
    st.markdown("---") # Separator

    # --- Bottone Reset SPOSTATO QUI ---
    if st.button("🧹 Clear Cache and Reset Data", key="reset_fd"):
        # Clear specific session state keys related to Farmadati processing
        keys_to_remove = [
            "renaming_uploader_key", "renaming_session_id",
            "manual_input_farmadati", "process_farmadati",
            "renaming_start_processing_fd", "renaming_processing_done_fd",
            "renaming_zip_buffer_fd", "renaming_error_data_fd"
        ]
         # Also clear general keys if they exist from other sections
        keys_to_remove.extend([
            "manual_input_switzerland", "process_switzerland",
            "renaming_start_processing_ch", "renaming_processing_done_ch",
            "renaming_zip_path_ch", "renaming_error_path_ch"
        ])
        # Clear the cached Farmadati mapping if the function exists
        if 'get_farmadati_mapping' in globals() and hasattr(get_farmadati_mapping, 'clear'):
            get_farmadati_mapping.clear()


        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        # Reset the uploader key to force re-render
        st.session_state.renaming_uploader_key = str(uuid.uuid4())
         # Generate a new session ID for the next run
        st.session_state.renaming_session_id = str(uuid.uuid4())

        st.success("Cache and session data cleared. Ready for a new task.")
        time.sleep(1) # Short pause before rerun
        st.rerun()

    # Input Methods
    farmadati_file = st.file_uploader("Upload file (Excel or CSV with 'sku' column)", type=["xlsx", "csv"], key=st.session_state.renaming_uploader_key)
    manual_input_fd = st.text_area("Or paste your SKUs (AIC codes) here (one per line):", key="manual_input_farmadati", height=150)

    # Process Button
    if st.button("Search Images", key="process_farmadati", use_container_width=True):
         # Reset state for this run
         st.session_state.renaming_start_processing_fd = True
         st.session_state.renaming_processing_done_fd = False
         if "renaming_zip_buffer_fd" in st.session_state: del st.session_state.renaming_zip_buffer_fd
         if "renaming_error_data_fd" in st.session_state: del st.session_state.renaming_error_data_fd


    # Processing Logic Trigger
    if st.session_state.get("renaming_start_processing_fd") and not st.session_state.get("renaming_processing_done_fd", False):
        sku_list_fd = get_sku_list(farmadati_file, manual_input_fd)
        if not sku_list_fd:
            st.warning("Please upload a file or paste some SKUs (AIC codes) to process.")
            st.session_state.renaming_start_processing_fd = False # Stop processing if no SKUs
        else:
            st.info(f"Processing {len(sku_list_fd)} SKUs for Farmadati...")

            # --- Farmadati Constants and Helper Functions ---
            # Credentials should ideally be stored securely (e.g., Streamlit secrets)
            USERNAME = st.secrets.get("FARMADATI_USER", "BDF250621d") # Fallback to default if not in secrets
            PASSWORD = st.secrets.get("FARMADATI_PASS", "wTP1tvSZ") # Fallback to default if not in secrets
            WSDL_URL = 'http://webservices.farmadati.it/WS2/FarmadatiItaliaWebServicesM2.svc?wsdl'
            DATASET_CODE = "TDZ" # Dataset containing AIC to image filename mapping

            @st.cache_resource(ttl=3600, show_spinner="Fetching Farmadati mapping...")
            def get_farmadati_mapping(_username, _password):
                """Fetches and parses the Farmadati dataset to create an AIC-to-image filename map."""
                # st.info(f"Fetching Farmadati dataset '{DATASET_CODE}'...") # Less verbose
                history = HistoryPlugin()
                transport = Transport(cache=InMemoryCache(), timeout=180) # Increased timeout
                settings = Settings(strict=False, xml_huge_tree=True) # Allow large XML
                try:
                    # Initialize SOAP client
                    client = Client(wsdl=WSDL_URL, wsse=UsernameToken(_username, _password), transport=transport, plugins=[history], settings=settings)
                    # Call the GetDataSet service method
                    response = client.service.GetDataSet(_username, _password, DATASET_CODE, "GETRECORDS", 1) # 1 = Full dataset
                except Exception as e:
                    st.error(f"Farmadati Connection/Fetch Error: {e}")
                    # Consider logging the full traceback for debugging
                    # st.exception(e)
                    # Stop execution if connection fails
                    st.stop() # Use st.stop() to halt execution in callbacks/scripts

                # Check API response status
                if response.CodEsito != "OK" or response.ByteListFile is None:
                    st.error(f"Farmadati API Error: {response.CodEsito} - {response.DescEsito}")
                    st.stop()

                # st.info("Parsing Farmadati XML mapping...") # Less verbose
                code_to_image = {}
                try:
                    # Process the downloaded ZIP file containing the XML
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        zip_path_fd = os.path.join(tmp_dir, f"{DATASET_CODE}.zip")
                        # Write the byte content to a temporary zip file
                        with open(zip_path_fd, "wb") as f: f.write(response.ByteListFile)

                        # Extract the XML file from the zip
                        with zipfile.ZipFile(zip_path_fd, 'r') as z:
                            # Find the XML file within the zip (case-insensitive)
                            xml_file = next((name for name in z.namelist() if name.lower().endswith('.xml')), None)
                            if not xml_file: raise FileNotFoundError("XML file not found within the downloaded Farmadati ZIP.")
                            z.extract(xml_file, tmp_dir)
                            xml_full_path = os.path.join(tmp_dir, xml_file)

                        # Parse the large XML file efficiently using iterparse
                        context = ET.iterparse(xml_full_path, events=('end',))
                        for event, elem in context:
                            if elem.tag == 'RECORD':
                                t218_elem = elem.find('FDI_T218') # AIC Code
                                t438_elem = elem.find('FDI_T438') # Image Filename

                                if t218_elem is not None and t438_elem is not None and t218_elem.text and t438_elem.text:
                                    aic = t218_elem.text.strip().lstrip("0")
                                    image_filename = t438_elem.text.strip()
                                    if aic and image_filename:
                                        code_to_image[aic] = image_filename

                                # *** CORREZIONE ERRORE XML ***
                                # Clear the element per liberare memoria DOPO averlo processato.
                                # Rimuovere il ciclo while che usava il metodo inesistente getprevious().
                                elem.clear()
                                # *** FINE CORREZIONE ***

                        # del context # Non necessario eliminare il contesto qui

                    # st.success(f"Farmadati mapping loaded ({len(code_to_image)} codes).") # Less verbose
                    return code_to_image
                except Exception as e:
                    st.error(f"Error parsing Farmadati XML: {e}")
                    # st.exception(e)
                    st.stop()

            def process_image_fd(img_bytes):
                """Processes downloaded Farmadati image bytes."""
                try:
                    img = Image.open(BytesIO(img_bytes))

                    # Check for empty images (all black or all white)
                    if img.mode != 'L': gray = img.convert("L")
                    else: gray = img
                    extrema = gray.getextrema()
                    if extrema == (0, 0) or extrema == (255, 255): raise ValueError("Empty image (all black or white)")

                    # Handle EXIF orientation
                    img = ImageOps.exif_transpose(img)

                    # Trim whitespace (assuming white background)
                    bg_white = Image.new(img.mode, img.size, (255, 255, 255))
                    diff = ImageChops.difference(img, bg_white)
                    bbox = diff.getbbox()
                    if bbox: img = img.crop(bbox)
                    if img.width == 0 or img.height == 0: raise ValueError("Image became empty after trimming")

                    # Farmadati specific cropping/padding logic (adjust if needed)
                    # Crop to 1000px if wider/taller
                    if img.width > 1000:
                        left = (img.width - 1000) // 2
                        img = img.crop((left, 0, left + 1000, img.height))
                    if img.height > 1000:
                        top = (img.height - 1000) // 2
                        img = img.crop((0, top, img.width, top + 1000))

                    # Pad to 1000x1000 if smaller
                    if img.width < 1000 or img.height < 1000:
                        # Ensure image is RGB before pasting onto RGB canvas
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        canvas = Image.new("RGB", (1000, 1000), "white")
                        left = (1000 - img.width) // 2
                        top = (1000 - img.height) // 2
                        canvas.paste(img, (left, top))
                        final_img = canvas
                    else:
                        final_img = img # Already 1000x1000 or less after cropping

                    # Save processed image to a buffer as JPEG
                    buffer = BytesIO()
                    # Ensure final image is RGB before saving as JPEG
                    if final_img.mode != "RGB":
                         final_img = final_img.convert("RGB")
                    final_img.save(buffer, "JPEG", quality=95)
                    buffer.seek(0)
                    return buffer
                except UnidentifiedImageError:
                    raise RuntimeError("Downloaded content is not a valid image.")
                except ValueError as ve:
                    raise RuntimeError(f"Processing failed: {ve}")
                except Exception as e:
                     raise RuntimeError(f"Unexpected processing error: {e}")

            # --- Execute Processing (Farmadati) ---
            try:
                # Get the mapping (uses cache if available)
                aic_to_image = get_farmadati_mapping(USERNAME, PASSWORD)

                if not aic_to_image:
                     st.error("Failed to load Farmadati mapping. Cannot proceed.")
                     st.session_state.renaming_start_processing_fd = False # Stop processing
                else:
                    total_fd = len(sku_list_fd)
                    progress_bar_fd = st.progress(0, text="Starting Farmadati image download...")
                    error_list_fd = [] # List to store tuples of (sku, reason)
                    processed_files_count = 0
                    zip_buffer = BytesIO() # In-memory buffer for the ZIP file

                    with st.spinner(f"Downloading and processing {total_fd} Farmadati images..."):
                        # Use a context manager for the ZIP file buffer
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                             # Use a persistent requests session for potential connection reuse
                             with requests.Session() as http_session:
                                for i, sku in enumerate(sku_list_fd):
                                    # Update progress bar for each SKU
                                    progress_text_fd = f"Processing {sku} ({i+1}/{total_fd})"
                                    progress_bar_fd.progress((i+1)/total_fd, text=progress_text_fd)

                                    # Clean the SKU (AIC code)
                                    clean_sku = str(sku).strip()
                                    if clean_sku.upper().startswith("IT"): clean_sku = clean_sku[2:]
                                    clean_sku = clean_sku.lstrip("0")

                                    if not clean_sku:
                                        error_list_fd.append((sku, "Invalid AIC format"))
                                        continue # Skip to next SKU

                                    # Find the image filename from the mapping
                                    image_name = aic_to_image.get(clean_sku)
                                    if not image_name:
                                        error_list_fd.append((sku, "AIC not found in Farmadati mapping"))
                                        continue # Skip to next SKU

                                    # Construct the image download URL (URL encode the filename)
                                    from urllib.parse import quote
                                    image_url = f"https://ws.farmadati.it/WS_DOC/GetDoc.aspx?accesskey={PASSWORD}&tipodoc=Z&nomefile={quote(image_name)}"

                                    try:
                                        # Download the image
                                        r = http_session.get(image_url, timeout=45) # Increased timeout
                                        r.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

                                        if not r.content:
                                             error_list_fd.append((sku, "Downloaded file is empty"))
                                             continue

                                        # Process the downloaded image
                                        processed_buffer = process_image_fd(r.content)

                                        # Add the processed image to the ZIP file
                                        zipf.writestr(f"{sku}-h1.jpg", processed_buffer.read())
                                        processed_files_count += 1

                                    except requests.exceptions.Timeout:
                                        error_list_fd.append((sku, "Download timed out"))
                                    except requests.exceptions.HTTPError as http_e:
                                         error_list_fd.append((sku, f"HTTP Error {http_e.response.status_code}"))
                                    except requests.exceptions.RequestException as req_e:
                                         error_list_fd.append((sku, f"Network Error: {req_e}"))
                                    except RuntimeError as proc_e: # Catch processing errors from process_image_fd
                                         error_list_fd.append((sku, f"Processing Error: {proc_e}"))
                                    except Exception as e: # Catch any other unexpected errors
                                         error_list_fd.append((sku, f"Unexpected Error: {e}"))
                                         # Consider logging traceback for unexpected errors
                                         # import traceback
                                         # st.warning(f"Traceback for SKU {sku}: {traceback.format_exc()}")


                    progress_bar_fd.progress(1.0, text="Farmadati processing complete!")

                    # Store results in session state
                    if processed_files_count > 0:
                        zip_buffer.seek(0) # Rewind the buffer before storing
                        st.session_state["renaming_zip_buffer_fd"] = zip_buffer
                    else:
                        st.session_state["renaming_zip_buffer_fd"] = None

                    if error_list_fd:
                        error_df = pd.DataFrame(error_list_fd, columns=["SKU", "Reason"])
                        # Optional: Drop duplicates based on SKU and Reason
                        error_df = error_df.drop_duplicates().sort_values(by="SKU")
                        # Convert DataFrame to CSV bytes
                        csv_error = error_df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
                        st.session_state["renaming_error_data_fd"] = csv_error
                    else:
                        st.session_state["renaming_error_data_fd"] = None

            except Exception as critical_e:
                 st.error(f"A critical error occurred during Farmadati processing: {critical_e}")
                 # import traceback
                 # st.error(f"Traceback: {traceback.format_exc()}")

            # Mark processing as done and stop the trigger
            st.session_state["renaming_processing_done_fd"] = True
            st.session_state.renaming_start_processing_fd = False
            st.rerun() # Rerun to show download buttons


    # --- Download Buttons Section (Farmadati) ---
    if st.session_state.get("renaming_processing_done_fd"):
        st.markdown("---")
        st.subheader("Download Results (Farmadati)")
        col1_fd_dl, col2_fd_dl = st.columns(2)

        # Download Images Button
        with col1_fd_dl:
            zip_data = st.session_state.get("renaming_zip_buffer_fd")
            if zip_data:
                # The buffer is already in memory, no need to open file
                st.download_button(
                    label="Download Images (ZIP)",
                    data=zip_data, # Pass the BytesIO buffer directly
                    file_name=f"farmadati_images_{st.session_state.renaming_session_id[:6]}.zip",
                    mime="application/zip",
                    key="dl_fd_zip",
                    use_container_width=True
                )
            else:
                 st.info("No images were successfully processed and saved.")

        # Download Error List Button
        with col2_fd_dl:
            error_data = st.session_state.get("renaming_error_data_fd")
            if error_data:
                 # The error data is already CSV bytes
                st.download_button(
                    label="Download Missing/Error List (CSV)",
                    data=error_data, # Pass the CSV bytes directly
                    file_name=f"errors_farmadati_{st.session_state.renaming_session_id[:6]}.csv",
                    mime="text/csv",
                    key="dl_fd_err",
                    use_container_width=True
                )
            else:
                st.success("No errors reported during processing.")


# ======================================================
# SECTION: coming soon (Originale)
# ======================================================
elif server_country == "coming soon":
    st.header("Coming Soon")
    st.info("This section is under development. Functionality for other servers will be added here.")
