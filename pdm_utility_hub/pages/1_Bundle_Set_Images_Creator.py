# pages/1_Bundle_Set_Images_Creator.py
import streamlit as st
import streamlit.components.v1 as components
import os
import aiohttp
import asyncio
import pandas as pd
import shutil
import uuid
import time
from io import BytesIO
from PIL import Image, ImageChops
from cryptography.fernet import Fernet

st.set_page_config(
    page_title="Bundle & Set Creator",
    # layout="wide", # RIMOSSO per usare il default (centered)
    initial_sidebar_state="expanded" # Sidebar visibile
)

# --- CSS Globale per nascondere navigazione default e impostare larghezza sidebar ---
# *** COPIA ESATTA DEL BLOCCO CSS DA pdm_hub.py (con sfondo #d8dfe6) ***
st.markdown(
    """
    <style>
    /* Imposta larghezza sidebar e FORZA con !important */
    [data-testid="stSidebar"] > div:first-child {
        width: 550px !important;
        min-width: 550px !important;
        max-width: 550px !important;
    }
    /* Nasconde la navigazione automatica generata da Streamlit nella sidebar */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sfondo per il contenitore principale - NUOVO COLORE FORZATO */
    div[data-testid="stAppViewContainer"] > section > div.block-container {
         background-color: #f7f7f7 !important; /* NUOVO COLORE */
         padding: 2rem 1rem 1rem 1rem !important;
         border-radius: 0.5rem !important;
    }
    .main .block-container {
         background-color: #f7f7f7 !important; /* NUOVO COLORE */
         padding: 2rem 1rem 1rem 1rem !important;
         border-radius: 0.5rem !important;
    }


    /* Stile base per i bottoni/placeholder delle app (dall'hub) */
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
        color: #343a40;
    }
     .app-button-link svg, .app-button-placeholder svg,
     .app-button-link .icon, .app-button-placeholder .icon {
         margin-right: 0.6rem;
         flex-shrink: 0;
     }
    .app-button-link > div[data-testid="stText"] > span:before {
        content: "" !important; margin-right: 0 !important;
    }

    /* Colore UNICO per entrambi i bottoni cliccabili (dall'hub) */
    .app-button-link {
        background-color: #f5faff;
        border: 1px solid #c4daee;
    }
    .app-button-link:hover {
        background-color: #eaf2ff;
        border-color: #a9cce3;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        cursor: pointer;
    }

    /* Stile Placeholder Coming Soon (non cliccabile) (dall'hub) */
    .app-button-placeholder {
        background-color: #f1f3f5;
        opacity: 0.7;
        cursor: default;
        box-shadow: none;
        color: #868e96;
        border: 1px dashed #cccccc;
    }
     .app-button-placeholder .icon {
         font-size: 1.5em;
     }


    /* Stile per descrizione sotto i bottoni (dall'hub) */
     .app-description {
        font-size: 0.9em;
        color: #343a40;
        padding: 0 15px;
        text-align: justify;
        width: 90%;
        margin: 0 auto;
     }

     /* Stili specifici di QUESTA app (Bundle Creator) */
     .stButton > button {
        background-color: #8984b3;
        color: white;
        border: none;
        padding: 8px 16px;
        text-align: center;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #625e8a;
    }
    .stDownloadButton > button {
        background-color: #acbf9b;
        color: white;
        border: none;
        padding: 8px 16px;
        text-align: center;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
    }
    .stDownloadButton > button:hover {
        background-color: #97a888;
    }
    /* Sovrascrive il padding del background per questa pagina specifica */
    /* Dato che ora è layout centered, potremmo non aver bisogno di sovrascrivere */
    /* .main .block-container{
        padding-top: 1rem !important;
        background-color: transparent !important;
        border-radius: 0 !important;
    } */

    </style>
    """,
    unsafe_allow_html=True
)

# --- Bottone per tornare all'Hub nella Sidebar ---
st.sidebar.page_link("pdm_hub.py", label="**PDM Utility Hub**", icon="🏠")
st.sidebar.markdown("---") # Separatore opzionale

# ---------------------- Session State Management ----------------------
if "bundle_creator_session_id" not in st.session_state:
    st.session_state["bundle_creator_session_id"] = str(uuid.uuid4())

