import logging
from abc import ABC

from driver import AppiumDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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

    def scroll_to(self, count_locator: str, pattern_locator: str, element_text: str):
        """Проскролить список элементов до целевого

        :param count_locator: общий локатор для нахождения множества элементов
        :param pattern_locator: шаблон для нахождения уникального элемента
        :param element_text: текст элемента
        """

        logger.info(f"Скролим список элементов до {element_text}")
        # Ждем появления списка элементов
        self._wait.until(lambda e: self._driver.find_elements(By.XPATH, count_locator))

        bottom_element = None
        while True:
            # Ищем нужный элемент. Если есть выходим из цикла
            target_element = self._driver.find_elements(
                By.XPATH, pattern_locator.format(element_text))
            if target_element:
                return

            # Если нет, то ищем все элементы на экране
            elements = self._driver.find_elements(By.XPATH, count_locator)
            if not elements or len(elements) < 2 or bottom_element == elements[-1]:
                # Если нет элементов, их меньше 2 или после скрола нижний элемент
                # тот же что с прошлой итерации - значит прокрутили до конца
                raise NoSuchElementException(f"Элемент {element_text} не найден")
            bottom_element = elements[-1]
            # Скролим от нижнего элемента до верхнего
            logger.info(f"Скролим список элементов от {elements[-1].text} до {elements[0].text}")
            self._driver.scroll(elements[-1], elements[0])

