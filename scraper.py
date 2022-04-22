from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class Scraper:

    def __init__(self, uri, name) -> None:
        self.uri = uri
        self.name = name
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--lang=eng")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def get_data(self):
        self.driver.get(self.uri)
        page = 1
        sleep(randint(3,6))
        name = []
        contacts = []
        addresses = []
        licen_name = [] 
        work_hours = []
        while True:
            self.driver.get(f'{self.uri}&Page={page}')
            if self.driver.find_elements(by=By.XPATH, value="//td[@class='Name']"):
                articlies = self.driver.find_elements(by=By.XPATH, value="//td[@class='Name']")
                addresses_temp = self.driver.find_elements(by=By.XPATH, value="//td[@class='Address']")

                sleep(randint(4,5))
                for button in self.driver.find_elements(by=By.XPATH, value="//a[@class='btn-info']"):
                    sleep(randint(3,6))
                    button.click()
                for button in self.driver.find_elements(by=By.XPATH, value="//div[@class='comp_add_mode']/a"):
                    sleep(randint(3,6))
                    button.click()

                work_hours_data = self.driver.find_elements(by=By.XPATH, value="//div[@class='operating_mode']")
                numbers = self.driver.find_elements(by=By.XPATH, value="//div[@class='phone-data']")
                for id in range(len(articlies)):
                    sleep(randint(3,6))
                    name.append(articlies[id].find_element(by=By.CLASS_NAME, value="orgName").text)
                    try:
                        licen_name.append(articlies[id].find_element(by=By.CLASS_NAME, value="Alt").text)
                    except:
                        licen_name.append(None)

                    contacts.append(numbers[id].text)
                    addresses.append((addresses_temp[id].text).replace("посмотреть на карте схему проезда", ""))
                    work_hours.append(work_hours_data[id].text)

 
                page += 1
                
            else:

                df = pd.DataFrame({'Название заведения': name, 'Юридическое название,': licen_name,'Контактные номера': contacts, 'Адрес': addresses, "Режим работы": work_hours})

                writer = pd.ExcelWriter(f'{self.name}.xlsx', engine='xlsxwriter')

                df.to_excel(writer, sheet_name='Page1')

                for column in df:
                    column_length = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['Page1'].set_column(col_idx, col_idx, column_length)

                writer.save()
