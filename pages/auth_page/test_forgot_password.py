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


def test_password_recovery_flow(browser):
    # 1. Открытие страницы авторизации
    browser.get("http://mice.dsm.dev.thehead.ru/auth")
    assert browser.current_url == "http://mice.dsm.dev.thehead.ru/auth", "Не удалось открыть страницу авторизации"

    # 2. Клик на "Забыли пароль?"
    forgot_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Забыли пароль?"))
    )
    forgot_link.click()

    # Проверка перехода на страницу восстановления
    WebDriverWait(browser, 10).until(
        EC.url_to_be("http://mice.dsm.dev.thehead.ru/auth/forgot-password"))

    # 3. Заполнение email и отправка формы
    email_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_field.clear()
    email_field.send_keys("auto_admin@gmail.com")

    submit_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_btn.click()

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