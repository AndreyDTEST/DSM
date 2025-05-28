from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def test_invoice_approve(finance_section):
    """Тест для проверки функционала согласования счета"""
    browser = finance_section



