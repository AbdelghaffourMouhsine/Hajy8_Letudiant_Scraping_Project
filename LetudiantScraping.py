from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time 
import os
import zipfile

from EcoleStorage import EcoleStorage
from Ecole import Ecole

class LetudiantScraping:
    
    def __init__(self, url=None, region=None, proxy=None, with_selenium_grid=True, file_path=None):
        self.url = url
        self.region = region
        self.file_path = file_path
        self.proxy = proxy
        if self.proxy :
            self.PROXY_HOST = proxy["PROXY_HOST"] # rotating proxy or host
            self.PROXY_PORT = proxy["PROXY_PORT"] # port
            self.PROXY_USER = proxy["PROXY_USER"] # username
            self.PROXY_PASS = proxy["PROXY_PASS"] # password
            self.options = self.get_options_for_proxy()
        else:
            self.options = webdriver.ChromeOptions()
            
        self.with_selenium_grid = with_selenium_grid
        if self.with_selenium_grid:
            # IP address and port and server of the Selenium hub and browser options
            self.HUB_HOST = "localhost"
            self.HUB_PORT = 4444
            self.server = f"http://{self.HUB_HOST}:{self.HUB_PORT}/wd/hub"
            self.driver = webdriver.Remote(command_executor=self.server, options=self.options)
        else:
            self.driver = webdriver.Chrome(options=self.options)
            
        # self.start_scraping()
        

    def get_options_for_proxy(self):
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        
        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (self.PROXY_HOST, self.PROXY_PORT, self.PROXY_USER, self.PROXY_PASS)
        
        def get_chrome_options(use_proxy=True, user_agent=None):
            chrome_options = webdriver.ChromeOptions()
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'
        
                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            
            return chrome_options
        return get_chrome_options()
        
    def click_elem(self, click_elem):
        t=2
        check = 0
        i = 0
        while not check and i<5:
            try:
                click_elem.click()
                time.sleep(t) ######
                check = 1
            except Exception as e:
                check = 0
            i += 1
            
    def start_scraping(self):
        try:
            self.driver.get(self.url)
            time.sleep(2)

            button_accept_all = self.get_element('/html/body/div[16]/div[2]/div/div/div[3]/div/div/div[2]/div/button[2]')
            if button_accept_all["status"]:
                button_accept_all = button_accept_all["data"]
                button_accept_all.click()
            else:
                button_accept_all = self.get_element('//*[@id="sd-cmp"]/div[2]/div/div/div[3]/div/div/div[2]/div/button[2]')
                if button_accept_all["status"]:
                    button_accept_all = button_accept_all["data"]
                    button_accept_all.click()

            input_search_region = self.get_element("/html/body/div[10]/section[3]/div/div[1]/form/div[1]/div[2]/div/div/input[1]")
            if input_search_region["status"]:
                input_search_region = input_search_region["data"]
                input_search_region.send_keys(self.region)
            else:
                return {"status": False, "data":input_search_region["data"] }

            time.sleep(2)
            # for some regions #################################################################################################################
            # choise_button = self.get_element("/html/body/div[10]/section[3]/div/div[1]/form/div[1]/div[2]/div/div/div[2]/ul/li[1]")
            # if choise_button["status"]:
            #     choise_button = choise_button["data"]
            #     self.click_elem(choise_button)
            # else:
            #     return {"status": False, "data":choise_button["data"] }
                
            search_button = self.get_element("/html/body/div[10]/section[3]/div/div[1]/form/div[1]/div[3]/button")
            if search_button["status"]:
                search_button = search_button["data"]
                self.click_elem(search_button)
            else:
                return {"status": False, "data":search_button["data"] }
                
            time.sleep(1)
            stop = False
            i=0
            while not stop :
                i+=1
                current_url = str(self.driver.current_url).strip()
                print(current_url)
                result = self.get_ecoles()
                pagination_li_s = self.get_element("/html/body/div[10]/section[5]/div[2]/div/ul/li", group=True)
                if pagination_li_s["status"]:
                    pagination_li_s = pagination_li_s["data"]
                    if len(pagination_li_s)>0:
                        pagination_li_a = self.get_element("a",from_elem=pagination_li_s[-1])
                        if pagination_li_a["status"]:
                            pagination_li_a = pagination_li_a["data"]
                            url = str(pagination_li_a.get_attribute("href")).strip()
                            if url == current_url:
                                stop = True
                            else:
                                self.driver.get(url)
                                time.sleep(2)
                        else:
                            stop = True
                    else:
                        print(f'/'*150)
                        print(i+1)
                        print(f'\\'*150)
                else:
                    print(f'/'*150)
                    print(i+1)
                    print(f'\\'*150)
                
            print('3333333333')
            
            
            # return {"status": True, "data": result }
            
        except Exception as e:
            print(f"Error : {e}")
            return {"status": False, "data": str(e) }
        finally :
            self.driver.quit()
            
    def get_element(self, path_to_elem, class_=None, group=False, from_elem=None):
        i = 0
        while i<5:
            try:
                if not class_:
                    if not from_elem:
                        if not group:
                            elem = self.driver.find_element(By.XPATH, path_to_elem)
                        else :
                            elem = self.driver.find_elements(By.XPATH, path_to_elem)
                        return {"status": True, "data":elem }
                    else:
                        if not group:
                            elem = from_elem.find_element(By.XPATH, path_to_elem)
                        else :
                            elem = from_elem.find_elements(By.XPATH, path_to_elem)
                        return {"status": True, "data":elem }
                        
            except Exception as e:
                i += 1
                if i == 5:
                    return {"status": False, "data":str(e) }

    def extract_ecole(self, div_ecole):
        ecole = Ecole()
        a_title = self.get_element('div/div/a', from_elem=div_ecole)
        if a_title["status"]:
            a_title = a_title["data"]
            ecole.ecole_name = a_title.text
            ecole.ecole_more_inf_url = a_title.get_attribute("href")
        else:
            return {"status": False, "data":a_title["data"] }
        
        ecole_title = self.get_element('div/h3', from_elem=div_ecole)
        if ecole_title["status"]:
            ecole_title = ecole_title["data"]
            ecole.ecole_title = ecole_title.text

        exist_star_elem = False
        ecole_ville = self.get_element('div/div[2]', from_elem=div_ecole)
        if ecole_ville["status"]:
            ecole_ville = ecole_ville["data"]
            if ecole_ville.get_attribute("class")  == "tw-py-2":
                ecole.ecole_ville = ecole_ville.text
            else:
                exist_star_elem = True
                ecole_ville = self.get_element('div/div[3]', from_elem=div_ecole)
                if ecole_ville["status"]:
                    ecole_ville = ecole_ville["data"]
                    if ecole_ville.get_attribute("class")  == "tw-py-2":
                        ecole.ecole_ville = ecole_ville.text
                        
        if not exist_star_elem :
            ecole_voir_la_fiche_url = self.get_element('div/div[3]/div/a', from_elem=div_ecole)
        else:
            ecole_voir_la_fiche_url = self.get_element('div/div[4]/div/a', from_elem=div_ecole)
            
        if ecole_voir_la_fiche_url["status"]:
            ecole_voir_la_fiche_url = ecole_voir_la_fiche_url["data"]
            ecole.ecole_voir_la_fiche_url = ecole_voir_la_fiche_url.get_attribute("href")
            
        return {"status": True, "data": ecole }
        
                
    def get_ecoles(self):
        divs_ecoles = self.get_element('/html/body/div[10]/section[4]/div/div[1]/div', group=True)
        if divs_ecoles["status"]:
            divs_ecoles = divs_ecoles["data"]
            ecoles_list = []
            for div_ecoles in divs_ecoles:
                ecole = self.extract_ecole(div_ecoles)
                if ecole['status']:
                    # print(ecole['data'])
                    ecole['data'].ecole_region = self.region
                    ecoles_list.append(ecole['data'])

            ecoleStorage = EcoleStorage(self.file_path)
            ecoleStorage.insert_ecoles(ecoles_list)
            ecoleStorage.close_file()
            print(f"*"*150)
            print('le nombre des ecoles est : ',len(ecoles_list))
            return {"status": True, "data": ecoles_list}
        else:
            return {"status": False, "data":divs_ecoles["data"] }

    def start_scraping_more_info(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
             )
        time.sleep(2)

        button_accept_all = self.get_element('/html/body/div[16]/div[2]/div/div/div[3]/div/div/div[2]/div/button[2]')
        if button_accept_all["status"]:
            button_accept_all = button_accept_all["data"]
            button_accept_all.click()
        else:
            button_accept_all = self.get_element('//*[@id="sd-cmp"]/div[2]/div/div/div[3]/div/div/div[2]/div/button[2]')
            if button_accept_all["status"]:
                button_accept_all = button_accept_all["data"]
                button_accept_all.click()
            
        ecole = Ecole()
        section_contact_divs = self.get_element('//*[@id="presentation"]/section/div/div[1]/div/div', group=True)
        if section_contact_divs["status"]:
            section_contact_divs = section_contact_divs["data"]
            # print(len(section_contact_divs))
            for contact_div in section_contact_divs:
                i_elem = self.get_element('i', from_elem=contact_div)
                if i_elem["status"]:
                    i_elem = i_elem["data"]
                    #print(i_elem.get_attribute("class"))
                    if 'map-marker' in i_elem.get_attribute("class"):
                        ecole.ecole_address = contact_div.text
                    else:
                        if 'phone' in i_elem.get_attribute("class"):
                            ecole.ecole_phone = contact_div.text
                        else:
                            if 'paper-plane' in i_elem.get_attribute("class"):
                                ecole.ecole_email = contact_div.text
                                
        
        section_contact = self.get_element('//*[@id="presentation"]/section')
        if section_contact["status"]:
            section_contact = section_contact["data"]
            section_contact_a_s = self.get_element('//*[@title="Site web de l\'établissement"]', from_elem=section_contact)
            if section_contact_a_s["status"]:
                section_contact_a_s = section_contact_a_s["data"]
                ecole.ecole_web_site_url = section_contact_a_s.get_attribute("href")

        presentation_divs = self.get_element('//*[@id="presentation"]/div', group=True)
        if presentation_divs["status"]:
            presentation_divs = presentation_divs["data"]
            for div in presentation_divs:
                if 'Comment contacter' in div.text:
                    div_contact = self.get_element('div[2]/div/p', from_elem=div)
                    if div_contact["status"]:
                        div_contact = div_contact["data"]
                        ecole.ecole_comment_contacter = div_contact.get_attribute("textContent")
                                
            return {"status": True, "data": ecole}
        else:
            return {"status": False, "data":section_contact_divs["data"] }