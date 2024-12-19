import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
logger = logging.getLogger(__name__)


class CatalogPage(BasePage):
    _category_name_pattern_locator = '//*[@resource-id="ru.dns.shop.android:id/title_text"][@text="{}"]'
    _categories_locator = '//*[@resource-id="ru.dns.shop.android:id/title_text"]'
    _text_current_catogory_locator = '//*[@resource-id="ru.dns.shop.android:id/toolbar"]//android.widget.TextView'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/chevron_image"]')

    @property
    def current_category(self):
        logger.info(f"Вернуть текущую категорию в каталоге")
        return self._wait.until(lambda e: self._driver.find_element(By.XPATH, self._text_current_catogory_locator)).text

    def select_category(self, category_name: str):
        logger.info(f"Нажать на категорию {category_name}")
        self.scroll_to(
            self._categories_locator,
            self._category_name_pattern_locator,
            category_name)
        self._driver.find_element(
            By.XPATH,
            self._category_name_pattern_locator.format(category_name)).click()
