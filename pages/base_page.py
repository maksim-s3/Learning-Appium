import logging
from abc import ABC

from driver import AppiumDriver
from selenium.webdriver.common.by import By

from driver.wait import AppiumDriverWait
logger = logging.getLogger(__name__)


class BasePage(ABC):
    _anchor_page_locator = None
    _driver = None
    _wait = None

    def __init__(self, anchor_page_locator):
        self._anchor_page_locator = anchor_page_locator
        self._driver = AppiumDriver.get_driver()
        self._wait = AppiumDriverWait.get_wait()

    @property
    def is_open(self):
        logger.info(f"Проверка доступности страницы {self.__class__}")
        return self._wait.until(
            lambda e: self._driver.find_element(
                By.XPATH, self._anchor_page_locator)
        ).is_displayed()
