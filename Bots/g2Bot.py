import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC

import os

basedir = os.path.dirname(__file__)


class G2BOT:
    def __init__(self, keyword, data_number):
        self.data_number = data_number
        path_to_exe = os.path.join(
            basedir, "Bots", "chromedriver.exe")
        options = uc.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--incognito')
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--no-sandbox')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        self.company = keyword
        self.company = self.company.replace(" ", "-")
        self.driver = uc.Chrome(executable_path=path_to_exe)

    def run(self):
        pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        reviewws = []
        self.driver.get(
            'https://www.g2.com/products/{}/reviews'.format(self.company))
        sleep(10)
        number = 2
        try:
            last = self.driver.find_element(
                By.XPATH, '//*[@id="reviews"]/div[2]/div[29]/ul/li[8]/a')
            self.driver.execute_script("arguments[0].click();", last)

            number = self.driver.find_element(
                By.XPATH, '//*[@id="reviews"]/div[2]/div[16]/ul/li[8]').text
            number = int(number)
        except:
            pass
        for page in range(1, number):
            while len(reviewws) < self.data_number:
                self.driver.get(
                    'https://www.g2.com/products/{}/reviews?page={}'.format(self.company, page))
                sleep(15)
                reviews = self.driver.find_elements(
                    By.CLASS_NAME, 'formatted-text')
                comment = [x.text for x in reviews]
                reviewws.extend(comment)
                sleep(20)
        self.driver.close()
        data = {"comment": reviewws}
        df = pd.DataFrame(data)
        return df
