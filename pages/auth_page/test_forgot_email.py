import pytest
import allure
from conftest import Locators
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@allure.feature("Не помню e-mail")
@allure.story("Успешная отправка формы восстановления")
def test_password_recovery_flow(browser):
    # 1. Открытие и проверка страницы авторизации
    with allure.step("Открыть страницу авторизации"):
        browser.get("http://mice.dsm.dev.thehead.ru/auth")
        assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth", "Не удалось открыть страницу авторизации"

    # 2. Переход на страницу восстановления пароля
    with allure.step("Открыть страницу восстановления пароля"):
        forgot_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.FORGOT_PASSWORD_BUTTON))
        forgot_link.click()

    with allure.step("Проверка перехода на страницу восстановления пароля"):
        WebDriverWait(browser, 10).until(
        EC.url_to_be("http://mice.dsm.dev.thehead.ru/auth/forgot-password"))

    # 3. Переход на страницу восстановления email
    with allure.step("Открыть страницу восстановления email"):
        dont_remember_email = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.FORGOT_EMAIL_BUTTON))
        dont_remember_email.click()

    with allure.step("Проверка перехода на страницу восстановления email"):
        WebDriverWait(browser, 10).until(
        EC.url_to_be("http://mice.dsm.dev.thehead.ru/auth/forgot-email"))

    # Заполнение формы восстановления
    # Ввод номера телефона
    with allure.step("Ввод номера телефона"):
        phone_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(Locators.PHONE_FIELD))
        phone_field.send_keys("1234567890")

    # Ввод организации
    with allure.step("Ввод организации"):
        org_input = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(Locators.COMPANY_FIELD))
        org_input.send_keys("Моя компания")

    # Ввод ФИО
    with allure.step("Ввод ФИО"):
        full_name_input = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(Locators.FIO_FIELD))
        full_name_input.send_keys("Моя ФИО")

    # Активация чекбокса
    with allure.step("Активация чекбокса"):
        checkbox = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.CHECK_BOX))
        checkbox.click()

    # Отправка формы
    with allure.step("Отправка формы"):
        login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.LOGIN_BUTTON))
        login_button.click()

    # 4. Закрытие модального окна
    with allure.step("Закрытие модального окна"):
        close_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.CLOSE_MODAL_BUTTON))
        close_btn.click()

    # Проверка закрытия модального окна
    with allure.step("Проверка закрытия модального окна"):
        WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located(Locators.MODAL_WINDOW))

    # 5. Проверка возврата на страницу авторизации
    with allure.step("Проверка возврата на страницу авторизации"):
        assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth", \
        "Не произошел возврат на страницу авторизации после закрытия модального окна"