import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class MainPage(BasePage):
    _text_permission_locator = '//*[@resource-id="ru.dns.shop.android:id/permission_message"]'
    _text_current_selected_city_locator = '//*[@resource-id="ru.dns.shop.android:id/change_current_settlement_button"]'
    _text_product_items_locator = '//*[@resource-id="ru.dns.shop.android:id/product_title_text"]'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/app_bar"]'
                         '//*[@resource-id="ru.dns.shop.android:id/logo_image"]')

    @property
    def current_selected_city(self):
        logger.info(f"Получить текущий выбранный город")
        return self._driver.find_element(By.XPATH, self._text_current_selected_city_locator).text

    def get_name_product_item_by_index(self, index: int):
        logger.info(f"Получить название товара на главное странице по индексу")
        products = self._driver.find_elements(By.XPATH, self._text_product_items_locator)
        return products[index].text
