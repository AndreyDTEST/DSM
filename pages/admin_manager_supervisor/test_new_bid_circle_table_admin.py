import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators
from conftest import NewBidLocators
from selenium.webdriver.common.by import By

def test_create_request(auth, auth_data):
    browser = auth
    role = auth_data["role"]

    # Проверяем, что авторизация прошла успешно
    assert "auth" not in browser.current_url

    # Кнопка "Создать заявку"
    create_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CREATE_NEW_BID_BUTTON))
    create_btn.click()

    # Радио-баттон "Круглый стол"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CIRCLE_TABLE))
    circle_table.click()

    # Кнопка "Создать заявку внутри модального окна"
    create_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CREATE_BUTTON))
    create_btn.click()

    # Кликаем на селект "Компания", чтобы открыть поле ввода
    company = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(NewBidLocators.COMPANY))
    company.click()

    # Находим поле ввода внутри
    company_field = WebDriverWait(browser, 5).until(EC.presence_of_element_located(NewBidLocators.COMPANY_FIELD))
    company_field.send_keys("AUTO")

    # Выбираем первый вариант
    first_option = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                               "div.react-select__option")))
    first_option.click()
    time.sleep(0.5)

    # Кликаем на селект "Автор", чтобы открыть поле ввода
    author = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(NewBidLocators.AUTHOR))
    author.click()

    # Находим поле ввода внутри
    author_field = WebDriverWait(browser, 5).until(EC.presence_of_element_located(NewBidLocators.AUTHOR_FIELD))
    author_field.send_keys("AUTO_TESTS")


    # Кликаем на селект "Телефон", чтобы открыть поле ввода
    phone_number = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(NewBidLocators.PHONE))
    phone_number.click()
    phone_number.send_keys("1234567890")
    time.sleep(2)

    # Проверка роли и поля "Менеджер DSM"
    if role == "Менеджер DSM":
        try:
            manager_input = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]"
                    "/following-sibling::div//div[contains(@class, 'react-select__input-container')]//input"
                ))
            )
            value = manager_input.get_attribute('value')
            if value == "Auto_manager":
                print("Поле менеджера заполнено правильно")
            else:
                print(f"Поле менеджера содержит {value}. Переделываем нахуй! ")
        except Exception as e:
            print("Не удалось найти или проверить поле менеджера:", e)
    else:
        # Кликаем на селект "Менеджер DSM 1", чтобы открыть поле ввода
        manager = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(NewBidLocators.MANAGER_1))
        manager.click()

        manager_field = WebDriverWait(browser, 5).until(EC.presence_of_element_located(NewBidLocators.MANAGER_1_FIELD))
        manager_field.send_keys("Auto_manager")
        time.sleep(2)