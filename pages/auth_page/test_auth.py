import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(browser, auth_data):
    """Тест успешной авторизации с валидными данными"""
    browser.get("http://mice.dsm.dev.thehead.ru/auth")

    # Заполняем форму авторизации
    email_field = browser.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(auth_data["email"])

    password_field = browser.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_field.clear()
    password_field.send_keys(auth_data["password"])

    # Нажимаем кнопку входа
    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Проверяем переход на главную страницу
    assert WebDriverWait(browser, 10).until(
        EC.url_to_be("http://mice.dsm.dev.thehead.ru/")
    ), f"Не произошёл переход на главную страницу. Текущий URL: {browser.current_url}"
    time.sleep(1)


def test_invalid_login(browser, invalid_credentials):
    """Тест авторизации с НЕвалидными данными"""
    for credentials in invalid_credentials:
        browser.get("http://mice.dsm.dev.thehead.ru/auth")

        # Заполняем форму авторизации
        email_field = browser.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(credentials["email"])

        password_field = browser.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(credentials["password"])

        # Нажимаем кнопку входа
        login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # Проверяем сообщения об ошибках
        if not credentials["email"] or not credentials["password"]:
            # Проверка пустых полей
            error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Обязательное поле']"))
            )
            assert error_message.is_displayed(), "Сообщение 'Обязательное поле' не отображается"

        elif "@" not in credentials["email"] or "." not in credentials["email"]:
            # Проверка невалидного email
            error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Введите корректный e-mail']"))
            )
            assert error_message.is_displayed(), "Сообщение 'Введите корректный e-mail' не отображается"

        else:
            # Проверка неверных учетных данных
            error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Неверные логин или пароль']"))
            )
            assert error_message.is_displayed(), "Сообщение 'Неверные логин или пароль' не отображается"

        # Проверяем, что остались на странице авторизации
        current_url = browser.current_url
        assert "auth" in current_url, \
            f"Не остались на странице авторизации для данных {credentials}. Текущий URL: {current_url}"