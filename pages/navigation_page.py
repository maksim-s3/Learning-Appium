import logging
import re

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class NavigationPage(BasePage):
    _button_home_locator = '//*[@resource-id="ru.dns.shop.android:id/nav_home"]'
    _button_outlets_locator = '//*[@resource-id="ru.dns.shop.android:id/nav_outlets"]'
    _button_catalog_locator = '//*[@resource-id="ru.dns.shop.android:id/nav_catalog"]'
    _button_cart_locator = '//*[@resource-id="ru.dns.shop.android:id/nav_cart"]'
    _button_profile_locator = '//*[@resource-id="ru.dns.shop.android:id/nav_profile"]'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/navigation_bar_item_icon_view"]')

    @property
    def number_items_in_cart(self):
        logger.info(f"Получить количество товаров в корзине")
        text = self._driver.find_element(By.XPATH, self._button_cart_locator).get_attribute("content-desc")
        regexp = r"Корзина\,\ (\d+)\ новое\ уведомление"
        result = re.search(regexp, text)
        if result:
            return int(result.groups()[0])
        else:
            return 0

    def open_cart(self):
        logger.info(f"Перейти на вкладку корзины")
        self._driver.find_element(By.XPATH, self._button_cart_locator).click()

    def open_profile(self):
        logger.info(f"Перейти на вкладку профиль")
        self._driver.find_element(By.XPATH, self._button_profile_locator).click()

    def open_catalog(self):
        logger.info(f"Перейти на вкладку каталог")
        self._driver.find_element(By.XPATH, self._button_catalog_locator).click()
