from selenium.webdriver.common.by import By
import pandas as pd
import requests
import os
import re


class Page:

    def __init__(self, driver):
        self.driver = driver

    def click(self, element, mode):
        element = self.get(element, mode)
        element.click()

    def set(self, element, mode, text):
        element = self.get(element, mode)
        element.clear()
        element.send_keys(text)
        assert element.get_property('value') == text

    def get(self, element, mode):
        element = self.driver.find_element(mode, element)
        if mode == By.ID:
            return element
        return element

    def getAll(self, element, mode):
        elements = self.driver.find_elements(mode, element)
        return elements

    def select(self, options):
        for i, option in enumerate(options):
            print(f'{i}- {option.text}')
        n = -1
        while n < 0 or n >= len(options):
            n = int(input('Seleccione una opción:'))
        return options[n]


class CIJ(Page):

    def __init__(self, driver):
        super(CIJ, self).__init__(driver)

    def getExpedientes(self):
        expedientes = self.getAll(element='result', mode=By.CLASS_NAME)
        return expedientes

    def scrapeExpedientes(self, expedientes):
        lista = list()
        for expediente in expedientes:
            data = self.getData(expediente)
            link = self.getLink(expediente)
            data['link'] = link
            lista.append(data)
        dataframe = pd.DataFrame(lista)
        return dataframe

    def getData(self, expediente):
        data = expediente.find_elements(By.TAG_NAME, 'li')
        dictionary = dict()
        for li in data:
            span = li.find_element(By.TAG_NAME, 'span')
            spanText = span.text
            text = li.text.replace(spanText, '')
            spanText = spanText.replace(':', '')
            dictionary[spanText] = text
        return dictionary

    def getLink(self, expediente):
        link = expediente.find_element(By.CLASS_NAME, 'download')
        link = link.get_attribute("href")
        return link

    def run(self):
        next = True
        dataframe = pd.DataFrame()
        while next:
            expedientes = self.getExpedientes()
            expedientes = self.scrapeExpedientes(expedientes)
            dataframe = pd.concat([dataframe, expedientes], ignore_index=True)
            next = self.next()

        self.toExcel(dataframe=dataframe)
        self.saveAll(expedientes=dataframe)

    def download(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f'Error al descargar el archivo desde {link}, status code: {response.status_code}')

    def save(self, carpeta, name, pdf):
        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear la ruta completa del archivo
        ruta_completa = os.path.join(carpeta, f'{name}.pdf')

        # Guardar el archivo PDF
        with open(ruta_completa, 'wb') as pdf_file:
            pdf_file.write(pdf)

        return True

    def filter(self, string):
        string = string.strip()
        string = re.sub(r'[^a-zA-Z0-9]', '-', string)
        return string

    def saveAll(self, expedientes):
        for index, expediente in expedientes.iterrows():
            link = expediente['link']
            caratula = expediente['Carátula']
            caratula = self.filter(caratula)
            tribunal = expediente['Tribunal']
            tribunal = self.filter(tribunal)
            path = f'descargas/{tribunal}'
            pdf = self.download(link)
            self.save(carpeta=path, name=caratula, pdf=pdf)

    def next(self):
        try:
            self.click(element='next', mode=By.CLASS_NAME)
            return True
        except Exception as e:
            return False

    def toExcel(self, dataframe):
        if not os.path.exists('descargas'):
            os.makedirs('descargas')
        dataframe.to_excel('descargas/resumen.xlsx', index=False)