# ---------------------- LOGIN RIMOSSO ----------------------

# ---------------------- Begin Main App Code ----------------------
session_id = st.session_state["bundle_creator_session_id"]
base_folder = f"Bundle&Set_{session_id}"

def clear_old_data():
    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)
    zip_path = f"Bundle&Set_{session_id}.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    missing_csv_path = f"missing_images_{session_id}.csv"
    bundle_list_csv_path = f"bundle_list_{session_id}.csv"
    if os.path.exists(missing_csv_path):
        os.remove(missing_csv_path)
    if os.path.exists(bundle_list_csv_path):
        os.remove(bundle_list_csv_path)

# ---------------------- Helper Functions (Originali) ----------------------
async def async_download_image(product_code, extension, session):
    if product_code.startswith(('1', '0')):
        product_code = f"D{product_code}"
    url = f"https://cdn.shop-apotheke.com/images/{product_code}-p{extension}.jpg"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                return content, url
            else:
                return None, None
    except Exception:
        return None, None

def trim(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def process_double_bundle_image(image, layout="horizontal"):
    image = trim(image)
    width, height = image.size
    chosen_layout = "vertical" if (layout.lower() == "automatic" and height < width) else layout.lower()
    if chosen_layout == "horizontal":
        merged_width = width * 2
        merged_height = height
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (width, 0))
    elif chosen_layout == "vertical":
        merged_width = width
        merged_height = height * 2
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (0, height))
    else:
        merged_width = width * 2
        merged_height = height
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (width, 0))

    scale_factor = min(1000 / merged_width, 1000 / merged_height)
    new_size = (int(merged_width * scale_factor), int(merged_height * scale_factor))
    resized_image = merged_image.resize(new_size, Image.LANCZOS)
    final_image = Image.new("RGB", (1000, 1000), (255, 255, 255))
    x_offset = (1000 - new_size[0]) // 2
    y_offset = (1000 - new_size[1]) // 2
    final_image.paste(resized_image, (x_offset, y_offset))
    return final_image

def process_triple_bundle_image(image, layout="horizontal"):
    image = trim(image)
    width, height = image.size
    chosen_layout = "vertical" if (layout.lower() == "automatic" and height < width) else layout.lower()
    if chosen_layout == "horizontal":
        merged_width = width * 3
        merged_height = height
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (width, 0))
        merged_image.paste(image, (width * 2, 0))
    elif chosen_layout == "vertical":
        merged_width = width
        merged_height = height * 3
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (0, height))
        merged_image.paste(image, (0, height * 2))
    else:
        merged_width = width * 3
        merged_height = height
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))
        merged_image.paste(image, (0, 0))
        merged_image.paste(image, (width, 0))
        merged_image.paste(image, (width * 2, 0))

    scale_factor = min(1000 / merged_width, 1000 / merged_height)
    new_size = (int(merged_width * scale_factor), int(merged_height * scale_factor))
    resized_image = merged_image.resize(new_size, Image.LANCZOS)
    final_image = Image.new("RGB", (1000, 1000), (255, 255, 255))
    x_offset = (1000 - new_size[0]) // 2
    y_offset = (1000 - new_size[1]) // 2
    final_image.paste(resized_image, (x_offset, y_offset))
    return final_image

def save_binary_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

async def async_get_nl_fr_images(product_code, session):
    tasks = [
        async_download_image(product_code, "1-fr", session),
        async_download_image(product_code, "1-nl", session)
    ]
    results = await asyncio.gather(*tasks)
    images = {}
    if results[0][0]:
        images["1-fr"] = results[0][0]
    if results[1][0]:
        images["1-nl"] = results[1][0]
    return images

async def async_get_image_with_fallback(product_code, session):
    fallback_ext = st.session_state.get("fallback_ext", None)
    if fallback_ext == "NL FR":
        images_dict = await async_get_nl_fr_images(product_code, session)
        if images_dict:
            return images_dict, "NL FR"
    tasks = [async_download_image(product_code, ext, session) for ext in ["1", "10"]]
    results = await asyncio.gather(*tasks)
    for ext, result in zip(["1", "10"], results):
        content, url = result
        if content:
            return content, ext
    if fallback_ext and fallback_ext != "NL FR":
        content, _ = await async_download_image(product_code, fallback_ext, session)
        if content:
            return content, fallback_ext
    return None, None

