import pytest
from selenium.webdriver.common.by import By

class Locators:
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")




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