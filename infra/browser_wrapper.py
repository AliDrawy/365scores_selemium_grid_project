from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from .config_loader import ConfigLoader
from selenium.common.exceptions import WebDriverException
from contextlib import contextmanager


class WebDriverWrapper:
    def __init__(self):
        self.settings = ConfigLoader.load_settings()

    def initialize_webdriver(self, browser_name):
        """Initializes a WebDriver instance based on browser preferences."""
        browser_preferences = self.fetch_browser_preferences(browser_name)
        hub_url = self.settings.get("hub")
        if self.settings.get("grid"):
            try:
                driver = webdriver.Remote(command_executor=hub_url, options=browser_preferences)
                return driver
            except WebDriverException as e:
                print(f"Failed to initialize WebDriver session: {e}")
                raise
        else:
            raise ValueError("Grid support is not configured.")

    def fetch_browser_preferences(self, browser_name):
        """Fetches browser preferences for the specified browser."""
        if browser_name == 'chrome':
            return webdriver.ChromeOptions()
        elif browser_name == 'firefox':
            return webdriver.FirefoxOptions()
        elif browser_name == 'edge':
            return webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @contextmanager
    def webdriver_session(self, browser_name):
        driver = self.initialize_webdriver(browser_name)
        try:
            yield driver
        finally:
            if driver is not None:
                driver.quit()

    def setup_wait_condition(self, driver, timeout=10):
        """Sets up a WebDriverWait condition for the specified driver."""
        return WebDriverWait(driver, timeout)

    def open_website(self, driver, url):
        """Navigates to a specified URL using the given driver."""
        driver.get(url)
        self.setup_wait_condition(driver, 10).until(lambda driver: url == driver.current_url)
