from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os
from dotenv import load_dotenv
import xlrd
from selenium.webdriver.common.keys import Keys
import time


class beerMile:
    def __init__(self, event_url):
        load_dotenv()

        self.event_url = event_url
        self.login = os.getenv('LOGIN')
        self.password = os.getenv('PASSWORD')

    def add_participants(self):
        # authorization
        browser = webdriver.Firefox()
        browser.get(self.event_url)
        wait = WebDriverWait(browser, 12)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn')))

        login = browser.find_element_by_name('username')
        login.send_keys(self.login)

        password = browser.find_element_by_name('password')
        password.send_keys(self.password)

        login_button.click()

        # home page
        continue_link = browser.find_element_by_link_text('Edit')
        continue_link.click()

        # event edit page
        event_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn')))
        event_btn.click()

        # edit entries
        participants_data = self.extraction_excel()

        for counter, participant in enumerate(participants_data):
            add_racers_button = wait.until(EC.element_to_be_clickable((By.ID, 'add_entry')))
            span = browser.find_element_by_id(f'container_select_{counter}_msdd')
            span.click()

            smth = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                f'/html/body/div[1]/section/div/div[1]'
                                                                                f'/form/table/tbody/tr[{counter + 2}]'
                                                                                f'/td[5]/div[2]'
                                                                                f'/div[2]/ul/li[2]'
                                                                                )))

            smth.click()

            first_name = browser.find_element_by_name(f'first_name_{counter}')
            first_name.send_keys(participant[0])

            last_name = browser.find_element_by_name(f'last_name_{counter}')
            last_name.send_keys(participant[1])

            beer = browser.find_element_by_css_selector(f'input.beer_input[name=beer_{counter}]')
            beer.send_keys('Волковская')

            add_racers_button.click()

    @staticmethod
    def extraction_excel(file_name="Beer_mile.xlsx"):
        excel_file = xlrd.open_workbook(file_name)
        sheet = excel_file.sheet_by_index(0)

        num_row = sheet.col(0)
        inf_part = []

        for i in range(2, len(num_row)):
            buf = sheet.row(i)
            buf_str = []
            for j in range(1, len(buf) - 3):
                buf_str.append(str(buf[j]).replace("text:", "").replace("empty:", "").replace("'", ""))

            if buf_str[3] != '':
                inf_part.append(buf_str)

        return inf_part


if __name__ == '__main__':
    beerMile = beerMile('https://www.beermile.com/?action=edit_entries&id=151671')
    beerMile.add_participants()
