from selenium.webdriver.common.by import By


def selectOption(select, options, n=None):
    # Elimina la primera opcion que es un titulo
    optionList = [option.text for option in options][1:]
    n = -1 if n is None else n
    if n == -1:
        print(optionList)
        for i, option in enumerate(optionList):
            print(f'{i}- {option}')
        while n < 0 or n >= len(optionList):
            n = int(input('Seleccione una opción:'))
    select.click()
    for option in options:
        if option.text == optionList[n]:
            option.click()
            assert option.is_selected()
            print(f'Ha seleccionado la opción: {option.text}')
            break


def completeInput(inputText, text, title):
    if text is None:
        text = input(f'Ingrese un valor para {title}: ')
    inputText.send_keys(text)
    assert inputText.get_property('value') == text
    print(f'Se ha completado el valor {title} con {text}')


def selectJurisdiccion(select):
    options = select.find_elements(By.TAG_NAME, 'li')
    print(options)
