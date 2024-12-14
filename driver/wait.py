from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from driver import AppiumDriver


class AppiumDriverWait:
    __wait = None

    @classmethod
    def get_wait(cls):
        driver = AppiumDriver.get_driver()
        if not cls.__wait:
            cls.__wait = WebDriverWait(
                driver,
                15,
                poll_frequency=1,
                ignored_exceptions=[
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                    NoSuchElementException
                ])
        return cls.__wait
