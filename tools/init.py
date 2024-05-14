from selenium import webdriver
from time import sleep


def init(url, headless=False):
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.add_argument('--start-maximized')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)
    return driver
