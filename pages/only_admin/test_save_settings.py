import time
import random
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import Locators
import pytest


def clear_input_field(field):
    """Очистка поля ввода, пока значение не станет '0'"""
    with allure.step("Очистка поля ввода"):
        max_attempts = 110
        for _ in range(max_attempts):
            field.click()
            for _ in range(3):
                field.send_keys(Keys.BACKSPACE)
            current_value = field.get_attribute("value")
            if current_value == "0":
                return True
        return False


def find_switch_element(driver, locators):
    """Поиск переключателя среди списка локаторов"""
    with allure.step("Поиск элемента переключателя"):
        for locator in locators:
            elements = driver.find_elements(*locator)
            if elements:
                return elements[0]
        return None


def get_switch_state(switch_element):
    """Определение состояния переключателя по классу"""
    with allure.step("Получение состояния переключателя"):
        class_attr = switch_element.get_attribute("class")
        return "checked" in class_attr or "active" in class_attr


@allure.feature("Тестирование настроек")
@allure.story("Проверка функционала настроек")
@pytest.mark.usefixtures("settings_modal", "auth")
class TestSettingsFlow:

    @pytest.fixture(scope="class")
    def saved_values(self):
        return {}

    @allure.title("Тестирование поля процентной ставки")
    def test_interest_rate_field(self, settings_modal, auth, saved_values):
        """Тестирование поля процентной ставки"""
        with allure.step("Получение поля ввода процентной ставки"):
            interest_input = WebDriverWait(settings_modal, 15).until(
                EC.element_to_be_clickable(Locators.INTEREST_RATE_INPUT))
            interest_value = str(random.randint(0, 100))

        with allure.step(f"Установка значения {interest_value} в поле процентной ставки"):
            assert clear_input_field(interest_input), "Не удалось очистить поле процентной ставки"
            interest_input.send_keys(interest_value)
            saved_values['interest'] = interest_value
            allure.attach(f"Значение установлено: {interest_value}", name="Результат")

    @allure.title("Тестирование полей переменных")
    @pytest.mark.parametrize("locator,name", [
        (Locators.VARIABLE_N2_INPUT, "variable2"),
        (Locators.VARIABLE_N3_INPUT, "variable3")
    ], ids=["variable_2", "variable_3"])
    def test_variable_fields(self, settings_modal, locator, name, saved_values):
        """Тестирование полей переменных"""
        with allure.step(f"Тестирование поля {name}"):
            field = WebDriverWait(settings_modal, 15).until(
                EC.element_to_be_clickable(locator))
            value = str(random.randint(0, 100))

        with allure.step(f"Установка значения {value} в поле {name}"):
            assert clear_input_field(field), f"Не удалось очистить поле {name}"
            field.send_keys(value)
            saved_values[name] = value

    @allure.title("Тестирование переключателя")
    def test_switch_toggle(self, auth, saved_values):
        """Тестирование переключателя"""
        with allure.step("Поиск и проверка переключателя"):
            switch = find_switch_element(auth, Locators.SWITCH_LOCATORS)
            assert switch is not None, "Не найден переключатель"

        with allure.step("Изменение состояния переключателя"):
            initial_state = get_switch_state(switch)
            switch.click()
            new_state = get_switch_state(switch)

        with allure.step("Проверка изменения состояния"):
            assert new_state != initial_state, "Состояние переключателя не изменилось после клика"
            saved_values['switch_state'] = new_state

    @allure.title("Тестирование кнопок сохранения")
    def test_save_buttons(self, settings_modal):
        """Тестирование кнопок сохранения"""
        with allure.step("Поиск кнопок сохранения"):
            save_buttons = WebDriverWait(settings_modal, 15).until(
                EC.presence_of_all_elements_located(Locators.SAVE_BUTTON))
            assert len(save_buttons) == 4, f"Ожидалось 4 кнопки сохранения, найдено {len(save_buttons)}"

        with allure.step("Нажатие всех кнопок сохранения"):
            for idx, btn in enumerate(save_buttons, start=1):
                with allure.step(f"Нажатие кнопки #{idx}"):
                    btn.click()

    @allure.title("Проверка индикаторов сохранения")
    def test_save_indicators(self, settings_modal):
        """Проверка индикаторов сохранения"""
        with allure.step("Поиск индикаторов сохранения"):
            saved_indicators = WebDriverWait(settings_modal, 15).until(
                EC.presence_of_all_elements_located(Locators.SAVED_INDICATOR))
            assert len(saved_indicators) == 4, f"Не все кнопки сохранили состояние. Найдено: {len(saved_indicators)}"

        with allure.step("Проверка состояния индикаторов"):
            for idx, indicator in enumerate(saved_indicators, start=1):
                with allure.step(f"Проверка индикатора #{idx}"):
                    class_attr = indicator.get_attribute("class")
                    assert "ChangeSettings__saved--XZlZA" in class_attr, \
                        f"Кнопка #{idx} не имеет класса 'saved' после сохранения."

    @allure.title("Тестирование закрытия модального окна")
    def test_modal_close_reopen(self, auth):
        """Тестирование закрытия модального окна"""
        with allure.step("Закрытие модального окна"):
            close_button = WebDriverWait(auth, 15).until(
                EC.element_to_be_clickable(Locators.CLOSE_MODAL_BUTTON))
            close_button.click()

        with allure.step("Проверка закрытия окна"):
            WebDriverWait(auth, 15).until(
                EC.invisibility_of_element_located(Locators.MODAL_WINDOW))

    @allure.title("Проверка сохраненных значений")
    def test_reopened_values(self, auth, saved_values):
        """Проверка сохраненных значений после повторного открытия"""
        with allure.step("Открытие модального окна настроек"):
            settings_button = WebDriverWait(auth, 15).until(
                EC.element_to_be_clickable(Locators.SETTINGS_BUTTON))
            settings_button.click()

            settings_modal = WebDriverWait(auth, 15).until(
                EC.visibility_of_element_located(Locators.MODAL_WINDOW))
            time.sleep(1)

        with allure.step("Проверка процентной ставки"):
            interest_input = WebDriverWait(settings_modal, 15).until(
                EC.element_to_be_clickable(Locators.INTEREST_RATE_INPUT))
            assert interest_input.get_attribute("value") == saved_values['interest'], \
                f"Значение процентной ставки не совпадает. Ожидалось: {saved_values['interest']}"

        with allure.step("Проверка полей переменных"):
            for locator, name in [(Locators.VARIABLE_N2_INPUT, "variable2"),
                                  (Locators.VARIABLE_N3_INPUT, "variable3")]:
                with allure.step(f"Проверка поля {name}"):
                    field = WebDriverWait(settings_modal, 15).until(
                        EC.element_to_be_clickable(locator))
                    assert field.get_attribute("value") == saved_values[name], \
                        f"Значение поля {name} не совпадает. Ожидалось: {saved_values[name]}"

        # Проверка состояния переключателя временно отключена
        with allure.step("Проверка состояния переключателя"):

             switch = find_switch_element(auth, Locators.SWITCH_LOCATORS)
             current_state = get_switch_state(switch)
             assert current_state == saved_values['switch_state'], \
                 f"Состояние переключателя не совпадает. Ожидалось: {saved_values['switch_state']}, Получено: {current_state}"
             allure.attach(f"Состояние переключателя корректно: {current_state}", name="Результат проверки")

        allure.attach("Все проверенные значения совпадают после повторного открытия", name="Общий результат")