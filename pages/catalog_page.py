import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
logger = logging.getLogger(__name__)


class CatalogPage(BasePage):
    _category_name_pattern_locator = '//*[contains(@resource-id, "title_text")][@text="{}"]'
    _categories_locator = '//*[contains(@resource-id, "title_text")]'
    _text_current_catogory_locator = '//*[contains(@resource-id, "toolbar")]//android.widget.TextView'

    def __init__(self):
        super().__init__('//*[contains(@resource-id, "chevron_image")]')

    @property
    def current_category(self):
        logger.info(f"Вернуть текущую категорию в каталоге")
        return self._wait.until(lambda e: self._driver.find_element(By.XPATH, self._text_current_catogory_locator)).text

    def select_category(self, category_name: str):
        logger.info(f"Нажать на категорию {category_name}")
        self._wait.until(lambda e: self._driver.find_elements(By.XPATH, self._categories_locator))

        bottom_element = None
        while True:
            # Ищем нужную категорию. Если есть - кликаем на нее
            target_category = self._driver.find_elements(By.XPATH, self._category_name_pattern_locator.format(category_name))
            if target_category:
                target_category[0].click()
                return

            # Если нет, то ищем все категории на экране
            elements = self._wait.until(lambda e: self._driver.find_elements(By.XPATH, self._categories_locator))
            if bottom_element == elements[-1]:
                # Если после скролла нижний элемент тот же что с прошлой итерации - значит прокрутили до конца
                raise NoSuchElementException(f"Категория {category_name} не найдена")
            bottom_element = elements[-1]
            self._driver.scroll(elements[-1], elements[0])
