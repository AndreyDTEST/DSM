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
    # 1. Открытие страницы авторизации
    with allure.step("Открыть страницу авторизации"):
        browser.get("http://mice.dsm.dev.thehead.ru/auth")
        assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth", "Не удалось открыть страницу авторизации"

    # 2. Клик на "Забыли пароль?"
    with allure.step("Открыть страницу восстановления пароля"):
        forgot_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.FORGOT_PASSWORD_BUTTON))
        forgot_link.click()

    with allure.step("Проверка перехода на страницу восстановления пароля"):
        WebDriverWait(browser, 10).until(
        EC.url_to_be("http://mice.dsm.dev.thehead.ru/auth/forgot-password"))

    # 3. Заполнение email и отправка формы
    with allure.step("Заполнение email"):
        email_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(Locators.EMAIL_FIELD))
        email_field.send_keys("auto_admin@gmail.com")

    with allure.step("Отправка формы"):
        submit_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(Locators.LOGIN_BUTTON))
        submit_btn.click()

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