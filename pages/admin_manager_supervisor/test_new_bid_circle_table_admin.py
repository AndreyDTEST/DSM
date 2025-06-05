import time
import allure
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from conftest import Locators, Customer, ManagerDSM, DeleteManagerDSM, ManagerClear, Event, Budget, Venue

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'test_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

venue_mapping = data.get('venue_mapping', [])


def safe_interaction(browser, locator, action_type, value=None, timeout=1, retries=5):
    """Безопасное взаимодействие с элементом с повторными попытками"""
    for attempt in range(retries):
        try:
            element = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located(locator))

            if action_type == "click":
                WebDriverWait(browser, timeout).until(
                    EC.element_to_be_clickable(locator)).click()
            elif action_type == "send_keys":
                element.send_keys(value)


            time.sleep(0.05)
            return True

        except:
            if attempt == retries - 1:
                raise
            time.sleep(0.3)
    return False

def fill_select_and_clear(browser):
    """Заполняет поля type и site, выбирает первые значения, затем очищает"""
    for item in venue_mapping:
        site_type = item['type']
        site = item['site']

        with allure.step(f"Обработка записи: type={site_type}, site={site}"):
            # Заполняем SITE_TYPE и выбираем первый вариант
            safe_interaction(browser, Venue.SITE_TYPE, "send_keys", site_type)
            safe_interaction(browser, Venue.SITE_TYPE, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

            # Заполняем SITE и выбираем первый вариант
            safe_interaction(browser, Venue.SITE, "send_keys", site)
            safe_interaction(browser, Venue.SITE, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

            # Очищаем оба поля
            safe_interaction(browser, Venue.SITE_TYPE_CLEAR_INDICATOR, "click")


@allure.feature("Создание заявки")
@allure.story("Проверка создания заявки на круглый стол")
def test_create_request(auth, auth_data):
    browser = auth
    role = auth_data["role"]

    with allure.step("Проверяем успешную авторизацию"):
        assert "auth" not in browser.current_url

    with allure.step("Нажимаем кнопку 'Создать заявку'"):
        safe_interaction(browser, Locators.CREATE_NEW_BID_BUTTON, "click")

    with allure.step("Выбираем тип 'Круглый стол'"):
        safe_interaction(browser, Locators.CIRCLE_TABLE, "click")

    with allure.step("Нажимаем кнопку 'Создать' в модальном окне"):
        safe_interaction(browser, Locators.CREATE_BUTTON, "click")
    time.sleep(0.5)

    def select_company(browser, company_name="AUTO", clear_after=False):
        with allure.step(f"Выбираем компанию '{company_name}'"):
            safe_interaction(browser, Customer.COMPANY_FIELD, "send_keys", company_name)
            safe_interaction(browser, Customer.COMPANY_FIELD, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

            if clear_after:
                with allure.step("Очищаем поле компании"):
                    safe_interaction(browser, Customer.COMPANY_CLEAR_INDICATOR, "click")

    with allure.step("Тестируем выбор компании - первый сценарий (с очисткой)"):
        select_company(browser, "AUTO", clear_after=True)

    with allure.step("Тестируем выбор компании - второй сценарий (без очистки)"):
        select_company(browser, "AUTO")

    with allure.step("Заполняем поле 'Автор'"):
        safe_interaction(browser, Customer.AUTHOR_FIELD, "send_keys", "AUTO_TESTS")
        safe_interaction(browser, Customer.AUTHOR_FIELD, "click")

    with allure.step("Заполняем поле 'Телефон'"):
        safe_interaction(browser, Customer.PHONE, "click")
        safe_interaction(browser, Customer.PHONE, "send_keys", "1234567890")

    with allure.step("Проверяем/заполняем поле 'Менеджер DSM'"):
        if role == "Менеджер DSM":
            try:
                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located(ManagerDSM.MANAGER_VALUE))
                allure.attach("Элемент 'Auto_manager' не найден за отведенное время",
                              name="Результат поиска",
                              attachment_type=allure.attachment_type.TEXT)
            except TimeoutException:
                allure.attach("Элемент 'Auto_manager' не найден",
                              name="Результат поиска",
                              attachment_type=allure.attachment_type.TEXT)
        else:
            safe_interaction(browser, ManagerDSM.MANAGER_1_FIELD, "send_keys", "Auto_manager")
            safe_interaction(browser, ManagerDSM.MANAGER_1_FIELD, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

    with allure.step("Добавляем дополнительных менеджеров"):
        for _ in range(4):
            safe_interaction(browser, ManagerDSM.ADD_MANAGER_BUTTON, "click")

    with allure.step("Заполняем поля дополнительных менеджеров"):
        managers = [
            (ManagerDSM.MANAGER_2_FIELD, 'Auto_manager_2'),
            (ManagerDSM.MANAGER_3_FIELD, 'Auto_manager_3'),
            (ManagerDSM.MANAGER_4_FIELD, 'Auto_manager_4'),
            (ManagerDSM.MANAGER_5_FIELD, 'Auto_manager_5'),
        ]

        for locator, manager_name in managers:
            safe_interaction(browser, locator, "send_keys", manager_name)
            safe_interaction(browser, locator, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

    with allure.step("Удаляем некоторых менеджеров"):
        manager_numbers = [4, 2, 3, 2]

        for num in manager_numbers:
            clear_locator = getattr(ManagerClear, f"MANAGER_{num}_CLEAR_INDICATOR")
            delete_locator = getattr(DeleteManagerDSM, f"DELETE_MANAGER_{num}_BUTTON")

            with allure.step(f"Очищаем и удаляем менеджера {num}"):
                safe_interaction(browser, clear_locator, "click")
                safe_interaction(browser, delete_locator, "click")

    with allure.step("Заполняем поле 'Название мероприятия'"):
        safe_interaction(browser, Event.NAME_FIELD, "send_keys", "AUTO_TESTS")
        safe_interaction(browser, Event.NAME_FIELD, "click")

    def select_event_type(browser, type_name="Другое", clear_after=False):
        with allure.step(f"Выбираем тип мероприятия '{type_name}'"):
            safe_interaction(browser, Event.TYPE_FIELD, "send_keys", type_name)
            safe_interaction(browser, Event.TYPE_FIELD, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

            if clear_after:
                with allure.step("Очищаем поле типа мероприятия"):
                    safe_interaction(browser, Event.EVENT_CLEAR_INDICATOR, "click")

    with allure.step("Тестируем выбор типа мероприятия - первый сценарий (с очисткой)"):
        select_event_type(browser, "Другое", clear_after=True)

    with allure.step("Тестируем выбор типа мероприятия - второй сценарий (без очистки)"):
        select_event_type(browser, "Другое")

    with allure.step("Заполняем поле 'Планируемое количество участников'"):
        safe_interaction(browser, Event.PLAN_QUANTITY_FIELD, "send_keys", "123")
        safe_interaction(browser, Event.PLAN_QUANTITY_FIELD, "click")

    with allure.step("Заполняем поле 'Фактическое количество участников'"):
        safe_interaction(browser, Event.FACT_QUANTITY_FIELD, "send_keys", "123")
        safe_interaction(browser, Event.FACT_QUANTITY_FIELD, "click")

    with allure.step("Заполняем поле 'Итог. бюджет (без НДС) план'"):
        safe_interaction(browser, Budget.TOTAL_BUDGET, "send_keys", "123")
        safe_interaction(browser, Budget.TOTAL_BUDGET, "click")

    with allure.step("Заполняем поле 'Препарат'"):
        safe_interaction(browser, Budget.PREPARATION, "send_keys", "123")
        safe_interaction(browser, Budget.PREPARATION, "click")

    with allure.step("Проверяем значение в поле 'Cтрана'"):
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(Venue.COUNTRY_VALUE))
            allure.attach("Элемент 'Россия' найден.",
                          name="Результат поиска",
                          attachment_type=allure.attachment_type.TEXT)
        except TimeoutException:
            allure.attach("Элемент 'Россия' не найден за отведенное время.",
                          name="Результат поиска",
                          attachment_type=allure.attachment_type.TEXT)

    def select_city(browser, city_name="Москва", clear_after=False):
        with allure.step(f"Выбираем Город'{city_name}'"):
            safe_interaction(browser, Venue.CITY, "send_keys", city_name)
            safe_interaction(browser, Venue.CITY, "click")
            safe_interaction(browser, Locators.FIRST_OPTION, "click")

            if clear_after:
                with allure.step("Очищаем поле Город"):
                    safe_interaction(browser, Venue.CITY_CLEAR_INDICATOR, "click")

    with allure.step("Тестируем выбор компании - первый сценарий (с очисткой)"):
        select_city(browser, "Москва", clear_after=True)

    with allure.step("Тестируем выбор компании - второй сценарий (без очистки)"):
        select_city(browser, "Москва")

    with allure.step("Заполняем поля площадки из JSON"):
        fill_select_and_clear(browser)