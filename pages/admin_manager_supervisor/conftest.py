
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

class NewBidLocators:
    COMPANY = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Компания']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    COMPANY_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Компания']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)

    AUTHOR = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Автор']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    AUTHOR_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Автор']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    PHONE = (By.ID, "phoneNumber")
    MANAGER_1 = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
    """)
    MANAGER_1_FIELD = (By.XPATH, """
    //div[contains(@class, 'Input__nameContainer')][.//div[text()='Менеджер DSM 1']]
    /following-sibling::div//div[contains(@class, 'react-select__input-container')]//input
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