# ---------------------- Main Processing Function (Originale) ----------------------
async def process_file_async(uploaded_file, progress_bar=None, layout="horizontal"):
    session_id = st.session_state["bundle_creator_session_id"]
    base_folder = f"Bundle&Set_{session_id}"
    missing_images_csv_path = f"missing_images_{session_id}.csv"
    bundle_list_csv_path = f"bundle_list_{session_id}.csv"

    if "encryption_key" not in st.session_state:
        st.session_state["encryption_key"] = Fernet.generate_key()
    key = st.session_state["encryption_key"]
    f = Fernet(key)

    file_bytes = uploaded_file.read()
    encrypted_bytes = f.encrypt(file_bytes)
    decrypted_bytes = f.decrypt(encrypted_bytes)

    csv_file = BytesIO(decrypted_bytes)
    data = pd.read_csv(csv_file, delimiter=';', dtype=str)

    required_columns = {'sku', 'pzns_in_set'}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None, None, None, None

    if data.empty:
        st.error("The CSV file is empty!")
        return None, None, None, None

    data = data[list(required_columns)]
    data.dropna(inplace=True)

    st.write(f"File loaded: {len(data)} bundles found.")
    os.makedirs(base_folder, exist_ok=True)

    mixed_sets_needed = False
    mixed_folder = os.path.join(base_folder, "mixed_sets")
    error_list = []
    bundle_list = []

    total = len(data)

    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        for i, (_, row) in enumerate(data.iterrows()):
            bundle_code = row['sku'].strip()
            product_codes = [code.strip() for code in row['pzns_in_set'].strip().split(',')]
            num_products = len(product_codes)
            is_uniform = (len(set(product_codes)) == 1)
            bundle_type = f"bundle of {num_products}" if is_uniform else "mixed"
            bundle_cross_country = False

            if is_uniform:
                product_code = product_codes[0]
                folder_name = os.path.join(base_folder, f"bundle_{num_products}")
                if st.session_state.get("fallback_ext") in ["NL FR", "1-fr", "1-de", "1-nl"]:
                    bundle_cross_country = True
                    folder_name = os.path.join(base_folder, "cross-country")
                os.makedirs(folder_name, exist_ok=True)

                if st.session_state.get("fallback_ext") == "NL FR":
                    result, used_ext = await async_get_image_with_fallback(product_code, session)
                    if used_ext == "NL FR" and isinstance(result, dict):
                        for lang, image_data in result.items():
                            suffix = "-p1-fr" if lang == "1-fr" else "-p1-nl"
                            try:
                                img = await asyncio.to_thread(Image.open, BytesIO(image_data))
                                if num_products == 2:
                                    final_img = await asyncio.to_thread(process_double_bundle_image, img, layout)
                                elif num_products == 3:
                                    final_img = await asyncio.to_thread(process_triple_bundle_image, img, layout)
                                else:
                                    final_img = img
                                save_path = os.path.join(folder_name, f"{bundle_code}{suffix}.jpg")
                                await asyncio.to_thread(final_img.save, save_path, "JPEG", quality=100)
                            except Exception as e:
                                st.error(f"Error processing image for bundle {bundle_code}: {e}")
                                error_list.append((bundle_code, product_code))
                    elif result:
                        try:
                            img = await asyncio.to_thread(Image.open, BytesIO(result))
                            if num_products == 2:
                                final_img = await asyncio.to_thread(process_double_bundle_image, img, layout)
                            elif num_products == 3:
                                final_img = await asyncio.to_thread(process_triple_bundle_image, img, layout)
                            else:
                                final_img = img
                            save_path = os.path.join(folder_name, f"{bundle_code}-h1.jpg")
                            await asyncio.to_thread(final_img.save, save_path, "JPEG", quality=100)
                        except Exception as e:
                            st.error(f"Error processing image for bundle {bundle_code}: {e}")
                            error_list.append((bundle_code, product_code))
                    else:
                        error_list.append((bundle_code, product_code))
                else:
                    image_data, used_ext = await async_get_image_with_fallback(product_code, session)
                    if used_ext in ["1-fr", "1-de", "1-nl"]:
                        bundle_cross_country = True
                        folder_name = os.path.join(base_folder, "cross-country")
                        os.makedirs(folder_name, exist_ok=True)
                    if image_data:
                        try:
                            img = await asyncio.to_thread(Image.open, BytesIO(image_data))
                            if num_products == 2:
                                final_img = await asyncio.to_thread(process_double_bundle_image, img, layout)
                            elif num_products == 3:
                                final_img = await asyncio.to_thread(process_triple_bundle_image, img, layout)
                            else:
                                final_img = img
                            suffix = "-h1"
                            save_path = os.path.join(folder_name, f"{bundle_code}{suffix}.jpg")
                            await asyncio.to_thread(final_img.save, save_path, "JPEG", quality=100)
                        except Exception as e:
                            st.error(f"Error processing image for bundle {bundle_code}: {e}")
                            error_list.append((bundle_code, product_code))
                    else:
                        error_list.append((bundle_code, product_code))

            else:
                mixed_sets_needed = True
                bundle_folder = os.path.join(mixed_folder, bundle_code)
                os.makedirs(bundle_folder, exist_ok=True)
                for p_code in product_codes:
                    if st.session_state.get("fallback_ext") == "NL FR":
                        result, used_ext = await async_get_image_with_fallback(p_code, session)
                        if used_ext == "NL FR" and isinstance(result, dict):
                            for lang, image_data in result.items():
                                suffix = "-p1-fr" if lang == "1-fr" else "-p1-nl"
                                prod_folder = os.path.join(bundle_folder, "cross-country")
                                os.makedirs(prod_folder, exist_ok=True)
                                file_path = os.path.join(prod_folder, f"{p_code}{suffix}.jpg")
                                await asyncio.to_thread(save_binary_file, file_path, image_data)
                        elif result:
                            suffix = "-h1"
                            prod_folder = os.path.join(bundle_folder, "cross-country") if used_ext in ["1-fr", "1-de", "1-nl"] else bundle_folder
                            os.makedirs(prod_folder, exist_ok=True)
                            file_path = os.path.join(prod_folder, f"{p_code}{suffix}.jpg")
                            await asyncio.to_thread(save_binary_file, file_path, result)
                        else:
                            error_list.append((bundle_code, p_code))
                    else:
                        image_data, used_ext = await async_get_image_with_fallback(p_code, session)
                        if used_ext in ["1-fr", "1-de", "1-nl"]:
                            bundle_cross_country = True
                        if image_data:
                            prod_folder = os.path.join(bundle_folder, "cross-country") if used_ext in ["1-fr", "1-de", "1-nl"] else bundle_folder
                            os.makedirs(prod_folder, exist_ok=True)
                            file_path = os.path.join(prod_folder, f"{p_code}.jpg")
                            await asyncio.to_thread(save_binary_file, file_path, image_data)
                        else:
                            error_list.append((bundle_code, p_code))

            if progress_bar is not None:
                progress_bar.progress((i + 1) / total)

            bundle_list.append([bundle_code, ', '.join(product_codes), bundle_type, "Yes" if bundle_cross_country else "No"])

    if not mixed_sets_needed and os.path.exists(mixed_folder):
        shutil.rmtree(mixed_folder)

    missing_images_data = None
    missing_images_df = pd.DataFrame(columns=["PZN Bundle", "PZN with image missing"])
    if error_list:
        missing_images_df = pd.DataFrame(error_list, columns=["PZN Bundle", "PZN with image missing"])
        missing_images_df = missing_images_df.groupby("PZN Bundle", as_index=False).agg({
            "PZN with image missing": lambda x: ', '.join(sorted(list(set(x))))
        })
        missing_images_df.to_csv(missing_images_csv_path, index=False, sep=';', encoding='utf-8-sig')
        with open(missing_images_csv_path, "rb") as f_csv:
            missing_images_data = f_csv.read()

    bundle_list_data = None
    if bundle_list:
        bundle_list_df = pd.DataFrame(bundle_list, columns=["sku", "pzns_in_set", "bundle type", "cross-country"])
        bundle_list_df.to_csv(bundle_list_csv_path, index=False, sep=';', encoding='utf-8-sig')
        with open(bundle_list_csv_path, "rb") as f_csv:
            bundle_list_data = f_csv.read()

    zip_bytes = None
    if os.path.exists(base_folder) and any(os.scandir(base_folder)):
        temp_parent = f"Bundle&Set_temp_{session_id}"
        if os.path.exists(temp_parent): shutil.rmtree(temp_parent)
        os.makedirs(temp_parent, exist_ok=True)
        zip_content_folder = os.path.join(temp_parent, "Bundle&Set")
        shutil.copytree(base_folder, zip_content_folder)
        zip_base_name = f"Bundle&Set_archive_{session_id}"
        try:
            shutil.make_archive(zip_base_name, 'zip', temp_parent)
            final_zip_path = f"{zip_base_name}.zip"
            if os.path.exists(final_zip_path):
                with open(final_zip_path, "rb") as zip_file:
                    zip_bytes = zip_file.read()
                os.remove(final_zip_path)
            else:
                 st.error("Failed to create ZIP archive.")
        except Exception as e:
            st.error(f"Error during zipping: {e}")
        finally:
            if os.path.exists(temp_parent): shutil.rmtree(temp_parent)

    return zip_bytes, missing_images_data, missing_images_df, bundle_list_data

