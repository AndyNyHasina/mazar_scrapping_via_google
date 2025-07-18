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

async def mirindra(page):
    search = page.locator('textarea[role="combobox"]')
    await search.click()
    await human_type(search, "Andy Ny Hasina ANDRIAMBOAHANGY")
    await search.press("Enter")
    input('📌 Appuie sur Entrée pour quitter...')

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

        #await page.goto(search_url, wait_until="networkidle", timeout=0)
        await page.goto("https://www.google.com/recaptcha/api2/demo", wait_until="networkidle", timeout=0)
        input("")
        hrefs = await get_list_link(page)
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


async def check_capcha(page , browser , url , proxies): 
    if "https://www.google.com/sorry/" in page.url : 
        try :
            selector = 'div[data-sitekey][class="g-recaptcha"]'
            selector_capcha = await page.query_selector(selector)
            if not selector_capcha :
                return
            key =await selector_capcha.get_attribute("data-sitekey")
            if key : 
                print(key)
                token =  solve_recaptcha2(page , key)
                input('first')
                if token : 
                    await page.evaluate(
            """(token) => { document.querySelector('#g-recaptcha-response').value = token; }""",
            token
        )
        except Exception as e  : 
            print(e)
            await browser.close()
            


async def get_list_link(page):
    selector = 'div[role="main"] span > a'
    await page.wait_for_selector(selector, timeout=15000)
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