import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
logger = logging.getLogger(__name__)


class SelectCityPage(BasePage):
    _text_current_city_locator = '//*[@resource-id="ru.dns.shop.android:id/current_settlement_text"]'
    _button_change_city = '//*[@resource-id="ru.dns.shop.android:id/change_current_settlement_button"]'
    _button_confirm_locator = '//*[@resource-id="ru.dns.shop.android:id/confirm_current_settlement_button"]'
    _input_search_city = '//*[@resource-id="ru.dns.shop.android:id/search_edit"]'
    _text_city_item_pattern_locator = '//*[@resource-id="ru.dns.shop.android:id/settlement_name_text"][@text="{}"]'
    _list_of_cities_locator = '//*[@resource-id="ru.dns.shop.android:id/settlement_name_text"]'

    def __init__(self):
        super().__init__('//*[@resource-id="ru.dns.shop.android:id/current_settlement_title_text"]')

    @property
    def current_city(self):
        logger.info('Вернуть текущий выбранный город в приложении')
        return self._driver.find_element(By.XPATH, self._text_current_city_locator).text

    def change_city_click(self):
        logger.info('Кликнуть на кнопке "Сменить город"')
        self._driver.find_element(By.XPATH, self._button_change_city).click()

    def select_city(self, city: str):
        logger.info(f'Выбрать город {city}')
        self._wait.until(lambda e: self._driver.find_element(By.XPATH, self._list_of_cities_locator))
        input_element = self._driver.find_element(By.XPATH, self._input_search_city)
        input_element.click()
        input_element.send_keys(city)
        self._driver.find_element(By.XPATH, self._text_city_item_pattern_locator.format(city)).click()

    def confirm_click(self):
        logger.info(f'Кликнуть на кнопке "Подтвердить"')
        self._driver.find_element(By.XPATH, self._button_confirm_locator).click()
