import asyncio
import random
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
from playwright_stealth import Stealth
from captchaai import CaptchaAI
EXTENSION_PATH = r"C:\Users\Hasina_IA\Documents\vscode\laida_linkdin_2.0\extension_nopecha"

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

async def human_type(locator, text, delay_range=(0.05, 0.15)):
    for char in text:
        await locator.type(char)
        await asyncio.sleep(random.uniform(*delay_range))


async def runChrome(search_url: str, proxies=None):
    async with async_playwright() as p:
    
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_PATH,
            headless=False,
            ignore_default_args=['--enable-automation'],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}",
            ],
            viewport={'width': 1366, 'height': 645},
            locale="en-US",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        )

        await context.add_init_script("""
            delete Object.getPrototypeOf(navigator).webdriver

            // Fausser languages
            Object.defineProperty(navigator, 'languages', {
                get: () => [ "fr-FR","en-US","fr","en"],
            });

            // Supprimer les propriétés chrome
            window.chrome = {
                runtime: {},
                // Ajouter ici d'autres propriétés si besoin
            };

            // Empêcher la détection de permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );

            // Empêcher WebGL detection (optionnel)
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
                    return "Google Inc. (Intel)";
                }

                if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
                    return "ANGLE (Intel, Intel(R) HD Graphics 5500 (0x00001616) Direct3D11 vs_5_0 ps_5_0, D3D11)";
                }
                return getParameter(parameter);
            };
            HTMLVideoElement.prototype.canPlayType = (type) => {

    return "probably";
  };
        """)

        page =  context.pages[0]  if  context.pages[0] else  await context.new_page()

        await page.goto(search_url, wait_until="networkidle", timeout=0)
        #await page.goto("https://www.google.com/recaptcha/api2/demo", wait_until="networkidle", timeout=0)
        await main_loop(page)
        input("")
        
        await context.close()

import urllib.parse
def generate_google_search_url(query: str, domain: str = "linkedin.com/in/") -> str:
    # Crée la requête complète avec site:...
    full_query = f'site:{domain} "{query}"'
    
    # Encode la requête pour l'URL
    encoded_query = urllib.parse.quote_plus(full_query)
    
    # Crée l'URL complète Google
    google_url = f"https://www.google.com/search?q={encoded_query}"
    
    return google_url





async def get_list_link(page):
    selector = 'div[role="main"] span > a'
    await page.wait_for_selector(selector, timeout=0)
    list_link = await page.query_selector_all(selector)
    
    hrefs = []
    for link in list_link:
        href = await link.get_attribute("href")
        if href and "linkedin" in href:
            hrefs.append(href)
            
    write_file('\n'.join(hrefs))
    return hrefs





def write_file(data):
    with open('text.txt', 'w', encoding='utf-8') as f:
        f.write(data)


async def change_page(page):
    selector = 'div[role = "main"] a#pnnext.LLNLxf'
    next_button1 = page.locator(selector)
    next_button = await page.query_selector(selector) 
    if next_button : 
        await smooth_scroll_to_element(page, next_button1)
        await next_button.click()
        await page.wait_for_timeout(random.uniform(5,20)*1000)
        return True
    else : 
        return False


async def main_loop(page):
    while(True):
        await check_url(page)
        hrefs = await get_list_link(page)
        print(hrefs)
        print("*"*10)
        is_next_page_exist =await change_page(page)
        if not  is_next_page_exist : 
            break
        
import asyncio

# Scroll lent vers un élément
async def smooth_scroll_to_element(page, locator, steps=[5,9], timeout=[5, 10]):
    step =int(random.uniform(*steps)*10)
    
    print(step)
    timeout = random.uniform(*timeout)
    # Récupérer la position de l'élément
    box = await locator.bounding_box()
    if not box:
        raise Exception("Élément introuvable")

    target_y = box["y"]
    current_y = await page.evaluate("() => window.scrollY")

    step_distance = (target_y - current_y) / step

    for _ in range(step):
        current_y += step_distance
        await page.evaluate(f"window.scrollTo(0, {current_y})")
        
        await asyncio.sleep(timeout/100)  # ralentit le défilement

    # S'assurer que l'élément est visible
    await locator.scroll_into_view_if_needed()

def read_content(path_text) : 
    if not os.path.exists(path_text):
        raise Exception("pas de fichier portant ce nom ")
    with open(path_text, "r", encoding="utf-8") as f:
        contenu = f.read()
        return contenu


async def get_content(path_text):
    content  = read_content(path_text)
    #ask chat_gpt
    
    
async def check_url(page):
    await page.wait_for_load_state("domcontentloaded")
    if 'https://www.google.com/sorry/index?continue' in page.url:
        await page.wait_for_function(
            "() => window.location.href.includes('https://www.google.com/search')"
        )
        await page.wait_for_load_state("domcontentloaded")
        



if __name__ == "__main__":
    PROFILE_PATH = "./playwright_profile" 
    # ton code ici
    proxies = {
        "server":"brd.superproxy.io:33335",
        "username":"brd-customer-hl_1844e337-zone-mazar_zone",
        "password":"xkp6rpqbu370"
    }
    url =generate_google_search_url("mazars")
    print(url)
    #url  = "http://www.google.com/recaptcha/api2/demo"
    asyncio.run(runChrome(url ,proxies))