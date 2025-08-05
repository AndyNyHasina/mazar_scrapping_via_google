import json
import logging
import asyncio
import random
from playwright.async_api import async_playwright, Page
import urllib
from GPT import GPT_ask
from playwright_stealth import Stealth
import shutil
import os 
from Global_var import combinaison , current_dir , PATH_EXTENSION
from extra_utils import write_manifest_file
from test import check_extension
import re

logger = logging.getLogger(__name__)  

async def runChrome(search_url: str, gpt: GPT_ask, compagny: str, refere: str,
                    viewport: tuple[int, int], user_agent: str, counter: int, gpu_vendor: str | tuple[str, str]):

    async with Stealth().use_async(async_playwright()) as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="test",
            headless=False,
            locale="en-US",
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

        if isinstance(gpu_vendor, tuple):
            vendor_script = f"""
                Object.defineProperty(navigator, 'platform', {{ get: () => 'Win64' }});
            
                window.chrome = {{ runtime: {{}} }};
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({{ state: Notification.permission }}) :
                    originalQuery(parameters)
                );
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) return "{gpu_vendor[0]}";
                    if (parameter === 37446) return "{gpu_vendor[1]}";
                    return getParameter.call(this, parameter);
                }};
                HTMLVideoElement.prototype.canPlayType = (type) => "probably";
            """
        else:
            vendor_script = f"""
                Object.defineProperty(navigator, 'platform', {{ get: () => 'Win64' }});

                window.chrome = {{ runtime: {{}} }};
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({{ state: Notification.permission }}) :
                    originalQuery(parameters)
                );
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) return "{gpu_vendor}";
                    return getParameter.call(this, parameter);
                }};
                HTMLVideoElement.prototype.canPlayType = (type) => "probably";
            """

        await context.add_init_script(vendor_script)

        if counter == 3:
            logging.info("Navigation via Google referer pour accéder au profil")
            logging.debug(f"URL: {search_url}")
            page = await access_via_google(context=context, search=search_url, compagny=compagny)
        elif counter == 2:
            logging.info("Navigation via LinkedIn referer")
            page = await access_via_linkdin(context=context)
            search_url += '?trk=people-guest_people_search-card'
        else:
            page = context.pages[0] if context.pages else await context.new_page()

        await page.goto(f'{search_url}', wait_until="domcontentloaded", timeout=60000)
        await load_dom(page, gpt, compagny)
        await asyncio.sleep(random.uniform(30, 60))
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
    if content == "vide":
        return
    informations = content.get("informations_personnelles", {})
    nom = informations.get("nom")
    if nom:
        write_ceo(data=nom, file_name=compagny)
        logging.info(f"Nom du CEO/CFO détecté : {nom}")
    else:
        logging.warning("Aucun nom trouvé dans les informations personnelles.")
    logging.info("Analyse terminée.")
    
    
def str_to_json(str_data):
    try:
        print(str_data)
        return json.loads(str_data)
    except json.JSONDecodeError as e :
    
        logging.error(f"❌ Erreur : la chaîne n'est pas du JSON valide. erreur  : {str(e)}")
        return None


def ask_gpt(gpt: GPT_ask, content_linkedin : str, compagny : str):
    input_data = {"texte_extrait": content_linkedin, "compagnie": compagny}
    return gpt.conversation(input_data)

async def main_function(search_url: str, gpt: GPT_ask, compagny: str, page: Page, index: int):
    check_extension()
    counter = 3
    combinaison_value = combinaison()
    resolution_and_user_agent_value_and_gpu = combinaison_value[index]
    logging.info(f"Profil: {resolution_and_user_agent_value_and_gpu}")
    viewport_value = resolution_and_user_agent_value_and_gpu[0]
    user_agent_value = resolution_and_user_agent_value_and_gpu[1]
    gpu_vendor = resolution_and_user_agent_value_and_gpu[2]
    path_session = os.path.join(current_dir, 'test')
    url = page.url

    async def safe_run(counter):
        try:
            await runChrome(search_url=search_url, gpt=gpt, compagny=compagny,
                            refere=url, viewport=viewport_value, user_agent=user_agent_value,
                            counter=counter, gpu_vendor=gpu_vendor)
        finally:
            if os.path.exists(path_session):
                logging.info("Suppression de l'ancienne session utilisateur")
                shutil.rmtree(path_session, ignore_errors=True)

    while counter > 0:
        try:
            await safe_run(counter)
            return
        except Exception as e:
            logging.error(str(e))
            counter -= 1
            logging.warning(f"{counter} tentative(s) restante(s), relance...")


