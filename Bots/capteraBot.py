from xml.etree.ElementTree import Comment
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

basedir = os.path.dirname(__file__)


class CapterraBot:
    def __init__(self, keyword, data_number):
        self.data_number = data_number
        path_to_exe = os.path.join(
            basedir, "Bots", "chromedriver.exe")
        self.options = uc.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        # self.options.add_argument('--headless')
        self.options.add_argument("--enable-javascript")
        self.options.add_argument(f'user-agent={user_agent}')
        self.company_name = keyword
        self.driver = uc.Chrome(
            executable_path=path_to_exe, options=self.options)

    def recreate_driver(self):
        self.driver.quit()
        self.options = uc.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        # self.options.add_argument('--headless')

        self.options.add_argument("--enable-javascript")
        self.options.add_argument(f'user-agent={user_agent}')
        return uc.Chrome(
            executable_path='./Bots/chromedriver.exe', options=self.options)

    def run(self):
        pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        reviewws = []
        # driver.request_interceptor = interceptor
        self.driver.get('https://www.capterra.com/')
        sleep(3)
        self.driver.get('https://www.capterra.com/')

        sleep(15)
        search = self.driver.find_element(
            By.CSS_SELECTOR, '#inline-search > form > div.nb-input-wrap.nb-flex-1.nb-overflow-hidden > input')
        sleep(2)
        search.send_keys(self.company_name)
        search.send_keys(Keys.ENTER)
        sleep(3)
        url = self.driver.current_url
        self.driver = self.recreate_driver()
        self.driver.get(url)
        sleep(5)
        company = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/a').get_attribute('href')
        sleep(5)
        self.driver = self.recreate_driver()
        self.driver.get(company)
        sleep(5)
        reviews = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div/ul/li[6]/a')
        reviews.click()
        sleep(2)
        url = self.driver.current_url
        self.driver = self.recreate_driver()
        self.driver.get(url)
        sleep(5)
        read_all = self.driver.find_element(
            By.XPATH, '//*[@id="LoadableReviewSectionForSpotlight"]/div/div[3]/div/div[1]/a[2]').get_attribute('href')

        self.driver = self.recreate_driver()
        self.driver.get(read_all)
        sleep(30)
        j = 0
        try:
            url = self.driver.current_url
            self.driver = self.recreate_driver()
            self.driver.get(url)
            sleep(20)
            while j < 5:
                self.driver.find_element(
                    By.CSS_SELECTOR, '.nb-button .nb-button-standard .nb-button-primary .nb-w-full .md:nb-w-auto .nb-my-3xs .nb-text-md .nb-py-2xs .nb-pr-sm .nb-pl-md').click()
                j += 1
                sleep(20)
        except:
            pass
        Comment = self.driver.find_elements(
            By.CSS_SELECTOR, '.nb-w-full .nb-h-auto')
        review = [x.text for x in Comment]
        reviewws.extend(review)
        self.driver.close()
        data = {"comment": reviewws}
        df = pd.DataFrame(data)
        return df
