from appium import webdriver
from appium.options.android import UiAutomator2Options

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    # autoGrantPermissions=True,
)

appium_server_url = 'http://localhost:4723'


class AppiumDriver:
    __driver = None

    @classmethod
    def get_driver(cls):
        if not cls.__driver:
            cls.__driver = webdriver.Remote(
                appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        return cls.__driver
