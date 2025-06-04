import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators


@allure.feature ("Тест радио-баттонов 'Создать заявку'")
@allure.story ("Кликабельность радио-баттонов")
def test_create_request(auth):
    browser = auth
    assert "auth" not in browser.current_url


    # Кнопка "Создать заявку"
    with allure.step("Создать заявку"):
        create_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CREATE_NEW_BID_BUTTON))
        create_btn.click()

    # Радио-баттон "Круглый стол"
    with allure.step("Радио-баттон 'Круглый стол'"):
        circle_table = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CIRCLE_TABLE))
        circle_table.click()


    # Радио-баттон "Другое (Российская заявка)"
    with allure.step("Радио-баттон 'Другое' (Российская заявка)"):
        another_rus = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.ANOTHER_RUSSIAN))
        another_rus.click()


    # Радио-баттон "Интенсив"
    with allure.step("Радио-баттон 'Интенсив'"):
        intensive = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.INTENSIVE))
        intensive.click()


    # Радио-баттон "Конференция/цикловая конференция" (Международная заявка)
    with allure.step("Радио-баттон 'Конференция/цикловая конференция' (Международная заявка)"):
        conference = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.CONFERENCE_RADIO_INTERNATIONAL))
        conference.click()


    # Радио-баттон "Другое" (Международная заявка)
    with allure.step("Радио-баттон 'Другое' (Международная заявка)"):
        another_int = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.ANOTHER_INTERNATIONAL))
        another_int.click()


    # Радио-баттон "Заявка на тендер"
    with allure.step("Радио-баттон 'Заявка на тендер'"):
        tender = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.TENDER_APPLICATION))
        tender.click()

    # Радио-баттон "Проект DSM"
    with allure.step("Радио-баттон 'Проект DSM'"):
        project_dsm = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(Locators.PROJECT_DSM))
        project_dsm.click()