# ---------------------- End of Function Definitions ----------------------

# --- Titolo Modificato ---
st.title("PDM Bundle&Set Image Creator")

# --- How to Use Modificato ---
st.markdown(
    """
    **How to use:**

    1. Create a Quick Report in Akeneo containing the list of products.
    2. Select the following options:
       - File Type: CSV - All Attributes or Grid Context (for Grid Context, select ID and PZN included in the set) - With Codes - Without Media
    3. **Choose the language for language specific photos:** (if needed)
    4. **Choose bundle layout:** (Horizontal, Vertical, or Automatic)
    5. Click **Process CSV** to start the process.
    6. Download the files.
    7. **Before starting a new process, click on Clear Cache and Reset Data.**
    """
)

# --- Bottone Reset SPOSTATO QUI ---
if st.button("🧹 Clear Cache and Reset Data"):
    keys_to_remove = [k for k in st.session_state if k.startswith('bundle_') or k in ['fallback_ext', 'encryption_key', 'zip_data', 'bundle_list_data', 'missing_images_data', 'missing_images_df', 'processing_complete_bundle', 'file_uploader']]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    st.cache_data.clear()
    st.cache_resource.clear()
    # Assicurati che la funzione sia definita
    if 'clear_old_data' in locals():
        clear_old_data()
    st.success("Data cleared.")
    st.rerun()