def write_ceo(file_name, data):
    with open(f"{file_name}.txt", 'a', encoding='utf-8') as f:
        f.write(f"{data}\n")


async def check_url(page):
    await page.wait_for_load_state("domcontentloaded")
    if page.url.startswith('https://www.google.com/sorry/index?continue'):
        logging.warning("⚠️ Redirection vers la page CAPTCHA détectée. Attente du retour à la recherche...")
        check_text_captcha_google(page=page)
        await page.wait_for_function(
                    "() => window.location.href.startsWith('https://www.google.com/search')", timeout=0
                )
        await page.wait_for_load_state("domcontentloaded")
        logging.info("✅ Retour sur la page de recherche Google")


async def access_via_google(context, search, compagny):
    search_parse = generate_google_search_url(query=search, compagny=compagny)
    page0 = context.pages[0] if context.pages else await context.new_page()
    try:
        await page0.goto(f'{search_parse}', wait_until="networkidle", timeout=60000)
        await check_url(page0)
    except Exception as e:
        logging.error(str(e))
    page = await context.new_page()
    await page.set_extra_http_headers({
        "Referer": f"{page0.url}" 
        #"https://www.google.com"
        })
    return page


async def access_via_linkdin(context):
    page0 = context.pages[0] if context.pages else await context.new_page()
    try:
        await page0.goto("https://www.linkedin.com/", wait_until="networkidle", timeout=0)
        await asyncio.sleep(random.uniform(50, 60))
        logging.debug(f"Page LinkedIn chargée : {page0.url}")
    except Exception as e:
        logging.error(str(e))
    try:
        page1 = await context.new_page()
        await page1.set_extra_http_headers({"Referer": f"{page0.url}"})
        await page1.goto("https://www.linkedin.com/pub/dir/+/+?trk=guest_homepage-basic_guest_nav_menu_people", wait_until="networkidle", timeout=60000)
        await asyncio.sleep(random.uniform(50, 60))
    except Exception as e:
        logging.error(str(e))
    page = await context.new_page()
    return page


def generate_google_search_url(query: str, compagny: str, domain: str = "linkedin.com/in/") -> str:
    important_query = query.split("/in/")[1]
    important_query_clean = re.sub(r'-[^-]*\d[^-]*$', '', important_query)
    text_clean = re.sub(r'-', ' ', important_query_clean)
    full_query = f'site:{domain} "{text_clean} " {compagny}'
    encoded_query = urllib.parse.quote_plus(full_query)
    google_url = f"https://www.google.com/search?q={encoded_query}&num=100"
    return google_url




async def check_text_captcha_google(page):
    selector_bouton = "input[type='submit']"
    selector_text = "#captcha"
    selector_img = '#captcha-form img'

    await page.wait_for_load_state("domcontentloaded")

    has_bouton = await page.locator(selector_bouton).count() > 0
    has_text = await page.locator(selector_text).count() > 0
    has_img = await page.locator(selector_img).count() > 0

    if has_bouton and has_text and has_img:
        input_selector = selector_text

        write_manifest_file(
            image_selector=selector_img,
            text_selector=input_selector
        )

        await page.reload()
        await page.wait_for_selector(input_selector)

        await page.wait_for_function(
            f"() => document.querySelector('{input_selector}').value.length > 0",
            timeout=30000
        )

        await page.locator(selector_bouton).click()
        print("✅ CAPTCHA texte rempli et envoyé automatiquement.")
    else:
        print("❌ Aucun CAPTCHA texte détecté ou incomplet.")












        










