from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from utils import load_config, human_delay, logging

class AccountManager:
    def __init__(self, credentials):
        self.config = load_config()
        self.credentials = credentials
        self.client = Client()
        self.client.delay_range = [1, 5]
        if self.config.get("proxy"):
            self.client.set_proxy(self.config["proxy"])

    def login(self):
        try:
            username = self.credentials["username"]
            password = self.credentials["password"]
            self.client.login(username, password)
            logging.info(f"Logged in as {username}")
        except LoginRequired:
            logging.error("Login failed")
            raise

    def create_account(self):
        chrome_options = Options()
        if self.config.get("headless", True):
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            temp_email = self._get_temp_email()
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            human_delay(2, 4)
            driver.find_element_by_name("emailOrPhone").send_keys(temp_email)
            driver.find_element_by_name("fullName").send_keys("Test User")
            driver.find_element_by_name("username").send_keys(f"testuser{random.randint(1000, 9999)}")
            driver.find_element_by_name("password").send_keys("SecurePass123!")
            driver.find_element_by_css_selector("button[type='submit']").click()
            human_delay(3, 5)
            logging.info(f"Created account with email {temp_email}")
        finally:
            driver.quit()

    def _get_temp_email(self):
        response = requests.get("https://api.temp-mail.org/request/mail/id/1/")
        email = response.json().get("mail")
        logging.info(f"Generated temp email: {email}")
        return email
