import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    _button_skip_auth_locator = '//*[contains(@resource-id, "skip_auth_button")]'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "skip_auth_button")]')

    def skip_auth_click(self):
        logger.info('Кликнуть на кнопке "Войти позже""')
        button = self._driver.find_element(By.XPATH, self._button_skip_auth_locator)
        button.click()
