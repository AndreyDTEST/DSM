import pytest
from selenium.webdriver.common.by import By

class Locators:
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")




@pytest.fixture(params=[
    {
        "role": "Менеджер DSM",
        "email": "manager@gmail.com",
        "password": "123456789",

    },
    {
        "role": "Руководитель DSM",
        "email": "r@gmail.com",
        "password": "123456789",

    },
    {
        "role": "Администратор DSM",
        "email": "admin@gmail.com",
        "password": "123456789",

    },
    {
        "role": "Руководитель клиента",
        "email": "ruk@gmail.com",
        "password": "123456789",

    },
    {
        "role": "Директор клиента",
        "email": "dir@gmail.com",
        "password": "123456789",

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