# --- Sidebar Content Modificato ---
st.sidebar.header("What This App Does")
st.sidebar.markdown(
    """
    - ❓ **Automated Bundle&Set Creation:** Automatically create product bundles and mixed set by downloading and organizing images;
    - 🔎 **Language Selection:** Choose the language if you have language-specific photos. NL-FR, DE, FR;
    - 🔎 **Choose the layout for double/triple bundles:** Automatic, Horizontal or Vertical;
    - ✏️ **Dynamic Processing:** Combine images (double/triple) with proper resizing;
    - ✏️ **Rename images** using the specific bundle&set code (e.g. -h1, -p1-fr, -p1-nl, etc);
    - ❌ **Error Logging:** Missing images are logged in a CSV;
    - 📥 **Download:** Get a ZIP with all processed images and reports;
    - 🌐 **Interactive Preview:** Preview and download individual product images from the sidebar.
    """, unsafe_allow_html=True
)

# --- Sidebar Preview (Originale) ---
st.sidebar.header("Product Image Preview")
product_code_preview = st.sidebar.text_input("Enter Product Code:", key="preview_pzn_bundle")
selected_extension = st.sidebar.selectbox("Select Image Extension:", [str(i) for i in range(1, 19)], key="sidebar_ext_bundle")
with st.sidebar:
    col_button, col_spinner = st.columns([2, 1])
    show_image = col_button.button("Show Image", key="show_preview_bundle")
    spinner_placeholder = col_spinner.empty()

