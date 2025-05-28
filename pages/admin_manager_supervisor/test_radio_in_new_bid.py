import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators

def test_create_request(auth):
    """Тест создания новой заявки под каждым пользователем"""
    browser = auth

    # Проверяем, что авторизация прошла успешно
    assert "auth" not in browser.current_url

    # Кнопка "Создать заявку"
    create_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CREATE_NEW_BID_BUTTON))
    create_btn.click()

    # Радио-баттон "Круглый стол"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CIRCLE_TABLE))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Другое (Российская заявка)"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.ANOTHER_RUSSIAN))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Интенсив"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.INTENSIVE))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Конференция/цикловая конференция" (Международная заявка)
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CONFERENCE_RADIO_INTERNATIONAL))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Другое" (Международная заявка)
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.ANOTHER_INTERNATIONAL))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Заявка на тендер"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.TENDER_APPLICATION))
    circle_table.click()
    time.sleep(0.3)

    # Радио-баттон "Проект DSM"
    circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.PROJECT_DSM))
    circle_table.click()
    time.sleep(0.3)