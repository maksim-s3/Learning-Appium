import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage

logger = logging.getLogger(__name__)


class FavoritesPage(BasePage):
    _empty_content_locator = '//*[@resource-id="ru.dns.shop.android:id/empty_content_view"]'
    _button_login_locator = '//*[@resource-id="ru.dns.shop.android:id/login_button"]'
    _button_go_to_catalog_locator = '//*[@resource-id="ru.dns.shop.android:id/empty_content_action_button"]'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/toolbar"]//*[@text="Избранное"]')

    @property
    def is_empty(self):
        logger.info(f'Проверить что список избранного пуст')
        elements = self._driver.find_elements(By.XPATH, self._empty_content_locator)
        return True if elements else False

    @property
    def button_login_is_displayed(self):
        logger.info(f'Проверить что отображается кнопка "Войти"')
        return self._driver.find_element(By.XPATH, self._button_login_locator)

    @property
    def button_go_to_catalog_is_displayed(self):
        logger.info(f'Проверить что отображается кнопка "Перейти в каталог"')
        return self._driver.find_element(By.XPATH, self._button_go_to_catalog_locator)
