import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from conftest import Locators
from conftest import Customer
from conftest import ManagerDSM
from conftest import DeleteManagerDSM
from conftest import ManagerClear
from conftest import Event
from conftest import Budget
from conftest import Venue




@allure.feature("Создание заявки")
@allure.story("Проверка создания заявки на круглый стол")
def test_create_request(auth, auth_data):
    browser = auth
    role = auth_data["role"]

    with allure.step("Проверяем успешную авторизацию"):
        assert "auth" not in browser.current_url

    with allure.step("Нажимаем кнопку 'Создать заявку'"):
        create_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(Locators.CREATE_NEW_BID_BUTTON))
        create_btn.click()

    with allure.step("Выбираем тип 'Круглый стол'"):
        circle_table = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(Locators.CIRCLE_TABLE))
        circle_table.click()

    with allure.step("Нажимаем кнопку 'Создать' в модальном окне"):
        create_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(Locators.CREATE_BUTTON))
        create_btn.click()
    time.sleep(0.5)

    def select_company(browser, company_name="AUTO", clear_after=False):
        with allure.step(f"Выбираем компанию '{company_name}'"):
            company_field = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(Customer.COMPANY_FIELD)
            )
            company_field.send_keys(company_name)
            time.sleep(0.2)
            company_field.click()
            time.sleep(0.3)

            first_option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(Locators.FIRST_OPTION)
            )
            first_option.click()
            time.sleep(0.2)

            if clear_after:
                with allure.step("Очищаем поле компании"):
                    company_clear = WebDriverWait(browser, 5).until(
                        EC.element_to_be_clickable(Customer.COMPANY_CLEAR_INDICATOR)
                    )
                    company_clear.click()
                    time.sleep(0.2)

    with allure.step("Тестируем выбор компании - первый сценарий (с очисткой)"):
        select_company(browser, "AUTO", clear_after=True)

    with allure.step("Тестируем выбор компании - второй сценарий (без очистки)"):
        select_company(browser, "AUTO")

    with allure.step("Заполняем поле 'Автор'"):
        author_field = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Customer.AUTHOR_FIELD))
        author_field.send_keys("AUTO_TESTS")
        time.sleep(0.2)
        author_field.click()
        time.sleep(0.3)

    with allure.step("Заполняем поле 'Телефон'"):
        phone_number = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(Customer.PHONE))
        phone_number.click()
        time.sleep(0.2)
        phone_number.send_keys("1234567890")
        time.sleep(0.2)

    with allure.step("Проверяем/заполняем поле 'Менеджер DSM'"):
        if role == "Менеджер DSM":
                try:
                    element = WebDriverWait(browser, 5).until(
                        EC.visibility_of_element_located(ManagerDSM.MANAGER_VALUE)
                    )
                    allure.attach("Элемент 'Auto_manager' не найден за отведенное время", name="Результат поиска",
                                  attachment_type=allure.attachment_type.TEXT)

                except TimeoutException:
                    allure.attach("Элемент 'Auto_manager' не найден", name="Результат поиска",
                                  attachment_type=allure.attachment_type.TEXT)
        else:
            manager_field = (WebDriverWait(browser, 5).until
                            (EC.presence_of_element_located(ManagerDSM.MANAGER_1_FIELD)))
            manager_field.send_keys("Auto_manager")
            manager_field.click()
            time.sleep(0.1)

            manager_first_option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(Locators.FIRST_OPTION))
            manager_first_option.click()
            time.sleep(0.1)

    with allure.step("Добавляем дополнительных менеджеров"):
        for _ in range(4):
            add_manager = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(ManagerDSM.ADD_MANAGER_BUTTON))
            add_manager.click()
            time.sleep(0.1)

    with allure.step("Заполняем поля дополнительных менеджеров"):
        managers = [
            (ManagerDSM.MANAGER_2_FIELD, 'Auto_manager_2'),
            (ManagerDSM.MANAGER_3_FIELD, 'Auto_manager_3'),
            (ManagerDSM.MANAGER_4_FIELD, 'Auto_manager_4'),
            (ManagerDSM.MANAGER_5_FIELD, 'Auto_manager_5'),
        ]

        for locator, manager_name in managers:
            manager_field = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(locator))
            manager_field.send_keys(manager_name)
            manager_field.click()
            time.sleep(0.1)

            first_option_2 = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(Locators.FIRST_OPTION))
            first_option_2.click()
            time.sleep(0.1)

    with allure.step("Удаляем некоторых менеджеров"):
        manager_numbers = [4, 2, 3, 2]

        for num in manager_numbers:
            clear_locator = getattr(ManagerClear, f"MANAGER_{num}_CLEAR_INDICATOR")
            delete_locator = getattr(DeleteManagerDSM, f"DELETE_MANAGER_{num}_BUTTON")

            with allure.step(f"Очищаем и удаляем менеджера {num}"):
                manager_clear = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(clear_locator)
                )
                manager_clear.click()
                time.sleep(0.1)

                del_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(delete_locator)
                )
                del_button.click()
                time.sleep(0.1)

    with allure.step("Заполняем поле 'Название мероприятия'"):
        name_field = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Event.NAME_FIELD))
        name_field.send_keys("AUTO_TESTS")
        name_field.click()
        time.sleep(0.2)

    def select_event_type(browser, type_name="Другое", clear_after=False):
        with allure.step(f"Выбираем тип мероприятия '{type_name}'"):
            type_event_field = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(Event.TYPE_FIELD))
            type_event_field.send_keys(type_name)
            type_event_field.click()
            time.sleep(0.1)

            first_option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(Locators.FIRST_OPTION)
            )
            first_option.click()
            time.sleep(0.3)

            if clear_after:
                with allure.step("Очищаем поле типа мероприятия"):
                    type_clear = WebDriverWait(browser, 5).until(
                        EC.element_to_be_clickable(Event.EVENT_CLEAR_INDICATOR)
                    )
                    type_clear.click()
                    time.sleep(0.2)

    with allure.step("Тестируем выбор типа мероприятия - первый сценарий (с очисткой)"):
        select_event_type(browser, "Другое", clear_after=True)

    with allure.step("Тестируем выбор типа мероприятия - второй сценарий (без очистки)"):
        select_event_type(browser, "Другое")

    with allure.step("Заполняем поле 'Планируемое количество участников'"):
        plan_quantity_field = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Event.PLAN_QUANTITY_FIELD))
        plan_quantity_field.send_keys("123")
        plan_quantity_field.click()
        time.sleep(0.2)

    with allure.step("Заполняем поле 'Фактическое количество участников'"):
        fact_quantity_field = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Event.FACT_QUANTITY_FIELD))
        fact_quantity_field.send_keys("123")
        fact_quantity_field.click()
        time.sleep(0.2)

    with allure.step("Заполняем поле 'Итог. бюджет (без НДС) план'"):
        total_budget = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Budget.TOTAL_BUDGET))
        total_budget.send_keys("123")
        total_budget.click()
        time.sleep(0.2)

    with allure.step("Заполняем поле 'Препарат'"):
        preparation = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(Budget.PREPARATION))
        preparation.send_keys("123")
        preparation.click()
        time.sleep(0.2)



    with allure.step("Заполняем поле 'Cтрана'"):
        try:
            element = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located(Venue.COUNTRY_VALUE)
            )
            allure.attach("Элемент 'Россия' найден.", name="Результат поиска",
                          attachment_type=allure.attachment_type.TEXT)

        except TimeoutException:
            allure.attach("Элемент 'Россия' не найден за отведенное время.", name="Результат поиска",
                          attachment_type=allure.attachment_type.TEXT)
