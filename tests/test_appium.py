from driver import AppiumDriver


class TestAppium:
    def test_appium(self):
        AppiumDriver.get_driver().quit()
