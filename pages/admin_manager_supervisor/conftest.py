
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Locators:
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CREATE_NEW_BID_BUTTON = (By.XPATH, "//button[contains(@class, 'Button__bigSizeButton--R0b24 Button__primaryButton--R0b24 Button__iconLeftButton--0dG9u')]/div[contains(text(), 'Создать заявку')]")
    CIRCLE_TABLE = (By.XPATH, "//span[contains(., 'Круглый стол')]")
    ANOTHER_RUSSIAN = (By.XPATH,
        "//div[contains(@class, 'CreateRequestTypeSelect__categoryWithType')][.//p[contains(text(), 'Российская заявка')]]"
        "//span[contains(text(), 'Другое')]")
    INTENSIVE = (By.XPATH, "//span[contains(., 'Инсентив')]")
    CONFERENCE_RADIO_INTERNATIONAL = (By.XPATH,
        "//div[contains(@class, 'CreateRequestTypeSelect__categoryWithType')][.//p[contains(text(), 'Международная заявка')]]"
        "//span[contains(text(), 'Конференция/цикловая конференция')]")
    ANOTHER_INTERNATIONAL = (By.XPATH,
        "//div[contains(@class, 'CreateRequestTypeSelect__categoryWithType')][.//p[contains(text(), 'Международная заявка')]]"
        "//span[contains(text(), 'Другое')]")
    TENDER_APPLICATION = (By.XPATH, "//span[contains(., 'Заявка на тендер')]")
    PROJECT_DSM = (By.XPATH, "//span[contains(., 'Проект DSM')]")
    CREATE_BUTTON = (By.XPATH, "//button[.//div[text()='Создать заявку']]")
    FIRST_OPTION = (By.XPATH, "(//div[contains(@class, 'react-select__option')])[1]")

class Customer:
    COMPANY_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Компания']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)

    AUTHOR_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Автор']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    PHONE = (By.ID, "phoneNumber")
    COMPANY_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Компания']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)

class ManagerDSM:
    MANAGER_VALUE = (By.XPATH,
                     "//div[@class='react-select__single-value css-w54w9q-singleValue']//*[normalize-space(text())='Auto_manager']")

    MANAGER_1_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)

    MANAGER_2_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 2']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    MANAGER_3_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 3']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    MANAGER_4_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 4']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    MANAGER_5_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 5']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    ADD_MANAGER_BUTTON = (By.XPATH, "//button[.//div[text()='Добавить менеджера']]")

class DeleteManagerDSM:
    DELETE_MANAGER_2_BUTTON = (By.XPATH, """
    //div[contains(text(), 'Менеджер DSM 2')]/ancestor::div[contains(@class, 'Input__nameContainer')]
    /following::button[contains(@class, 'Button')]
    """)
    DELETE_MANAGER_3_BUTTON = (By.XPATH, """
    //div[contains(text(), 'Менеджер DSM 3')]/ancestor::div[contains(@class, 'Input__nameContainer')]
    /following::button[contains(@class, 'Button')]
    """)
    DELETE_MANAGER_4_BUTTON = (By.XPATH, """
    //div[contains(text(), 'Менеджер DSM 4')]/ancestor::div[contains(@class, 'Input__nameContainer')]
    /following::button[contains(@class, 'Button')]
    """)
    DELETE_MANAGER_5_BUTTON = (By.XPATH, """
    //div[contains(text(), 'Менеджер DSM 5')]/ancestor::div[contains(@class, 'Input__nameContainer')]
    /following::button[contains(@class, 'Button')]
    """)
class ManagerClear:
    MANAGER_1_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    MANAGER_2_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 2']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    MANAGER_3_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 3']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    MANAGER_4_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 4']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    MANAGER_5_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 5']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
class Event:
    NAME_FIELD = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Наименование']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    TYPE_FIELD = (By.XPATH, """
                            //div[contains(@class, 'Input__nameContainer')][.//div[text()='Тип мероприятия']]
                            /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
                            """)
    PLAN_QUANTITY_FIELD = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Кол-во чел. план']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    FACT_QUANTITY_FIELD = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Кол-во чел. факт']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    EVENT_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Тип мероприятия']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)

class Budget:
    TOTAL_BUDGET = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Итог. бюджет (без НДС) план']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    PREPARATION = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Препарат']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")

class Venue:
    COUNTRY_VALUE = (By.XPATH,
    "//div[@class='react-select__single-value react-select__single-value--is-disabled css-w54w9q-singleValue']//*[normalize-space(text())='Россия']")

    CITY = (By.XPATH, """
            //div[contains(@class, 'Input__nameContainer')][.//div[text()='Город']]
            /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
            """)
    SITE_TYPE = (By.XPATH, """
            //div[contains(@class, 'Input__nameContainer')][.//div[text()='Тип площадки']]
            /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
            """)
    SITE = (By.XPATH, """
            //div[contains(@class, 'Input__nameContainer')][.//div[text()='Площадка']]
            /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
            """)
    CITY_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Город']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    SITE_TYPE_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Тип площадки']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)
    SITE_CLEAR_INDICATOR = (By.XPATH, """
        //div[contains(@class, 'Input__nameContainer')][.//div[text()='Площадка']]
        /following-sibling::div//div[contains(@class, 'react-select__indicators')]//div[contains(@class, 'react-select__clear-indicator')]
        """)





@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(params=[
    {
        "role": "Менеджер DSM",
        "email": "auto_manager@gmail.com",
        "password": "z1crjhjcnm",
    },
    {
        "role": "Руководитель DSM",
        "email": "auto_ruk@gmail.com",
        "password": "z1crjhjcnm",
    },
    {
        "role": "Администратор DSM",
        "email": "auto_admin@gmail.com",
        "password": "z1crjhjcnm",
    }
])
def auth_data(request):
    return request.param


@pytest.fixture
def auth(driver, auth_data):
    """Фикстура для авторизации с параметрами"""
    driver.get("http://mice.dsm.dev.thehead.ru/auth")

    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(Locators.EMAIL_FIELD))
    email_input.send_keys(auth_data["email"])

    password_input = driver.find_element(*Locators.PASSWORD_FIELD)
    password_input.send_keys(auth_data["password"])

    submit_button = driver.find_element(*Locators.LOGIN_BUTTON)
    submit_button.click()

    WebDriverWait(driver, 15).until(lambda d: "auth" not in d.current_url)
    return driver