if show_image and product_code_preview:
    with spinner_placeholder:
        with st.spinner("Processing..."):
            pzn_url = product_code_preview
            if pzn_url.startswith(('1', '0')): pzn_url = f"D{pzn_url}"
            preview_url = f"https://cdn.shop-apotheke.com/images/{pzn_url}-p{selected_extension}.jpg"
            image_data = None
            try:
                import requests
                response = requests.get(preview_url, stream=True, timeout=10)
                if response.status_code == 200:
                     image_data = response.content
            except Exception:
                pass
    if image_data:
        try:
            image = Image.open(BytesIO(image_data))
            st.sidebar.image(image, caption=f"Product: {product_code_preview} (p{selected_extension})", use_container_width=True)
            st.sidebar.download_button(
                label="Download Image",
                data=image_data,
                file_name=f"{product_code_preview}-p{selected_extension}.jpg",
                mime="image/jpeg",
                key="dl_preview_bundle"
            )
        except Exception:
             st.sidebar.error("Could not display preview image.")
    else:
        st.sidebar.error(f"No image found for {product_code_preview} with -p{selected_extension}.jpg")

# --- Main Area UI (Originale) ---
uploaded_file = st.file_uploader("**Upload CSV File**", type=["csv"], key="file_uploader")
if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        fallback_language = st.selectbox("**Choose the language for language specific photos:**", options=["None", "FR", "DE", "NL FR"], index=0, key="lang_select_bundle")
    with col2:
        layout_choice = st.selectbox("**Choose bundle layout:**", options=["Horizontal", "Vertical", "Automatic"], index=2, key="layout_select_bundle")

    if fallback_language == "NL FR":
        st.session_state["fallback_ext"] = "NL FR"
    elif fallback_language != "None":
        st.session_state["fallback_ext"] = f"1-{fallback_language.lower()}"
    else:
        st.session_state["fallback_ext"] = None

    if st.button("Process CSV", key="process_csv_bundle"):
        start_time = time.time()
        progress_bar = st.progress(0, text="Starting processing...")
        try:
            # Assicurati che la funzione sia definita
            if 'process_file_async' not in locals():
                 st.error("Processing function not found!")
                 st.stop()

            zip_data, missing_images_data, missing_images_df, bundle_list_data = asyncio.run(process_file_async(uploaded_file, progress_bar, layout=layout_choice))
            progress_bar.empty()
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            st.success(f"Processing finished in {minutes}m {seconds}s.")

            st.session_state["zip_data"] = zip_data
            st.session_state["bundle_list_data"] = bundle_list_data
            st.session_state["missing_images_data"] = missing_images_data
            st.session_state["missing_images_df"] = missing_images_df
            st.session_state["processing_complete_bundle"] = True

        except Exception as e:
             progress_bar.empty()
             st.error(f"An error occurred: {e}")
             st.session_state["processing_complete_bundle"] = False


# --- Sezione Download Modificata (Senza Titolo, Verticale) ---
if st.session_state.get("processing_complete_bundle", False):
    st.markdown("---") # Separatore

    # Bottone Download ZIP
    if st.session_state.get("zip_data"):
        st.download_button(
            label="Download Bundle Images (ZIP)",
            data=st.session_state["zip_data"],
            file_name=f"BundleSet_{session_id}.zip",
            mime="application/zip",
            key="dl_zip_bundle_v"
        )
    else:
        st.info("No ZIP file generated.")

    # Bottone Download Lista Bundle
    if st.session_state.get("bundle_list_data"):
        st.download_button(
            label="Download Bundle List (CSV)",
            data=st.session_state["bundle_list_data"],
            file_name=f"bundle_list_{session_id}.csv",
            mime="text/csv",
            key="dl_list_bundle_v"
        )
    else:
        st.info("No bundle list generated.")

    # Sezione Immagini Mancanti
    missing_df = st.session_state.get("missing_images_df")
    if missing_df is not None and not missing_df.empty:
        st.markdown("---") # Separatore prima della tabella errori
        st.warning(f"{len(missing_df)} bundles with missing images:")
        st.dataframe(missing_df.head(), use_container_width=True) # Mostra tabella
        # Bottone Download Lista Errori
        if st.session_state.get("missing_images_data"):
            st.download_button(
                label="Download Missing List (CSV)",
                data=st.session_state["missing_images_data"],
                file_name=f"missing_images_{session_id}.csv",
                mime="text/csv",
                key="dl_missing_bundle_v"
            )
    elif missing_df is not None: # Esiste ma è vuoto
         st.success("No missing images reported.")
