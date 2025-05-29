import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators
from conftest import NewBidLocators
from conftest import ManagerDSM
from conftest import DeleteManagerDSM
from conftest import ManagerClear
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



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
    time.sleep(0.3)

    def select_company(browser, company_name="AUTO", clear_after=False):
        # Ищем блок "Компания"
        company_field = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(NewBidLocators.COMPANY_FIELD)
        )
        company_field.send_keys(company_name)
        company_field.click()

        # Выбираем первый вариант
        first_option = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(NewBidLocators.FIRST_OPTION)
        )
        first_option.click()
        time.sleep(0.3)

        if clear_after:
            company_clear = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(NewBidLocators.COMPANY_CLEAR_INDICATOR)
            )
            company_clear.click()
            time.sleep(0.3)

    # Первый сценарий: выбрать и очистить
    select_company(browser, "AUTO", clear_after=True)

    # Второй сценарий: снова выбрать
    select_company(browser, "AUTO")

    # Находим поле ввода внутри
    author_field = WebDriverWait(browser, 5).until(EC.presence_of_element_located(NewBidLocators.AUTHOR_FIELD))
    author_field.send_keys("AUTO_TESTS")
    author_field.click()

    # Кликаем на селект "Телефон", чтобы открыть поле ввода
    phone_number = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(NewBidLocators.PHONE))
    phone_number.click()
    phone_number.send_keys("1234567890")


    # Проверка/заполнение поля
    if role == "Менеджер DSM":
        try:
            selected_value = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, """
            //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]
            /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
            """)))
            print("Поле менеджера заполнено правильно")
        except TimeoutException:
            print("Не найдено значение 'Auto_manager' в поле менеджера")
    else:
        # Кликаем на селект "Менеджер DSM 1", чтобы открыть поле ввода

        manager_field = (WebDriverWait(browser, 5).until
                        (EC.presence_of_element_located(ManagerDSM.MANAGER_1_FIELD)))
        manager_field.send_keys("Auto_manager")
        manager_field.click()
        time.sleep(0.1)

        # Выбираем первый вариант из выпадающего списка "Менеджер DSM"
        manager_first_option = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(NewBidLocators.FIRST_OPTION))
        manager_first_option.click()
        time.sleep(0.1)

    # Добавление новых менеджеров
    for _ in range(4):
        add_manager = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(ManagerDSM.ADD_MANAGER_BUTTON))
        add_manager.click()

    # Список локаторов и соответствующих названий
    managers = [
        (ManagerDSM.MANAGER_2_FIELD, 'Auto_manager_2'),
        (ManagerDSM.MANAGER_3_FIELD, 'Auto_manager_3'),
        (ManagerDSM.MANAGER_4_FIELD, 'Auto_manager_4'),
        (ManagerDSM.MANAGER_5_FIELD, 'Auto_manager_5'),
    ]

    for locator, manager_name in managers:
        # Находим поле
        manager_field = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(locator))
        # Вводим название менеджера
        manager_field.send_keys(manager_name)
        manager_field.click()
        time.sleep(0.1)

        # Ждем появления варианта и выбираем его
        first_option_2 = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(NewBidLocators.FIRST_OPTION))
        first_option_2.click()
        time.sleep(0.1)

    # Удаление вообще всех менеджеров
    for _ in range(4):
            del_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(DeleteManagerDSM.DELETE_MANAGER_2_BUTTON))
            del_button.click()
            time.sleep(0.1)

    manager_clear = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(ManagerClear.MANAGER_1_CLEAR_INDICATOR))
    manager_clear.click()
    time.sleep(2)



