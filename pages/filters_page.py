import logging

from selenium.webdriver.common.by import By
from .base_page import BasePage
logger = logging.getLogger(__name__)


class FiltersPage(BasePage):
    _filter_pattern_locator = '//*[@resource-id="ru.dns.shop.android:id/title_text"][@text="{}"]'
    _count_filters_locator = '//*[@resource-id="ru.dns.shop.android:id/title_text"]'
    _checkbox_pattern_locator = '//*[@resource-id="ru.dns.shop.android:id/check"][contains(@text, "{}")]'
    _count_checkbox_locator = '//*[@resource-id="ru.dns.shop.android:id/check"]'
    _button_apply_locator = '//*[@resource-id="ru.dns.shop.android:id/apply_button"]'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/extended_mode_text"]')

    def select_filter(self, filter_name: str):
        logger.info(f"Кликнуть на фильтре {filter_name}")
        self.scroll_to(self._count_filters_locator, self._filter_pattern_locator, filter_name)
        self._driver.find_element(By.XPATH, self._filter_pattern_locator.format(filter_name)).click()

    def select_checkbox(self, checkbox_name: str):
        logger.info(f"Выбрать чекбокс {checkbox_name}")
        self._driver.find_element(By.XPATH, self._checkbox_pattern_locator.format(checkbox_name)).click()

    def button_apply_click(self):
        logger.info(f"Кликнуть на кнопке 'Применить'")
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._button_apply_locator)).click()
