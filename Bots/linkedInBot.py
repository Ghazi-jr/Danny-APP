from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup as bs
import os

basedir = os.path.dirname(__file__)

class LinkedInBot():
    def __init__(self, keyword, data_number):
        self.data_number = data_number
        ### input company name ###
        self.company_name = keyword
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        path_to_exe = os.path.join(
            basedir, "Bots", "chromedriver.exe")
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            executable_path=path_to_exe, options=self.options)

    def run(self):
        email = "hannalilya14@gmail.com"
        password = "Hafedh14"
        self.driver.get("https://www.linkedin.com")
        sleep(5)
        login_form_email = self.driver.find_element(By.ID, 'session_key')
        sleep(5)
        login_form_email.send_keys(email)
        sleep(5)
        login_form_password = self.driver.find_element(
            By.ID, 'session_password')
        sleep(5)
        login_form_password.send_keys(password)
        sleep(5)
        submit = self.driver.find_element(
            By.CLASS_NAME, 'sign-in-form__submit-button')
        submit.click()
        sleep(10)
        try:
            skip = self.driver.find_element(By.CLASS_NAME, 'secondary-action')
            skip.click()
        except:
            print('-------- no add phone number screen ----------- ')
        sleep(15)
        search = self.driver.find_element(
            By.XPATH, '/html/body/div[5]/header/div/div/div/div[1]/input')
        search.send_keys(self.company_name)
        search.send_keys(Keys.ENTER)

        sleep(8)
        see_all_posts_results = self.driver.find_element(
            By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[4]/div[2]/a')
        see_all_posts_results.click()
        sleep(8)
        ### scrolling ###
        print('-----------scrolling-------------')
        try:
            scroll_pause_time = 3
            screen_height = self.driver.execute_script(
                "return window.screen.height;")
            i = 1
            j = 0
            while True:
                # scroll one screen height each time
                self.driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = self.driver.execute_script(
                    "return document.body.scrollHeight;")
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if (screen_height) * i > scroll_height:
                    break
                if (j > 80):
                    break
                j += 1
        except:
            print('---------- reached all posts ----------')
        # loading more comments
        sleep(10)
        i = 0
        print('-----------loading more-------------')
        comments = []
        while i != 2:
            load_more = self.driver.find_elements(
                By.CLASS_NAME, 'comments-comments-list__load-more-comments-button ')
            print(load_more)
            for button in load_more:
                try:
                    button.click()
                    print('-----------clicked sucessfully------------')
                    sleep(3)
                except:
                    pass
            i += 1
        soup = bs(self.driver.page_source, 'html.parser')
        comment = soup.find_all(
            "span", attrs={"dir": "ltr"})
        comment = [x.text for x in comment]
        comments.extend(comment)
        data = {"comment": comments}
        df = pd.DataFrame(data)
        self.driver.close()
        return df
        