import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
def test_successful_login(browser, auth_data):
    """Тест успешной авторизации с валидными данными"""
    with allure.step("Открыть страницу авторизации"):
        browser.get("http://mice.dsm.dev.thehead.ru/auth")

    with allure.step("Заполнить форму авторизации"):
        email_field = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.EMAIL_FIELD))
        email_field.send_keys(auth_data["email"])

        password_field = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.PASSWORD_FIELD))
        password_field.send_keys(auth_data["password"])

    with allure.step("Нажать кнопку входа"):
        login_button = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.LOGIN_BUTTON))
        login_button.click()

    with allure.step("Проверить переход на главную страницу"):
        assert WebDriverWait(browser, 10).until(
            EC.url_to_be("http://mice.dsm.dev.thehead.ru/")
        ), f"Не произошёл переход на главную страницу. Текущий URL: {browser.current_url}"

@allure.feature("Авторизация")
@allure.story("Неуспешная авторизация")
def test_invalid_login(browser, invalid_credentials):
    """Тест авторизации с НЕвалидными данными"""
    for credentials in invalid_credentials:
        browser.get("http://mice.dsm.dev.thehead.ru/auth")

        with allure.step("Заполнить форму авторизации"):
            email_field = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.EMAIL_FIELD))
            email_field.send_keys(credentials["email"])

            password_field = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.PASSWORD_FIELD))
            password_field.send_keys(credentials["password"])

        with allure.step("Нажать кнопку входа"):
            login_button = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(Locators.LOGIN_BUTTON))
            login_button.click()

        # Проверяем сообщения об ошибках
        with allure.step("Проверяем сообщения об ошибках"):
            if not credentials["email"] or not credentials["password"]:
                # Проверка пустых полей
                error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located(Locators.REQUIRED_MASSAGE))
                assert error_message.is_displayed(), "Сообщение 'Обязательное поле' не отображается"

            elif "@" not in credentials["email"] or "." not in credentials["email"]:
                # Проверка невалидного email
                error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located(Locators.INVALID_EMAIL_MASSAGE))
                assert error_message.is_displayed(), "Сообщение 'Введите корректный e-mail' не отображается"

            else:
                # Проверка неверных учетных данных
                error_message = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located(Locators.INVALID_MASSAGE))
                assert error_message.is_displayed(), "Сообщение 'Неверные логин или пароль' не отображается"

        # Проверяем, что остались на странице авторизации
        with allure.step("Остались на странице авторизации"):
            current_url = browser.current_url
            assert "auth" in current_url, \
            f"Не остались на странице авторизации для данных {credentials}. Текущий URL: {current_url}"