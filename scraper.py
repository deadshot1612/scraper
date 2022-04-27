from random import randint
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import bot, BASE_DIR

import pandas as pd

class Scraper:

    def __init__(self, uri, name,chat_id) -> None:
        self.uri = uri
        self.name = name
        self.id = chat_id
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def get_data(self):
        page = 1
        name = []
        contacts = []
        addresses = []
        licen_name = [] 
        work_hours = []
        while True: 
            self.driver.get(f'{self.uri}&Page={page}')
            sleep(randint(3,6))
            if self.driver.find_elements(by=By.XPATH, value="//td[@class='Name']"):
                print(page)
                articlies = self.driver.find_elements(by=By.XPATH, value="//td[@class='Name']")
                addresses_temp = self.driver.find_elements(by=By.XPATH, value="//td[@class='Address']")
                sleep(randint(4,5))

                for button in self.driver.find_elements(by=By.XPATH, value="//a[@class='btn-info']"):
                    sleep(randint(5,7))
                    button.click()
                for button in self.driver.find_elements(by=By.XPATH, value="//div[@class='comp_add_mode']/a"):
                    sleep(randint(3,6))
                    button.click()

                info = self.driver.find_elements(by=By.XPATH, value="//td[@class='Info']")

                for id in range(len(articlies)):
                    sleep(randint(3,6))
                    name.append(articlies[id].find_element(by=By.CLASS_NAME, value="orgName").text)
                    try:
                        licen_name.append(articlies[id].find_element(by=By.CLASS_NAME, value="Alt").text)
                    except:
                        licen_name.append(None)


                    try:
                            contacts.append(info[id].find_element(by=By.CLASS_NAME, value="phone-data").text)
                    except:
                            contacts.append(None)
                    addresses.append((addresses_temp[id].text).replace("посмотреть на карте схему проезда", ""))
                    try:    
                        work_hours.append(info[id].find_element(by=By.CLASS_NAME, value="operating_mode").text)
                    except:
                        work_hours.append(None)


 
                page += 1
                
            else:
                try:
                    df = pd.DataFrame({'Название заведения': name, 'Юридическое название,': licen_name,'Контактные номера': contacts, 'Адрес': addresses, "Режим работы": work_hours})

                    writer = pd.ExcelWriter(f'{BASE_DIR}/media/{self.name}.xlsx', engine='xlsxwriter')

                    df.to_excel(writer, sheet_name='Page1')

                    for column in df:
                        column_length = max(df[column].astype(str).map(len).max(), len(column))
                        col_idx = df.columns.get_loc(column)
                        writer.sheets['Page1'].set_column(col_idx, col_idx, column_length)
                    writer.save()
                    with open(f'{BASE_DIR}/media/{self.name}.xlsx', 'rb') as f:
                        bot.send_document(self.id, f)
                except:
                    bot.send_message(self.id, "Something Wrong! Is Link is correct?")
                self.driver.quit()  
                break

