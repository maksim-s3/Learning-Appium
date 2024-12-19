import logging
import time

import allure
import pytest

import pages
from driver import AppiumDriver
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver(request):
    driver = AppiumDriver.get_driver()

    def finalizer():
        driver.quit()

    request.addfinalizer(finalizer)
    yield driver


@pytest.fixture(scope="session")
def clear_app(driver):
    # Удаляем сохраненные данные приложения
    driver.execute_script("mobile: clearApp", {'appId': "ru.dns.shop.android"})


@pytest.fixture(scope="session")
def application(driver, request):
    # Закрываем приложение если оно осталось активным с прошлого теста
    driver.terminate_app("ru.dns.shop.android")
    # Запускаем приложение
    driver.activate_app("ru.dns.shop.android")

    def finalizer():
        # Закрываем приложение после теста
        driver.terminate_app("ru.dns.shop.android")

    request.addfinalizer(finalizer)
    yield


@pytest.fixture(scope="session")
def chrome_application(driver, request):
    # Закрываем приложение если оно осталось активным с прошлого теста
    driver.terminate_app("com.android.chrome")
    # Запускаем приложение
    driver.activate_app("com.android.chrome")

    def finalizer():
        # Закрываем приложение после теста
        driver.terminate_app("com.android.chrome")

    request.addfinalizer(finalizer)
    yield


@pytest.fixture(scope="session")
def grant_all_permissions(driver):
    # Выдаем все разрешения приложению
    driver.execute_script("mobile: changePermissions", {'permissions': 'all', 'appPackage': "ru.dns.shop.android"})


class TestAppium:
    def test_first_run_application(self, clear_app, grant_all_permissions, application):
        with allure.step("Выбрать город из параметра"):
            city = "Уфа"
            assert pages.select_city_page.is_open
            pages.select_city_page.change_city_click()
            # pages.permission_alert.while_using_the_app_click()
            pages.select_city_page.select_city(city)
            assert pages.select_city_page.current_city == f"{city}?"
            pages.select_city_page.confirm_click()
            assert pages.login_page.is_open

        with allure.step('Нажать "Войти позже"'):
            pages.login_page.skip_auth_click()
            # pages.permission_alert.wait_request_permission()

        with allure.step("Разрешить отправку уведомлений"):
            # pages.permission_alert.allow_click()
            assert pages.main_page.is_open
            assert pages.main_page.current_selected_city == city

        with allure.step("Нажать на иконку с корзиной в нижнем меню"):
            pages.navigation.open_cart()
            assert pages.cart_page.is_open
            assert pages.cart_page.is_empty
            assert pages.cart_page.button_go_to_catalog_is_displayed

        with allure.step("Перейти в профиль"):
            pages.navigation.open_profile()
            assert pages.profile_page.is_open
            assert pages.profile_page.button_login_is_displayed
            assert pages.profile_page.selected_city == city

        with allure.step('Нажать на кнопку "Избранное"'):
            pages.profile_page.button_favourites_click()
            assert pages.favourites_page.is_open
            assert pages.favourites_page.is_empty
            assert pages.favourites_page.button_login_is_displayed
            assert pages.favourites_page.button_go_to_catalog_is_displayed

    def test_viewing_product(self, application):
        with allure.step("Проверить, что отображается главная страница"):
            assert pages.main_page.is_open

        with allure.step("Нажать на иконку каталога в нижнем меню (список с лупой)"):
            pages.navigation.open_catalog()
            assert pages.catalog_page.is_open

        with allure.step('Перейти в меню "Аксессуары и услуги > Для мобильных устройств > Карты памяти"'):
            pages.catalog_page.select_category('Аксессуары и услуги')
            assert pages.catalog_page.current_category == 'Аксессуары и услуги'

            pages.catalog_page.select_category('Для мобильных устройств')
            assert pages.catalog_page.current_category == 'Для мобильных устройств'

            pages.catalog_page.select_category('Карты памяти')
            assert pages.products_page.current_category == 'Карты памяти'

        with allure.step("Открыть фильтры"):
            pages.products_page.button_filters_click()
            assert pages.filters_page.is_open

        with allure.step("Выбрать объем 128 ГБ"):
            pages.filters_page.select_filter("Объем (ГБ)")
            pages.filters_page.select_checkbox("128 ГБ")
            pages.filters_page.button_apply_click()

        with allure.step("Для первого товара в списке сохранить цену и название"):
            pages.products_page.scroll_to_product_by_index(0)
            product_name, product_price = pages.products_page.get_name_and_price_product(0)

        with allure.step("Открыть страницу первого товара"):
            pages.products_page.open_product_card_by_index(0)
            assert pages.product_card_page.current_price == product_price

        with allure.step("Нажать кнопку 'Купить'"):
            pages.product_card_page.buy_button_click()
            pages.product_card_page.wait_button_in_cart()
            assert pages.navigation.number_items_in_cart == 1

        with allure.step("Нажать на кнопку корзины в нижнем меню"):
            pages.navigation.open_cart()
            assert pages.cart_page.is_open
            assert pages.cart_page.find_product_in_cart(product_name)
            assert pages.cart_page.get_price_for_product(product_name) == product_price
            assert pages.cart_page.total_sum_cart == product_price

        with allure.step("Удалить товар из корзины"):
            pages.cart_page.button_remove_product_click(product_name)
            assert pages.cart_page.dialog_delete_product_is_displayed()
            pages.cart_page.button_delete_confirm_click()
            pages.cart_page.wait_empty_cart()
            assert not pages.cart_page.find_product_in_cart(product_name)
            pages.cart_page.wait_snack_bar()
            assert pages.cart_page.is_empty

    def test_switch_between_applications(self, driver, application, chrome_application):
        driver.activate_app("ru.dns.shop.android")
        assert pages.main_page.is_open
        driver.background_app(-1)

        driver.activate_app("com.android.chrome")
        time.sleep(5)
        search_box = driver.find_element(By.XPATH, "//*[contains(@resource-id, 'search_box_text')]")
        assert search_box.is_displayed()
        driver.background_app(-1)

        driver.activate_app("ru.dns.shop.android")
        assert pages.main_page.is_open
