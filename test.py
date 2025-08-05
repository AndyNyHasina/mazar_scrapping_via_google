import os
import shutil
import zipfile
import requests
import logging
from Global_var import current_dir , PATH_EXTENSION
from extra_utils import write_manifest_file
logger = logging.getLogger(__name__)  


def download_and_load_extension():
    #url = 'https://nopecha.com/f/ext.crx'
    url = "https://github.com/NopeCHALLC/nopecha-extension/releases/download/0.4.13/chromium_automation.zip"

    crx_path = 'chrome.zip'
    folder_path = 'extension_nopecha'

    with open(crx_path, 'wb') as f:
        f.write(requests.get(url).content)

    # Décompresser le .crx comme un .zip
    with zipfile.ZipFile(crx_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
    
    if os.path.exists(os.path.join(__file__  , f"extension_nopecha/{crx_path}")):
        logger.info("Suppression du fichier zip")
        shutil.rmtree(crx_path, ignore_errors=True)
        
        
def check_extension():
    
    if not os.path.exists(PATH_EXTENSION) :
        download_and_load_extension()
        write_manifest_file(image_selector="#captcha-form img" ,text_selector="#captcha")
    return PATH_EXTENSION
