from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import pandas as pd
import time
import os

basedir = os.path.dirname(__file__)


class IndeedBot():
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
        path_to_exe = os.path.join(
            basedir, "chromedriver.exe")
        self.srv = Service(path_to_exe)
        self.driver = webdriver.Chrome(
            service=self.srv, options=self.options)

    def recreate_driver(self):
        self.driver.quit()
        return webdriver.Chrome(
            service=self.srv, options=self.options)

    def run(self):
        next_btn = 'nextButton'
        search_bar = "ifl-InputFormField-3"  # ID
        search_btn = '//*[@id="main"]/div/div[1]/form/div/div[2]/button'
        campany_title = "css-1s5eo7v"
        base = "https://www.indeed.com"
        url = "https://www.indeed.com/companies"
        self.driver.get(url)
        time.sleep(5)
        s_b = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, search_bar)))
        s_b.send_keys(self.company)
        print("Located")
        # self.driver.find_element("id", search_bar)
        time.sleep(2)
        self.driver.find_element("xpath", search_btn).click()
        soup = bs(self.driver.page_source, 'html.parser')
        comp_url = soup.find_all(
            'a', href=True, class_=campany_title)[0]["href"]

        # Second Iteration
        self.driver = self.recreate_driver()
        self.driver.get(base + comp_url)
        time.sleep(2)
        soup = bs(self.driver.page_source, 'html.parser')
        comp_url = comp_url + "/reviews"
        # Third Iteration
        self.driver = self.recreate_driver()
        self.driver.get(base + comp_url)
        reviews = []
        while True and len(reviews) < self.data_number:
            try:
                soup = bs(self.driver.page_source, 'html.parser')
                reviews_p = soup.find_all(
                    "span", attrs={"itemprop": "reviewBody"})
                reviews_page = [x.text for x in reviews_p]
                reviews.extend(reviews_page)
                next_btn = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@title="Next"]')))
                next_btn.click()
                if reviews_page == []:
                    break
            except TimeoutException:
                break

        data = {"comment": reviews}
        df = pd.DataFrame(data)
        return df
