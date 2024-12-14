import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    _empty_content_locator = '//*[contains(@resource-id, "empty_content_view")]'
    _button_go_to_catalog_locator = '//*[contains(@resource-id, "empty_content_action_button")]'
    _text_products_name_locator = '//*[contains(@resource-id, "product_title_text")]'
    _text_product_name_pattern_locator = '//*[contains(@resource-id, "product_title_text")][@text, "{}"]'
    _text_product_price_with_name_locator = ('//*[contains(@text, "{}")]/following-sibling::*'
                                             '//*[contains(@resource-id, "cart_item_sum_view_current_sum_text")]')
    _button_delete_product_with_name_locator = ('//*[contains(@text, "{}")]/following-sibling::*'
                                                '//*[contains(@resource-id, "decrement_button")]')
    _text_total_sum_cart_locator = '//*[contains(@resource-id, "total_sum_text")]'
    _button_confirm_delete_locator = '//*[contains(@resource-id, "positive_button")]'
    _dialog_delete_product_locator = '//*[contains(@resource-id, "design_bottom_sheet")]'
    _snack_bar_locator = '//*[contains(@resource-id, "snackbar_text")]'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "title_text")][contains(@text, "Корзина")]')

    @property
    def is_empty(self):
        logger.info('Проверка корзины на наличие товаров')
        elements = self._driver.find_elements(By.XPATH, self._empty_content_locator)
        return True if elements else False

    @property
    def button_go_to_catalog_is_displayed(self):
        logger.info(f'Получение кнопки перехода в каталог')
        return self._driver.find_element(By.XPATH, self._button_go_to_catalog_locator)

    @property
    def total_sum_cart(self):
        logger.info(f'Получение полной стоимости товаров в корзине')
        total_sum_element = []
        while not total_sum_element:
            self._driver.swipe(100, 400, 100, 100)
            total_sum_element = self._driver.find_elements(By.XPATH, self._text_total_sum_cart_locator)
        return total_sum_element[0].text

    def wait_appear_products(self):
        logger.info('Ожидание загрузки товаров')
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._text_products_name_locator))

    def wait_empty_cart(self):
        logger.info('Ожидание освобождения корзины')
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._empty_content_locator))

    def find_product_in_cart(self, product_name: str):
        logger.info(f'Поиск товара {product_name} в корзине')
        # скролим до видимости нужного товара
        bottom_element = None
        while True:
            # Ищем нужный товар
            target_product = self._driver.find_elements(
                By.XPATH, self._text_product_name_pattern_locator.format(product_name))
            if target_product:
                return True

            # Если нет, то ищем все товары на экране
            elements = self._driver.find_elements(By.XPATH, self._text_products_name_locator)
            if not elements or bottom_element == elements[-1]:
                # Если после скролла нижний элемент тот же что с прошлой итерации
                # или продуктов в корзине нет - значит прокрутили до конца
                return False
            bottom_element = elements[-1]
            self._driver.scroll(elements[-1], elements[0])

    def get_price_for_product(self, product_name: str):
        logger.info(f'Получение стоимости товара {product_name} в корзине')
        self.wait_appear_products()
        if not self.find_product_in_cart(product_name):
            raise NoSuchElementException(f"Товар {product_name} не найден в корзине")

        while True:
            products = self._driver.find_elements(By.XPATH, self._text_products_name_locator)
            for product in products:
                if product.text in product_name:
                    return self._driver.find_element(
                        By.XPATH, self._text_product_price_with_name_locator.format(product.text)).text
                self._driver.swipe(100, 400, 100, 100)

    def button_remove_product_click(self, product_name: str):
        logger.info(f'Нажатие кнопки удаление товара')
        self.wait_appear_products()
        if not self.find_product_in_cart(product_name):
            raise NoSuchElementException(f"Товар {product_name} не найден в корзине")

        while True:
            products = self._driver.find_elements(By.XPATH, self._text_products_name_locator)
            for product in products:
                if product.text in product_name:
                    self._driver.find_element(
                        By.XPATH, self._button_delete_product_with_name_locator.format(product.text)
                    ).click()
                    return

    def dialog_delete_product_is_displayed(self):
        logger.info('Проверка отображения диалога удаления товара')
        return self._wait.until(
            lambda e: self._driver.find_element(
                By.XPATH, self._dialog_delete_product_locator)
        ).is_displayed()

    def button_delete_confirm_click(self):
        logger.info('Нажатие кнопки подтверждения удаления товара')
        self._driver.find_element(By.XPATH, self._button_confirm_delete_locator).click()

    def wait_snack_bar(self):
        logger.info('Ожидание подтверждения удаления товара')
        return self._wait.until(
            lambda e: self._driver.find_element(
                By.XPATH, self._snack_bar_locator)
        ).is_displayed()
