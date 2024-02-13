from django.test import TestCase
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class NavigationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000"
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 20)  # Increase the timeout

    def wait_for_element(self, by, value):
        try:
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None

    def wait_for_header(self, header_text):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, f'//h2[contains(text(), "{header_text}")]')))
        except TimeoutException:
            return None

    def test_navigation_flow(self):
        # Navigate directly to the login page
        self.driver.get(self.base_url + '/login')
        expected_title = "LOGIN"
        self.assertIn(expected_title.upper(), self.driver.title.upper())

        # Perform login
        username = self.wait_for_element(By.NAME, 'username')
        password = self.wait_for_element(By.NAME, 'password')
        login_button = self.wait_for_element(By.XPATH, '//input[@type="submit"]')

        username.send_keys("admin")
        password.send_keys("admin")
        login_button.click()

        # Wait for the "Services" link to be present and clickable after login (indicating the dashboard loaded)
        services_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Services")))
        self.assertIsNotNone(services_link, "Services link not found")
        services_link.click()

        # Wait for the services page to load by waiting for the "Services" header
        self.wait_for_header("Services")

        # Navigate to edit service page
        edit_service_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'edit-service-button')))
        self.assertIsNotNone(edit_service_button, "Edit Service button not found")
        edit_service_button.click()

        # Wait for the edit service page to load by waiting for the "Edit Service" header
        self.wait_for_header("Edit Service")

        # Explicitly wait for the "Edit Service Update" button to be present
        edit_service_update = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]')))

        # Check if the element is found before attempting to click
        if edit_service_update is not None:
            service_name = self.wait_for_element(By.NAME, 'name')
            description = self.wait_for_element(By.NAME, 'description')
            price = self.wait_for_element(By.NAME, 'price')

            service_name.clear()  # Clear existing text if any
            service_name.send_keys("Test Service")
            description.clear()
            description.send_keys("This is a test service.")
            price.clear()
            price.send_keys("100")

            # Click on the "Edit Service Update" button
            edit_service_update.click()
        else:
            current_url = self.driver.current_url
            error_message = f"Edit Service Update button not found. Current URL: {current_url}"
            self.fail(error_message)

        try:
            self.wait.until(EC.url_contains('servicedetails'))  # You can customize this based on the actual URL pattern
        except TimeoutException:
            print(f"Current URL: {self.driver.current_url}")
            raise

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
