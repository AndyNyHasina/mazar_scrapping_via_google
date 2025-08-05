import asyncio
import random
import logging
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
from playwright_stealth import Stealth
import urllib.parse
import asyncio
from outil import Utils


# CONFIGURATION DU LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("linkedin_scraper.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

async def human_type(locator, text, delay_range=(0.05, 0.15)):
    for char in text:
        await locator.type(char)
        await asyncio.sleep(random.uniform(*delay_range))


async def runChrome(search_url: str, compagny:str , proxies=None):
    async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch_persistent_context(
                #proxy= proxies , 
                user_data_dir=PROFILE_PATH,
                slow_mo=100,
                headless=False,
                ignore_https_errors=True,

                ignore_default_args=['--enable-automation'],
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--ignore-certificate-errors",
                ],
                viewport={'width': 1366, 'height': 645},
                locale="en-US",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                )
            )

            await browser.add_init_script("""
                

                // Fausser languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ["fr-FR","en-US","fr","en"],
                });

                window.chrome = {
                    runtime: {},
                };

                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
                );

                // Empêcher WebGL detection (optionnel)
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {
                        return "Google Inc. (Intel)";
                    }
                    if (parameter === 37446) {
                        return "ANGLE (Intel, Intel(R) HD Graphics 5500 (0x00001616) Direct3D11 vs_5_0 ps_5_0, D3D11)";
                    }
                    return getParameter(parameter);
                };
                
                HTMLVideoElement.prototype.canPlayType = (type) => {
                    return "probably";
                };
            """)
            try:
                page = browser.pages[0] if browser.pages else await browser.new_page()
                util = Utils(page)

                logging.info("🌐 Navigation vers la page de recherche Google...")
                await page.goto(search_url, wait_until="networkidle", timeout=0)
                
                logging.info("🔄 Récupération des liens LinkedIn via util.main_loop_for_list_url_with_access...")
                hrefs = await util.main_loop_for_list_url_with_access(compagny=compagny)

                logging.info(f"🔗 Liens extraits : {hrefs}")
            except Exception as e:
                logging.error(f"❌ Erreur lors de la navigation ou extraction : {str(e)}", exc_info=True)
            finally:
                await browser.close()
                logging.info("🛑 Navigateur fermé proprement")

def generate_google_search_url(query: str, domain: str = "linkedin.com/in/") -> str:
    
    #full_query = f'site:{domain} "{query}"'
    encoded_query = urllib.parse.quote_plus(query)
    google_url = f"https://www.google.com/search?q={encoded_query}"
    return google_url


if __name__ == "__main__":
    PROFILE_PATH = "./playwright_profile" 
    proxy = {
        "server": "http://brd.superproxy.io:33335",
        "username" : "brd-customer-hl_fc29d462-zone-web_unlocker1",
        "password": "ku4mg0aw29yo"
    }
    url = generate_google_search_url(query="CEO orange linkedin" )
    
    asyncio.run(runChrome(search_url=url , compagny = "orange"))