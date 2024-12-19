import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class PermissionAlert(BasePage):
    _button_allow_locator = '//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
    _button_while_using_locator = '//*[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'

    def __init__(self):
        super().__init__('//*[@resource-id="com.android.permissioncontroller:id/grant_dialog"]')

    def wait_request_permission(self):
        logger.info('Ожидание запроса разрешения на экране')
        self._wait.until(lambda e: self._driver.find_element(By.XPATH, self._anchor_page_locator))

    def allow_click(self):
        logger.info('Кликнуть на кнопке "Разрешить"')
        self.wait_request_permission()
        button = self._driver.find_element(By.XPATH, self._button_allow_locator)
        button.click()

    def while_using_the_app_click(self):
        logger.info('Кликнуть на кнопке "Разрешить пока используется"')
        self.wait_request_permission()
        button = self._driver.find_element(By.XPATH, self._button_while_using_locator)
        button.click()
