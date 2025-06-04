import pytest
from selenium.webdriver.common.by import By

class Locators:
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REQUIRED_MASSAGE = (By.XPATH, "//div[text()='Обязательное поле']")
    INVALID_EMAIL_MASSAGE = (By.XPATH, "//div[text()='Введите корректный e-mail']")
    INVALID_MASSAGE = (By.XPATH, "//div[text()='Неверные логин или пароль']")
    FORGOT_PASSWORD_BUTTON = (By.LINK_TEXT, "Забыли пароль?")
    FORGOT_EMAIL_BUTTON = (By.LINK_TEXT, "Не помню e-mail")
    PHONE_FIELD = (By.ID, "phoneNumber")
    COMPANY_FIELD = (By.XPATH, "//div[contains(@class, 'organizationName')]//input[@type='text']")
    FIO_FIELD = (By.XPATH, "//div[contains(@class, 'fullName')]//input[@type='text']")
    CHECK_BOX = (By.CLASS_NAME, "Checkbox__iconContainer--pbmVy")
    MODAL_WINDOW = (By.ID, "modal-container-id")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class, 'Button__mediumSizeButton')]//div[text()='Закрыть']/..")



@pytest.fixture(params=[
    {
        "role": "Менеджер DSM",
        "email": "auto_manager@gmail.com",
        "password": "z1crjhjcnm",

    },
    {
        "role": "Руководитель DSM",
            "email": "auto_ruk@gmail.com",
        "password": "z1crjhjcnm",

    },
    {
        "role": "Администратор DSM",
        "email": "auto_admin@gmail.com",
        "password": "z1crjhjcnm",

    },
    {
        "role": "Руководитель клиента",
        "email": "auto_ruk_cli@gmail.com",
        "password": "z1crjhjcnm",

    },
    {
        "role": "Директор клиента",
        "email": "auto_dir_cli@gmail.com",
        "password": "z1crjhjcnm",

    },
{
        "role": "Директор клиента",
        "email": "auto_employee_cli@gmail.com",
        "password": "z1crjhjcnm",

    }
])
def auth_data(request):
    return request.param


@pytest.fixture
def invalid_credentials():
    return [
        {
            "email": "wrong@gmail.com",
            "password": "wrongpassword"
        },
        {
            "email": "manager@gmail.com",
            "password": "wrongpassword"
        },
        {
            "email": "",
            "password": "123456789"
        },
        {
            "email": "admin@gmail.com",
            "password": ""
        },
        {
            "email": "1.com",
            "password": "123456789"
        },
        {
            "email": "1@com",
            "password": "123456789"
        },
        {
            "email": "1",
            "password": "123456789"
        }
    ]