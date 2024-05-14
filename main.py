from tools.init import init
from Pages import CIJ


def main():
    driver = None
    try:
        url = 'https://www.cij.gov.ar/sentencias.html'
        driver = init(url, headless=False)
        input('Press enter to start')
        cij = CIJ(driver)
        cij.run()
    except Exception as e:
        print(e)
        driver.close()
        main()
    input('Enter to stop')
    driver.close()
    exit()


main()
