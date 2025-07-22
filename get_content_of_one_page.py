import asyncio
import random
from playwright.async_api import async_playwright
from controller import GPT_ask
async def runChrome(search_url: str, gpt:GPT_ask ,proxies=None  ):
    async with async_playwright() as p:
    
        context = await p.chromium.launch_persistent_context(
            user_data_dir="test",
            
            headless=False,
            ignore_default_args=['--enable-automation'],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",

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

        await page.goto('https://fr.linkedin.com/in/christophe-mazars-b7a20a30', wait_until="domcontentloaded", timeout=0 ,referer="https://www.google.com")
        await load_dom(page , gpt)
        input("")


async def load_dom(page, gpt ):
    selector ='section.profile'
    await page.wait_for_load_state('domcontentloaded')

    profile = await page.query_selector(selector)
    if not  profile : 
        raise Exception('pas de section profile')
    content_html = await profile.inner_text()
    gpt_response = ask_gpt(gpt= gpt  ,  content_linkedin= content_html)
    print(gpt_response)
    print("fini")

def ask_gpt(gpt:GPT_ask , content_linkedin):
    texte = f"Le contenu du profil LinkedIn ici :\" {content_linkedin} \""
    return gpt.conversation(texte)
    

        
if __name__ == "__main__":
    gpt = GPT_ask()
    asyncio.run(runChrome(search_url='url' ,proxies='proxies' , gpt=gpt))
