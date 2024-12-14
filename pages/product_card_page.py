import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage

logger = logging.getLogger(__name__)


class ProductCardPage(BasePage):
    _text_products_name_locator = '//*[contains(@resource-id, "product_title_text")]'
    _text_current_price_locator = '//*[contains(@resource-id, "current_price_text")]'
    _button_buy_pattern_locator = '//*[contains(@resource-id, "buy_button")][@text="{}"]'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "collapsing_toolbar_layout")]')

    @property
    def current_price(self):
        logger.info(f"Вернуть стоимость товара")
        return self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._text_current_price_locator)).text

    def buy_button_click(self):
        logger.info(f"Кликнуть на кнопке 'Купить'")
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._button_buy_pattern_locator.format("Купить"))).click()

    def wait_button_in_cart(self):
        logger.info(f"Дождаться кнопку 'В корзине'")
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._button_buy_pattern_locator.format("В корзине")))
