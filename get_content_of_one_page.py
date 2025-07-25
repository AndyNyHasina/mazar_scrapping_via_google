import json
import asyncio
import random
from playwright.async_api import async_playwright
from GPT import GPT_ask
from playwright_stealth import Stealth
import shutil
import os 
async def runChrome(search_url: str, gpt:GPT_ask ,compagny:str   , refere : str):
    
    async with Stealth().use_async(async_playwright()) as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="test",
            headless=False,
            ignore_default_args=['--enable-automation'],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",

            ],


            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        )
        #page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        page = await context.new_page()
        await page.set_extra_http_headers({
    "Referer": f"{refere}"
})


        await page.goto(search_url, wait_until="domcontentloaded", timeout=60000  )
        await load_dom(page, gpt, compagny)
        await asyncio.sleep(random.uniform(30 ,60))
        await context.close()
        
        
async def load_dom(page, gpt, compagny):
    selector = 'section.profile'
    await page.wait_for_load_state('domcontentloaded')
    await page.wait_for_selector(selector, timeout=20000)

    profile = await page.query_selector(selector)
    if not profile:
        raise Exception('Pas de section profile trouvée')
    
    content_html = await profile.inner_text()
    gpt_response = ask_gpt(gpt=gpt, content_linkedin=content_html, compagny=compagny)
    json_data = str_to_json(str_data=gpt_response)
    
    if not json_data:
        return
    content = json_data.get("content")
    if  content == "vide":
        return
    
    informations = content.get("informations_personnelles", {})
    nom = informations.get("nom")
    
    if nom:
        write_ceo(data=nom, file_name=compagny)
        print(f"Nom du CEO/CFO détecté : {nom}")
    else:
        print("Aucun nom trouvé dans les informations personnelles.")
    
    print("Analyse terminée.")


def str_to_json(str_data):
    try:
        return json.loads(str_data)
    except json.JSONDecodeError:
        print("❌ Erreur : la chaîne n'est pas du JSON valide.")
        return None

def ask_gpt(gpt: GPT_ask, content_linkedin, compagny):
    input_data ={
        "texte_extrait" : content_linkedin ,
        "compagnie" : compagny
    }
    return gpt.conversation(input_data)


async def main_function(search_url: str, gpt: GPT_ask, compagny: str , page):
    path_session = r'C:\Users\Hasina_IA\Documents\vscode\laida_linkdin_2.0\test'
    url = page.url
    async def safe_run():
        
        try:
            await runChrome(search_url=search_url, gpt=gpt, compagny=compagny  ,refere = url)
        except Exception as e :
            print(e)
        finally :
            if os.path.exists(path_session):
                shutil.rmtree(path_session, ignore_errors=True)


    try:
        await safe_run()
    except Exception as e:
        print(f"Erreur détectée : {e}, tentative de relance...")
        await safe_run()

def write_ceo(file_name, data):
    with open(f"{file_name}.txt", 'a', encoding='utf-8') as f:
        f.write(f"{data}\n")

