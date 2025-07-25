import random
import asyncio
from get_content_of_one_page import main_function
from GPT import GPT_ask
class Utils : 
    def __init__(self , page):
        self.page = page
        self.gpt = GPT_ask()
    async def main_loop_for_list_url(self, counter:int |None=None):
        list_hrefs  = []
        while(True):
            await self.check_url()
            hrefs = await self.get_list_link()
            list_hrefs.extend(hrefs)
            if counter  and len(list_hrefs)>= counter:
                break
            is_next_page_exist =await self.change_page()
            if not  is_next_page_exist : 
                break
        return list_hrefs
        
        
    async def check_url(self):
        await self.page.wait_for_load_state("domcontentloaded")
        if self.page.url.startswith('https://www.google.com/sorry/index?continue'):
            await self.page.wait_for_function(
                "() => window.location.href.startsWith('https://www.google.com/search')", timeout = 0
            )
            await self.page.wait_for_load_state("domcontentloaded")
            
    
    async def get_list_link(self):
        selector = 'div[role="main"] span > a'
        try :
            await self.page.wait_for_selector(selector, timeout=3000)
            list_link = await self.page.query_selector_all(selector)
            
            hrefs = []
            for link in list_link:
                href = await link.get_attribute("href")
                if href and "linkedin" in href:
                    hrefs.append(href)
                    
            return hrefs
        except Exception as e : 
            return []
        
    async def change_page(self):
        selector = 'div[role="main"] a#pnnext.LLNLxf'
        try:
            # Attend que le bouton "suivant" soit présent (timeout = 10s)
            await self.page.wait_for_selector(selector, timeout=10000)
            next_button1 = self.page.locator(selector)
            next_button = await self.page.query_selector(selector)
            if next_button:
                await self.smooth_scroll_to_element(locator=next_button1)
                await next_button.click()
                # Pause aléatoire entre 5 et 20 secondes
                await self.page.wait_for_timeout(random.uniform(5, 20) * 1000)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    async def smooth_scroll_to_element(self, locator, steps=[5,9], timeout=[5, 10]):
        step =int(random.uniform(*steps)*10)
        timeout = random.uniform(*timeout)
        box = await locator.bounding_box()
        if not box:
            raise Exception("Élément introuvable")
        target_y = box["y"]
        current_y = await self.page.evaluate("() => window.scrollY")
        step_distance = (target_y - current_y) / step

        for _ in range(step):
            current_y += step_distance
            await self.page.evaluate(f"window.scrollTo(0, {current_y})")
            
            await asyncio.sleep(timeout/100)  
        await locator.scroll_into_view_if_needed()

    async def main_loop(self):
        await self.check_url()
        #hrefs = await get_list_link(page)


    async def main_loop_for_list_url_with_access(self, compagny:str , counter:int |None=None):
        list_hrefs  = []
        while(True):
            await self.check_url()
            hrefs = await self.get_list_link()
            list_hrefs.extend(hrefs)
            for link in hrefs : 
                await self.access_linkdin_profil(href=link , compagny= compagny)
            if counter  and len(list_hrefs)>= counter:
                break
            is_next_page_exist =await self.change_page()
            if not  is_next_page_exist : 
                break
        return list_hrefs
    
    async def access_linkdin_profil(self , href , compagny) : 
        await main_function(search_url=href , gpt= self.gpt  ,compagny= compagny, page =self.page )
        await asyncio.sleep(random.uniform(20,30))