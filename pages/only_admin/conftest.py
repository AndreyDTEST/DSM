import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Locators:
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    SETTINGS_BUTTON = (By.XPATH, "//button[.//span[contains(., 'Настройки')]]")
    MODAL_WINDOW = (By.CLASS_NAME, "ChangeSettings__settingsModal--vZGFs")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//div[contains(@class, 'ChangeSettings__topSideChangeSettings')]//*[local-name()='svg']")

    INTEREST_RATE_INPUT = (By.XPATH,
                           "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Процентная ставка']]" +
                           "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    VARIABLE_N2_INPUT = (By.XPATH,
                         "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Переменная №2']]" +
                         "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    VARIABLE_N3_INPUT = (By.XPATH,
                         "//div[contains(@class, 'Input__nameContainer--pbmVy') and .//div[normalize-space(text())='Переменная №3']]" +
                         "/following-sibling::div//div[contains(@class, 'Input__inputContainer--W5lcg')]//input[@type='text']")
    SWITCH_LOCATORS = [
        (By.CSS_SELECTOR, "div[role='switch']"),
        (By.CSS_SELECTOR, "div[class*='Switch']"),
        (By.XPATH, "//div[contains(@class, 'switch')]")
    ]
    SAVE_BUTTON = (By.CSS_SELECTOR, ".ChangeSettings__settingsSaveBtn--VCdG4")
    SAVED_INDICATOR = (By.CSS_SELECTOR,".ChangeSettings__settingsSaveBtn--VCdG4.ChangeSettings__saved--XZlZA")


    FINANCE_BUTTON = (By.XPATH, "//div[text()='Финансы']")
    INVOICE_APPROVE_BUTTON = (By.XPATH, "//div[contains(@class, 'ModalTabs__modalTabText') and text()='Согласование счета']")


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def auth(driver):
    """Фикстура только для авторизации"""
    driver.get("http://mice.dsm.dev.thehead.ru/auth")
    email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(Locators.EMAIL_INPUT))
    email_input.send_keys("auto_admin@gmail.com")

    password_input = driver.find_element(*Locators.PASSWORD_INPUT)
    password_input.send_keys("z1crjhjcnm")

    submit_button = driver.find_element(*Locators.SUBMIT_BUTTON)
    submit_button.click()

    WebDriverWait(driver, 15).until(lambda d: "auth" not in d.current_url)
    return driver


@pytest.fixture(scope="module")
def settings_modal(auth):
    """Фикстура для открытия настроек"""
    settings_button = WebDriverWait(auth, 15).until(EC.element_to_be_clickable(Locators.SETTINGS_BUTTON))
    settings_button.click()

    modal = WebDriverWait(auth, 15).until(EC.visibility_of_element_located(Locators.MODAL_WINDOW))
    return modal

@pytest.fixture(scope="module")
def finance_section(auth):
    """Фикстура для перехода в раздел Финансы и Согласование счета"""
    browser = auth

    # Находим внутри него элемент с текстом "Финансы"
    finance_link = WebDriverWait(auth, 15).until(EC.visibility_of_element_located(Locators.FINANCE_BUTTON))

    # Кликаем по нему
    finance_link.click()

    # Проверяем что перешли на страницу документов
    WebDriverWait(browser, 15).until(EC.url_contains("/finance/documents"))

    # Переходим непосредственно на страницу согласования счетов
    invoice_approve_link = WebDriverWait(auth, 15).until(EC.visibility_of_element_located(Locators.INVOICE_APPROVE_BUTTON))
    invoice_approve_link.click()

    # Проверяем что страница загрузилась
    WebDriverWait(browser, 15).until(
        EC.url_contains("/invoice-approve"))

    return browser