import unittest
import concurrent.futures
from selenium.webdriver.support.wait import WebDriverWait
from infra.browser_wrapper import WebDriverWrapper
from logic.logic import SiteNavigationHandler

class ParallelGridTest(unittest.TestCase):
    def setUp(self):
        self.web_driver_wrapper = WebDriverWrapper()

    def test_parallel_execution_across_browsers(self):
        """Executes tests in parallel across different browsers."""
        browsers = self.web_driver_wrapper.settings["browser_types"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(browsers)) as executor:
            futures = []
            for browser in browsers:
                future = executor.submit(self.run_specific_browser_test, browser)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.fail(f"An error occurred during the tests: {e}")

    def run_specific_browser_test(self, browser_name):
        """Executes test for a specific browser, encapsulating setup and teardown."""
        with self.web_driver_wrapper.webdriver_session(browser_name) as driver:
            driver.maximize_window()
            wait = WebDriverWait(driver, 10)  # Adjusted from 2 to 10 seconds
            self.navigation_handler = SiteNavigationHandler()

            # Proceed with test actions within the try block
            try:
                self.verify_homepage_title(driver, wait)
                self.go_to_football_section(driver, wait)
                self.go_to_basketball_section(driver, wait)
                self.go_to_tennis_section(driver, wait)
                self.go_to_hockey_section(driver, wait)
            finally:
                pass  # driver.quit() is handled by the context manager

    def verify_homepage_title(self, driver, wait):
        """Checks the title of the homepage."""
        expected_url = self.web_driver_wrapper.settings["url"]["english"]
        self.web_driver_wrapper.open_website(driver, expected_url)
        expected_title = "365Scores - Livescore, Results, Fixtures, News and Stats"
        actual_url, actual_title = self.navigation_handler.verify_page_title_and_url(expected_url, expected_title, driver, wait)
        self.assertIn(expected_url, actual_url, "The page URL is not as expected.")
        self.assertEqual(expected_title, actual_title, "The homepage title does not match the expected value.")

    def go_to_section(self, driver, wait, section, expected_url):
        """Navigates to a specific section and verifies the URL."""
        self.web_driver_wrapper.open_website(driver, self.web_driver_wrapper.settings["url"]["hebrew"])
        actual_url = self.navigation_handler.go_to_website_section(section, expected_url, driver, wait)
        self.assertIn(expected_url, actual_url, f"Did not navigate to the {section.capitalize()} section correctly.")

    def go_to_football_section(self, driver, wait):
        self.go_to_section(driver, wait, "football", "https://www.365scores.com/he/football")

    def go_to_basketball_section(self, driver, wait):
        self.go_to_section(driver, wait, "basketball", "https://www.365scores.com/he/basketball")

    def go_to_tennis_section(self, driver, wait):
        self.go_to_section(driver, wait, "tennis", "https://www.365scores.com/he/tennis")

    def go_to_hockey_section(self, driver, wait):
        self.go_to_section(driver, wait, "hockey", "https://www.365scores.com/he/hockey")

if __name__ == "__main__":
    unittest.main()
