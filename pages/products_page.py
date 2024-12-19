import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    _button_filters_locator = '//*[@resource-id="ru.dns.shop.android:id/filter_button"]'
    _text_products_name_locator = '//*[@resource-id="ru.dns.shop.android:id/product_title_text"]'
    _text_products_price_locator = '//*[@resource-id="ru.dns.shop.android:id/current_price_text"]'
    _text_current_catogory_locator = '//*[@resource-id="ru.dns.shop.android:id/toolbar"]//android.widget.TextView'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/filter_list"]')

    @property
    def current_category(self):
        logger.info(f'Вернуть текущую категорию товаров')
        return self._wait.until(
            lambda e: self._driver.find_element(
                By.XPATH, self._text_current_catogory_locator)).text

    def button_filters_click(self):
        logger.info(f'Кликнуть на кнопке фильтров')
        self._driver.find_element(By.XPATH, self._button_filters_locator).click()

    def scroll_to_product_by_index(self, index: int = 0):
        logger.info(f'Проскролить экран до {index} доступного товара')
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._text_products_name_locator))

        # index раз скролим от нижнего товара до верхнего
        for i in range(index):
            elements = self._driver.find_elements(By.XPATH, self._text_products_name_locator)
            if len(elements) < 2:
                raise NoSuchElementException(f"Товаров меньше чем {index}")
            self._driver.scroll(elements[1], elements[0])

    def get_name_and_price_product(self, index: int):
        logger.info(f'Вернуть название и цену {index} доступного товара на экране')
        self.scroll_to_product_by_index(index)

        product_name = self._driver.find_elements(By.XPATH, self._text_products_name_locator)[0].text
        product_price = self._driver.find_elements(By.XPATH, self._text_products_price_locator)[0].text
        return product_name, product_price

    def open_product_card_by_index(self, index: int):
        logger.info(f'Кликнуть на {index} доступном товаре')
        self.scroll_to_product_by_index(index)
        self._wait.until(
            lambda e: self._driver.find_elements(By.XPATH, self._text_products_name_locator)[0]).click()
