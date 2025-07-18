
import zipfile
import requests

with open('chromium_automation.zip', 'wb') as f:
    f.write(requests.get('https://github.com/NopeCHALLC/nopecha-extension/releases/latest/download/chromium_automation.zip').content)

with zipfile.ZipFile('chromium_automation.zip', 'r') as zip_ref:
    zip_ref.extractall("nopecha")