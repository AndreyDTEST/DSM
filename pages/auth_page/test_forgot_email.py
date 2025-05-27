import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def wait_and_click(driver, by_locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(by_locator)
    )
    element.click()

def wait_for_url(driver, url, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.url_to_be(url)
    )

def wait_for_visibility(driver, by_locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(by_locator)
    )

def test_password_recovery_flow(browser):
    # 1. Открытие страницы авторизации
    browser.get("http://mice.dsm.dev.thehead.ru/auth")
    assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth"

    # 2. Клик на "Забыли пароль?"
    wait_and_click(browser, (By.LINK_TEXT, "Забыли пароль?"))
    wait_for_url(browser, "http://mice.dsm.dev.thehead.ru/auth/forgot-password")

    # 3. Клик на "Не помню e-mail"
    wait_and_click(browser, (By.LINK_TEXT, "Не помню e-mail"))
    wait_for_url(browser, "http://mice.dsm.dev.thehead.ru/auth/forgot-email")

    # Ввод номера телефона
    phone_field = wait_for_visibility(browser, (By.ID, "phoneNumber"))
    phone_field.send_keys("1234567890")

    # Ввод организации
    org_input = (By.XPATH, "//div[contains(@class, 'organizationName')]//input[@type='text']")
    org_input = wait_for_visibility(browser, org_input)
    org_input.send_keys("Моя компания")

    # Ввод ФИО
    full_name = (By.XPATH, "//div[contains(@class, 'fullName')]//input[@type='text']")
    full_name_input = wait_for_visibility(browser, full_name)
    full_name_input.send_keys("Моя ФИО")

    checkbox = (By.CLASS_NAME, "Checkbox__iconContainer--pbmVy")
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(checkbox)).click()

    # Нажимаем кнопку входа
    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # 4. Закрытие модального окна
    close_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//button[contains(@class, 'Button__mediumSizeButton')]//div[text()='Закрыть']/.."))
    )
    close_btn.click()

    # Проверка закрытия модального окна
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.ID, "modal-container-id")))

    # 5. Проверка возврата на страницу авторизации
    assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth", \
        "Не произошел возврат на страницу авторизации после закрытия модального окна"

