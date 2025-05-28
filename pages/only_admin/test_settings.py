import time
from selenium.webdriver.common.keys import Keys
import re
from conftest import Locators
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def test_interest_rate_field(settings_modal):
    """Тест процентной ставки"""
    interest_input = WebDriverWait(settings_modal, 15).until(
        EC.element_to_be_clickable(Locators.INTEREST_RATE_INPUT))

    test_cases = [
        ("50", "50", "Корректное значение"),
        ("-10", "10", "Отрицательные значения"),
        ("abc", "0", "Буквенные значения"),
        ("150", "15", "Максимальное значение 100"),
        ("1000", "100", "Максимальное значение 100"),
    ]

    for input_value, expected_output, description in test_cases:
        clear_input_field(interest_input)
        interest_input.send_keys(input_value)
        current_value = interest_input.get_attribute("value")
        assert current_value == expected_output, \
            f"{description}. Ввод: '{input_value}', Получено: '{current_value}'"


@pytest.mark.parametrize("field_locator, field_name", [
    (Locators.VARIABLE_N2_INPUT, "Переменная 2"),
    (Locators.VARIABLE_N3_INPUT, "Переменная 3")
], ids=["variable_2", "variable_3"])
def test_variable_fields(settings_modal, field_locator, field_name):
    """Тест полей переменных"""
    field = WebDriverWait(settings_modal, 15).until(
        EC.element_to_be_clickable(field_locator))

    test_cases = [
        ("1234567890", "1234567890", "Цифры короткое число"),
        ("1" * 310, "∞", "Более 309 символов"),
        ("abc123", "123", "Буквенные символы недопустимы"),
        ("!@#$", "0", "Спецсимволы недопустимы"),
        ("  456  ", "456", "Пробелы в начале и конце"),
        ("12 34 56", "123456", "Пробелы внутри строки"),
        ("abc!@#123xyz", "123", "Буквы и спецсимволы среди цифр"),
        ("\xa0123\xa0456\xa0789", "123456789", "Невидимые символы внутри строки")
    ]

    for input_value, expected_output, description in test_cases:
        clear_input_field(field)
        field.send_keys(input_value)
        current_value = field.get_attribute("value")
        current_value_clean = clean_string(current_value.strip())

        input_digits_only = re.sub(r'\D', '', input_value)
        if len(input_digits_only) > 309:
            expected_field_value = '∞'
            assert current_value_clean == expected_field_value, \
                f"{description} (более 309 символов). Ввод: '{input_value}', Получено: '{current_value}'"
            continue

        if not re.sub(r'\D', '', current_value):
            expected_field_value = '0'
        else:
            expected_field_value = expected_output

        assert current_value_clean == expected_field_value, \
            f"{field_name}: {description}. Ввод: '{input_value}', Ожидается: '{expected_field_value}', Получено: '{current_value}'"


def find_switch_element(driver, locators):
    for locator in locators:
        elements = driver.find_elements(*locator)
        if elements:
            return elements[0]
    return None


def get_switch_state(switch_element):
    class_attr = switch_element.get_attribute("class")
    return "checked" in class_attr or "active" in class_attr


def test_switch(auth, settings_modal):
    """Тест переключателя"""
    switch = find_switch_element(auth, Locators.SWITCH_LOCATORS)

    if switch is None:
        pytest.fail("Не удалось найти элемент switch на странице")

    initial_state = get_switch_state(switch)
    switch.click()
    time.sleep(0.5)

    new_state = get_switch_state(switch)
    if new_state == initial_state:
        auth.save_screenshot("switch_not_changed.png")
        pytest.fail("Состояние switch не изменилось после клика")

    switch.click()
    time.sleep(0.5)

    final_state = get_switch_state(switch)
    if final_state != initial_state:
        auth.save_screenshot("switch_not_reset.png")
        pytest.fail("Не удалось вернуть switch в исходное состояние")