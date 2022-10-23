from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import os

basedir = os.path.dirname(__file__)


class GlassdoorBot():
    def __init__(self, company, data_number):
        self.company = company
        self.data_number = data_number
        self.options = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--headless')
        self.options.add_argument(f'user-agent={user_agent}')
        self.path = os.path.join(
            basedir, "chromedriver.exe")
        self.srv = Service(self.path)
        self.driver = webdriver.Chrome(
            service=self.srv, options=self.options)

    def Remove_popup(self, driver):
        popup_close = 'Close'
        try:
            popup = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, popup_close)))
            print("Popup Found")
            popup.close()
        except TimeoutException:
            print("Popup not found ")
            pass

    def recreate_driver(self):
        self.driver.quit()
        self.srv = Service(self.path)
        return webdriver.Chrome(
            service=self.srv, options=self.options)

    def run(self):
        url = "https://www.glassdoor.com/companies"
        next_btn = 'nextButton'
        search_bar = "sc.keyword"  # ID
        search_btn = "gd-ui-button"
        campany_title = "company-tile"
        base = "https://www.glassdoor.com"
        reviews_btn = 'e16bqfyh1'

        self.driver.get(url)
        print("Searching For company......")
        # Remove_popup(driver)
        s_b = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, search_bar)))
        s_b.send_keys(self.company)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, search_btn).click()

        soup = bs(self.driver.page_source, 'html.parser')
        comp_url = soup.find_all(
            'a', href=True, class_=campany_title)[0]["href"]

        self.driver = self.recreate_driver()
        print("redirecting to company........")
        print(comp_url)
        self.driver.get(base + comp_url)
        # Remove_popup(driver)

        soup = bs(self.driver.page_source, 'html.parser')
        comp_url = soup.find_all(
            'a', href=True, class_=reviews_btn)[0]["href"]
        base_comp_url = comp_url

        reviews_pros = []
        reviews_cons = []
        i = 1
        print("starting reviews scraping......")
        j = 1
        while j < 10 and len(reviews_pros) + len(reviews_cons) < self.data_number:
            self.driver = self.recreate_driver()
            self.driver.get(base + comp_url)
            # Remove_popup(driver)
            soup = bs(self.driver.page_source, 'html.parser')
            reviews_p = soup.find_all(
                "span", attrs={"data-test": "pros"})
            reviews_c = soup.find_all(
                "span", attrs={"data-test": "cons"})
            reviews_p = [x.text for x in reviews_p]
            reviews_c = [x.text for x in reviews_c]
            reviews_pros.extend(reviews_p)
            reviews_cons.extend(reviews_c)
            i += 1
            comp_url = base_comp_url.strip('.html')
            comp_url = comp_url + "_P" + str(i)
            comp_url = comp_url + ".htm"
            j += 1
            if reviews_p == [] and reviews_c == []:
                break

        reviews = reviews_pros + reviews_cons

        data = {"comment": reviews}
        df = pd.DataFrame(data)
        return df
