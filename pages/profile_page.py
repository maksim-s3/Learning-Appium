import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    _button_login_locator = '//*[contains(@resource-id, "login_button")]'
    _button_favourites_locator = '//*[contains(@resource-id, "button_text")][@text="Избранное"]'
    _text_selected_city_locator = '//*[contains(@resource-id, "settlement_text")]'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "toolbar")]//*[contains(@text, "Профиль")]')

    @property
    def button_login_is_displayed(self):
        logger.info(f'Проверить видимость кнопки "Войти"')
        return self._driver.find_element(By.XPATH, self._button_login_locator).is_displayed()

    @property
    def selected_city(self):
        logger.info(f'Вернуть текущий выбранный город')
        return self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._text_selected_city_locator)).text

    def button_favourites_click(self):
        logger.info(f'Кликнуть на кнопке "Избранное"')
        self._driver.find_element(By.XPATH, self._button_favourites_locator).click()

    def button_login_click(self):
        logger.info(f'Кликнуть на кнопке "Войти"')
        self._driver.find_element(By.XPATH, self._button_login_locator).click()
