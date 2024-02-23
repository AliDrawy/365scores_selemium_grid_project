from infra.page_base import PageBase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SiteNavigationHandler(PageBase):
    BTN_NOTICE_AGREE = (By.XPATH, '//button[@id="didomi-notice-agree-button"]')
    SVG_CLOSE_ICON = "//div/*[local-name()='svg' and @viewBox='0 0 24 24']/*[local-name()='path' and @d = 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z']"
    SECTION_PATHS = {
        'football': "//button[.//div[text()='כדורגל']]",
        'basketball': "//button[.//div[text()='כדורסל']]",
        'tennis': "//button[.//div[text()='טניס']]",
        'hockey': "//button[.//div[text()='הוקי']]"
    }

    def verify_page_title_and_url(self, expected_url, expected_title, driver, wait):
        """Verifies the page title and URL after navigating to the expected URL."""
        wait.until(lambda driver: expected_url == driver.current_url)
        wait.until(lambda driver: expected_title == driver.title)
        wait.until(EC.title_is(expected_title))
        actual_url = driver.current_url
        actual_title = driver.title
        return actual_url, actual_title

    def attempt_element_click(self, primary_xpath, fallback_xpath, driver):
        wait = WebDriverWait(driver, 5)  # Up to 5 seconds wait
        try:
            wait.until(EC.element_to_be_clickable(self.BTN_NOTICE_AGREE)).click()
        except Exception as E:
            print(E)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, primary_xpath))).click()
        except Exception as E:
            print(E)
            wait.until(EC.element_to_be_clickable((By.XPATH, fallback_xpath))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, primary_xpath))).click()

    def go_to_website_section(self, section, expected_url, driver, wait):
        """Navigates to a specific section of the site and verifies the URL."""
        self.attempt_element_click(self.SECTION_PATHS[section], self.SVG_CLOSE_ICON, driver)
        wait.until(lambda driver: expected_url == driver.current_url)
        current_url = driver.current_url
        return current_url
