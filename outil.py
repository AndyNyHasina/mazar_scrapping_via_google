import random
import asyncio
import logging
from get_content_of_one_page import main_function
from GPT import GPT_ask
from Global_var import combinaison_choice
from extra_utils import write_manifest_file
logger = logging.getLogger(__name__)  
class Utils : 
    def __init__(self, page):
        self.page = page
        self.gpt = GPT_ask()
        self.init_value()
        

        
    async def main_loop_for_list_url(self, counter: int | None = None):
        list_hrefs = []
        while True:
            await self.check_url()
            hrefs = await self.get_list_link()
            list_hrefs.extend(hrefs)
            logging.info(f"🔗 {len(hrefs)} liens extraits (total: {len(list_hrefs)})")

            if counter and len(list_hrefs) >= counter:
                break
            is_next_page_exist = await self.change_page()
            if not is_next_page_exist:
                break
        return list_hrefs
        
    

    async def check_url(self):
        await self.page.wait_for_load_state("domcontentloaded")
        if self.page.url.startswith('https://www.google.com/sorry/index?continue'):
            logging.warning("⚠️ Redirection vers la page CAPTCHA détectée. Attente du retour à la recherche...")
            self.check_text_captcha_google()
            await self.page.wait_for_function(
                "() => window.location.href.startsWith('https://www.google.com/search')", timeout=0
            )
            await self.page.wait_for_load_state("domcontentloaded")
            logging.info("✅ Retour sur la page de recherche Google")
            
    
    async def get_list_link(self):
        selector = 'div[role="main"] span > a'
        try:
            await self.page.wait_for_selector(selector, timeout=3000)
            list_link = await self.page.query_selector_all(selector)

            hrefs = []
            for link in list_link:
                href = await link.get_attribute("href")
                if href and "linkedin" in href:
                    hrefs.append(href)

            return hrefs
        except Exception as e:
            logging.error("❌ Erreur pendant l’extraction des liens : ", exc_info=True)
            return []
        
        
    async def change_page(self):
        selector = 'div[role="main"] a#pnnext.LLNLxf'
        try:
            await self.page.wait_for_selector(selector, timeout=10000)
            next_button1 = self.page.locator(selector)
            next_button = await self.page.query_selector(selector)
            if next_button:
                await self.smooth_scroll_to_element(locator=next_button1)
                await next_button.click()
                delay = random.uniform(5, 20)
                logging.info(f"➡️ Page suivante... Attente {delay:.2f}s")
                await self.page.wait_for_timeout(delay * 1000)
                return True
            else:
                logging.info("⛔️ Fin de pagination (pas de bouton suivant)")
                return False
        except Exception as e:
            logging.warning("⚠️ Pas de bouton suivant trouvé ou erreur", exc_info=True)
            return False
        

        
    async def smooth_scroll_to_element(self, locator, steps=[5, 9], timeout=[5, 10]):
        step = int(random.uniform(*steps) * 10)
        delay = random.uniform(*timeout)
        box = await locator.bounding_box()
        if not box:
            raise Exception("Élément introuvable")
        target_y = box["y"]
        current_y = await self.page.evaluate("() => window.scrollY")
        step_distance = (target_y - current_y) / step

        for _ in range(step):
            current_y += step_distance
            await self.page.evaluate(f"window.scrollTo(0, {current_y})")
            await asyncio.sleep(delay / 100)
        await locator.scroll_into_view_if_needed()
        logging.info("🧭 Scroll effectué vers l'élément ciblé")


    async def main_loop(self):
        await self.check_url()
        #hrefs = await get_list_link(page)



    
    async def main_loop_for_list_url_with_access(self, compagny: str, counter: int | None = None):
        list_hrefs = []
        while True:
            await self.check_url()
            hrefs = await self.get_list_link()
            list_hrefs.extend(hrefs)
            logging.info(f"🔎 Traitement de {len(hrefs)} profils LinkedIn")

            for link in hrefs:
                if len(self.combinaison_choice) == 0:
                    self.init_value()
                index = random.choice(self.combinaison_choice)
                self.combinaison_choice.remove(index)
                await self.access_linkdin_profil(href=link, compagny=compagny, index=index)

            if counter and len(list_hrefs) >= counter:
                break
            is_next_page_exist = await self.change_page()
            if not is_next_page_exist:
                break
        return list_hrefs
    

        
    async def access_linkdin_profil(self, href, compagny, index):
        logging.info(f"➡️ Accès au profil : {href} (index combinaison: {index})")
        try:
            await main_function(search_url=href, gpt=self.gpt, compagny=compagny, page=self.page, index=index)
            await asyncio.sleep(random.uniform(20, 30))
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'accès au profil {href} : {str(e)}", exc_info=True)
    
    def init_value(self):
        self.combinaison_choice = combinaison_choice
        
        
        
    async def check_text_captcha(self):
        selector_bouton = "input[type='submit']"
        selector_text = "input[type='text']"
        selector_textarea = "textarea"
        selector_img = 'form img'

        await self.page.wait_for_load_state("domcontentloaded")

        has_bouton = await self.page.locator(selector_bouton).count() > 0
        has_text = await self.page.locator(selector_text).count() > 0
        has_textarea = await self.page.locator(selector_textarea).count() > 0
        has_img = await self.page.locator(selector_img).count() > 0

        if has_bouton and (has_text or has_textarea):
            if not has_img:
                raise Exception("❌ CAPTCHA texte détecté mais pas d'image trouvée.")

            input_selector = selector_text if has_text else selector_textarea

            write_manifest_file(
                image_selector=selector_img,
                text_selector=input_selector
            )

            await self.page.reload()
            await self.page.wait_for_selector(input_selector)

            await self.page.wait_for_function(
                f"() => document.querySelector('{input_selector}').value.length > 0",
                timeout=30000
            )

            await self.page.locator(selector_bouton).click()
            print("✅ CAPTCHA texte rempli et envoyé automatiquement.")
        else:
            print("❌ Aucun CAPTCHA texte détecté")


    async def check_text_captcha_google(self):
        selector_bouton = "input[type='submit']"
        selector_text = "#captcha"
        selector_img = '#captcha-form img'

        await self.page.wait_for_load_state("domcontentloaded")

        has_bouton = await self.page.locator(selector_bouton).count() > 0
        has_text = await self.page.locator(selector_text).count() > 0
        has_img = await self.page.locator(selector_img).count() > 0

        if has_bouton and has_text and has_img:
            input_selector = selector_text 

            write_manifest_file(
                image_selector=selector_img,
                text_selector=input_selector
            )

            await self.page.reload()
            await self.page.wait_for_selector(input_selector)

            await self.page.wait_for_function(
                f"() => document.querySelector('{input_selector}').value.length > 0",
                timeout=30000
            )

            await self.page.locator(selector_bouton).click()
            print("✅ CAPTCHA texte rempli et envoyé automatiquement.")
