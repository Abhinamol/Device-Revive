import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000"  # Replace this with your base URL
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_successful_login(self):
        self.driver.get(self.base_url + '/login')
        expected_title = "LOGIN"  # Adjust based on the actual title of the login page
        self.assertIn(expected_title.upper(), self.driver.title.upper())

        # Find username, password, and login button elements
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Enter valid credentials and click login
        username.send_keys("anjali")
        password.send_keys("Anjali@12345")
        login_button.click()

        # Assuming successful login redirects to the home page, you can adjust this assertion based on your actual behavior
        expected_home_title = "USER PROFILE"  # Adjust based on the actual title of the home page
        self.assertIn(expected_home_title.upper(), self.driver.title.upper())

        # Click on "PRODUCTS" link
        products_link = self.driver.find_element(By.LINK_TEXT, "PRODUCTS")
        products_link.click()

        # Wait for the "Buy Products" button to be clickable
        buy_products_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Buy Products")]'))
        )
        buy_products_button.click()

        # Wait for the "Add to Cart" button to be clickable
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'add-to-cart-button'))
        )
        add_to_cart_button.click()

        # Now the product should be added to the cart

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

