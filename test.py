import os
import zipfile
import requests

# Télécharger le fichier .crx
url = 'https://nopecha.com/f/ext.crx'
crx_path = 'ext.crx'
folder_path = 'extension_nopecha'

with open(crx_path, 'wb') as f:
    f.write(requests.get(url).content)

# Décompresser le .crx comme un .zip
with zipfile.ZipFile(crx_path, 'r') as zip_ref:
    zip_ref.extractall(folder_path)
