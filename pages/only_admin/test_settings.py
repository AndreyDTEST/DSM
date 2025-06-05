import allure
from selenium.webdriver.common.keys import Keys
import re
from conftest import Locators
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def clear_input_field(field):
    max_attempts = 105
    for _ in range(max_attempts):
        field.click()
        for _ in range(3):
            field.send_keys(Keys.BACKSPACE)
        current_value = field.get_attribute("value")
        if current_value == "0":
            return True
    return False


def clean_string(s):
    return re.sub(r'\s+', '', s)


@allure.feature("Тест Настроек")
@allure.story("Тест процентной ставки")
@pytest.mark.parametrize("input_value, expected_output, description", [
    ("50", "50", "Корректное значение"),
    ("-10", "10", "Отрицательные значения"),
    ("abc", "0", "Буквенные значения"),
    ("150", "15", "Максимальное значение 100"),
    ("1000", "100", "Максимальное значение 100")
], ids=["50", "-10", "abc", "150", "1000"])
def test_interest_rate_field(settings_modal, input_value, expected_output, description):
    """Тест процентной ставки"""
    with allure.step(f"Проверка поля 'Процентная ставка': {description}"):
        interest_input = WebDriverWait(settings_modal, 15).until(
            EC.element_to_be_clickable(Locators.INTEREST_RATE_INPUT))

        clear_input_field(interest_input)
        interest_input.send_keys(input_value)
        current_value = interest_input.get_attribute("value")

        with allure.step(f"Проверка: ввод '{input_value}' → ожидаем '{expected_output}'"):
            assert current_value == expected_output, \
                f"{description}. Ввод: '{input_value}', Получено: '{current_value}'"


@allure.story("Тест полей переменных")
@pytest.mark.parametrize("field_name, input_value, expected_output, description", [
    # Тест-кейсы для Переменной 2
    ("2", "1234567890", "1234567890", "Цифры короткое число"),
    ("2", "1" * 310, "∞", "Более 309 символов"),
    ("2", "abc123", "123", "Буквенные символы недопустимы"),
    ("2", "!@#$", "0", "Спецсимволы недопустимы"),
    ("2", "  456  ", "456", "Пробелы в начале и конце"),
    ("2", "12 34 56", "123456", "Пробелы внутри строки"),
    ("2", "abc!@#123xyz", "123", "Буквы и спецсимволы среди цифр"),
    ("2", "\xa0123\xa0456\xa0789", "123456789", "Невидимые символы внутри строки"),

    # Тест-кейсы для Переменной 3 (такие же как для Переменной 2)
    ("3", "1234567890", "1234567890", "Цифры короткое число"),
    ("3", "1" * 310, "∞", "Более 309 символов"),
    ("3", "abc123", "123", "Буквенные символы недопустимы"),
    ("3", "!@#$", "0", "Спецсимволы недопустимы"),
    ("3", "  456  ", "456", "Пробелы в начале и конце"),
    ("3", "12 34 56", "123456", "Пробелы внутри строки"),
    ("3", "abc!@#123xyz", "123", "Буквы и спецсимволы среди цифр"),
    ("3", "\xa0123\xa0456\xa0789", "123456789", "Невидимые символы внутри строки")
], ids=[
            # Идентификаторы для каждого кейса
            ])
def test_variable_fields(settings_modal, field_name, input_value, expected_output, description):
    """Тест полей переменных с разными значениями"""
    with allure.step(f"Проверка поля '{field_name}': {description}"):
        # Выбираем локатор в зависимости от имени поля
        field_locator = Locators.VARIABLE_N2_INPUT if field_name == "2" else Locators.VARIABLE_N3_INPUT

        field = WebDriverWait(settings_modal, 15).until(
            EC.element_to_be_clickable(field_locator))

        clear_input_field(field)
        field.send_keys(input_value)
        current_value = field.get_attribute("value")
        current_value_clean = clean_string(current_value.strip())

        input_digits_only = re.sub(r'\D', '', input_value)

        if len(input_digits_only) > 309:
            expected_field_value = '∞'
            with allure.step(f"Проверка длинного числа (>309 символов)"):
                assert current_value_clean == expected_field_value, \
                    f"{description}. Ввод: '{input_value}', Получено: '{current_value}'"
            return

        if not re.sub(r'\D', '', current_value):
            expected_field_value = '0'
        else:
            expected_field_value = expected_output

        with allure.step(f"Проверка: ввод '{input_value}' → ожидаем '{expected_field_value}'"):
            assert current_value_clean == expected_field_value, \
                f"{description}. Ввод: '{input_value}', Ожидается: '{expected_field_value}', Получено: '{current_value}'"


def get_switch_element(driver):
    """Находит элемент переключателя"""
    for by, value in Locators.SWITCH_LOCATORS:
        try:
            element = driver.find_element(by, value)
            return element
        except NoSuchElementException:
            continue
    raise NoSuchElementException(f"Переключатель не найден")


def get_switch_state(switch_element):
    """Определяет состояние переключателя (True - активен, False - неактивен)"""
    classes = switch_element.get_attribute('class')
    return 'Switch__checkedSwitch--l0Y2g' in classes


@allure.story("Проверка переключения состояния")
def test_switch_toggle(auth):
    """Тест переключения с проверкой состояний"""
    with allure.step("First found"):
        switch = get_switch_element(auth)
        first_state = get_switch_state(switch)

    with allure.step("First click and check"):
        switch.click()
        WebDriverWait(auth, 10).until(
            lambda d: get_switch_state(get_switch_element(d)) != first_state
        )
        second_state = get_switch_state(get_switch_element(auth))
        assert second_state != first_state, "Состояние не изменилось после первого клика"

    with allure.step("Second click and check"):
        switch = get_switch_element(auth)
        switch.click()
        WebDriverWait(auth, 10).until(
            lambda d: get_switch_state(get_switch_element(d)) == first_state
        )
        final_state = get_switch_state(get_switch_element(auth))
        assert final_state == first_state, "Состояние не вернулось в исходное после второго клика"
