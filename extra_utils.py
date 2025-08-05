import os
import json
from Global_var import PATH_EXTENSION

def access_file(manifest_path):
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = f.read()
        if data:
            return json.loads(data)
    return {}

def write_manifest_file(image_selector, text_selector):
    if os.path.exists(PATH_EXTENSION):
        manifest_path = os.path.join(PATH_EXTENSION, 'manifest.json')
        json_data = access_file(manifest_path)
        nopecha = json_data.get("nopecha")
        nopecha['textcaptcha_image_selector'] = image_selector
        nopecha['textcaptcha_input_selector'] = text_selector
        nopecha['textcaptcha_auto_solve'] = True
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
    else:
        raise Exception(f"Le dossier {PATH_EXTENSION} n'existe pas")

def get_value_manifest(): 
    if os.path.exists(PATH_EXTENSION):
        manifest_path = os.path.join(PATH_EXTENSION, 'manifest.json')
        json_data = access_file(manifest_path)
        nopecha = json_data.get("nopecha")
        
        im_selector = nopecha.get('textcaptcha_image_selector') 
        text_selector = nopecha.get('textcaptcha_input_selector') 
        textcapcha_activator = nopecha.get('textcaptcha_auto_solve') 
        return im_selector , text_selector , textcapcha_activator
    else:
        raise Exception(f"Le dossier {PATH_EXTENSION} n'existe pas")