import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
logger = logging.getLogger(__name__)


class FiltersPage(BasePage):
    _filter_pattern_locator = '//*[contains(@resource-id, "title_text")][@text="{}"]'
    _count_filters_locator = '//*[contains(@resource-id, "title_text")]'
    _checkbox_pattern_locator = '//*[contains(@resource-id, "check")][contains(@text, "{}")]'
    _count_checkbox_locator = '//*[contains(@resource-id, "check")]'
    _button_apply_locator = '//*[contains(@resource-id, "apply_button")]'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "extended_mode_text")]')

    def select_filter(self, filter_name: str):
        logger.info(f"Кликнуть на фильтре {filter_name}")
        count_filters = len(self._driver.find_elements(By.XPATH, self._count_filters_locator))
        for _ in range(count_filters):
            try:
                self._driver.find_element(By.XPATH, self._filter_pattern_locator.format(filter_name)).click()
                break
            except NoSuchElementException:
                self._driver.swipe(100, 400, 200, 100)
        else:
            raise NoSuchElementException

    def select_checkbox(self, checkbox_name: str):
        logger.info(f"Выбрать чекбокс {checkbox_name}")
        count_checkbox = len(self._driver.find_elements(By.XPATH, self._count_checkbox_locator))
        for _ in range(count_checkbox):
            try:
                self._driver.find_element(By.XPATH, self._checkbox_pattern_locator.format(checkbox_name)).click()
                break
            except NoSuchElementException:
                self._driver.swipe(400, 400, 400, 100)
        else:
            raise NoSuchElementException

    def button_apply_click(self):
        logger.info(f"Кликнуть на кнопке 'Применить'")
        self._wait.until(
            lambda e: self._driver.find_element(By.XPATH, self._button_apply_locator)).click()
