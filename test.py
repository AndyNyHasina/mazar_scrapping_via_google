import os
import zipfile
import requests
from Global_var import current_dir , PATH_EXTENSION

def download_and_load_extension():
    url = 'https://nopecha.com/f/ext.crx'
    crx_path = 'ext.crx'
    folder_path = 'extension_nopecha'

    with open(crx_path, 'wb') as f:
        f.write(requests.get(url).content)

    # Décompresser le .crx comme un .zip
    with zipfile.ZipFile(crx_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
        
        
def check_extension():
    
    if not os.path.exists(PATH_EXTENSION) :
        download_and_load_extension()
    return PATH_EXTENSION
