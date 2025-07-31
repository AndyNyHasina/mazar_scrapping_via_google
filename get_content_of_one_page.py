import json
import asyncio
import random
from playwright.async_api import async_playwright, Page
import urllib
from GPT import GPT_ask
from playwright_stealth import Stealth
import shutil
import os 
from Global_var import combinaison , current_dir , PATH_EXTENSION
from test import check_extension
async def runChrome(search_url: str, gpt:GPT_ask ,compagny:str   , refere : str , viewport: tuple[int , int]  , user_agent : str , counter : int , gpu_vendor : str ):
    
    async with Stealth().use_async(async_playwright()) as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="test",
            headless=False,
            ignore_default_args=['--enable-automation'],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                f"--disable-extensions-except={PATH_EXTENSION}",
                f"--load-extension={PATH_EXTENSION}",

            ],
            viewport={'width': viewport[0], 'height': viewport[1]},
            user_agent=user_agent
        )
        
        script = f"""
            // Fausser languages
            Object.defineProperty(navigator, 'languages', {{
                get: () => ["fr-FR","en-US","fr","en"],
            }});

            // Supprimer les propriétés chrome
            window.chrome = {{
                runtime: {{}},
            }};

            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({{ state: Notification.permission }}) :
                originalQuery(parameters)
            );

            // Empêcher WebGL detection (optionnel)
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return "{gpu_vendor}";
                return getParameter.call(this, parameter);
            }};
            
            HTMLVideoElement.prototype.canPlayType = (type) => {{
                return "probably";
            }};
        """
        await context.add_init_script(script)
        if counter == 3 :
            print("via refer google to access profile")
            print(search_url)
            page = await access_via_google(context=context  ,search= search_url)
            
        elif counter == 2 :
            print("via refer to access linkdin")
            page = await access_via_linkdin(context=context )
            search_url+= '?trk=people-guest_people_search-card'
        
        else : 
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            
            
        await page.goto(f'{search_url}?trk=people-guest_people_search-card', wait_until="domcontentloaded", timeout=60000  )
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

async def main_function(search_url: str, gpt: GPT_ask, compagny: str , page:Page , index : int):
    check_extension()
    counter = 3
    combinaison_value = combinaison()
    resolution_and_user_agent_value_and_gpu  = combinaison_value[index]
    print(resolution_and_user_agent_value_and_gpu)
    viewport_value = resolution_and_user_agent_value_and_gpu[0]
    user_agent_value = resolution_and_user_agent_value_and_gpu[1]
    gpu_vendor = resolution_and_user_agent_value_and_gpu[2]
    path_session = os.path.join(current_dir, 'test')
    url = page.url
    async def safe_run(counter):
        try:
            await runChrome(search_url=search_url, gpt=gpt, compagny=compagny  ,refere = url  , viewport=viewport_value , user_agent=user_agent_value , counter = counter , gpu_vendor=gpu_vendor)
        finally :
            if os.path.exists(path_session):
                print("suppression de la session precedente")
                shutil.rmtree(path_session, ignore_errors=True)
    while(counter > 0) :
        try:
            await safe_run(counter)
            return
        except Exception as e:
            print(e)
            counter-=1
            print(f"{counter} tentative , tentative de relance...")
            

def write_ceo(file_name, data):
    with open(f"{file_name}.txt", 'a', encoding='utf-8') as f:
        f.write(f"{data}\n")


async def check_url(page):
    await page.wait_for_load_state("domcontentloaded")
    if page.url.startswith('https://www.google.com/sorry/index?continue'):
        await page.wait_for_function(
            "() => window.location.href.startsWith('https://www.google.com/search')", timeout = 0
        )
        await page.wait_for_load_state("domcontentloaded")


async def access_via_google(context , search) :
    search_parse = generate_google_search_url(query=search)
    page0  = context.pages[0] if len(context.pages) > 0 else await context.new_page()
    try : 
        await page0.goto(f'{search_parse}', wait_until="networkidle", timeout=60000  )
        await check_url(page0)
        await page0.wait_for_load_state("networkidle" , timeout = 0)
    except Exception as e : 
        print(e)
    page = await context.new_page()
    await page.set_extra_http_headers({
"Referer": f"{page0.url}"
})
    return page

async def access_via_linkdin(context):
    page0  = context.pages[0] if len(context.pages) > 0 else await context.new_page()
    try: 
        await page0.goto("https://www.linkedin.com/", wait_until="networkidle", timeout=100000 )
    except Exception as e : 
        print(e)
    try :
        page1 = await context.new_page()
        await page1.set_extra_http_headers({
"Referer": f"{page0.url}"
})
        await page1.goto("https://www.linkedin.com/pub/dir/+/+?trk=guest_homepage-basic_guest_nav_menu_people", wait_until="networkidle", timeout=1000000  )
        
    except Exception as e : 
        print(e)
    page = await context.new_page()
    return page


def generate_google_search_url(query: str, domain: str = "linkedin.com/in/") -> str:
    import re
    important_query = query.split("/in/")[1]
    resultat = re.sub(r"\d", "", important_query)
    full_query = f'site:{domain} "{resultat}"'
    encoded_query = urllib.parse.quote_plus(full_query)
    google_url = f"https://www.google.com/search?q={encoded_query}"

    return google_url
