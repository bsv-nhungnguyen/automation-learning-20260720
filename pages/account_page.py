import re
import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AccountPage(BasePage):

    # -----------------------------------------------------------------------
    # Locators
    # -----------------------------------------------------------------------
    EMAIL_PLACEHOLDER = "メールアドレス"        # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"          # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"              # type="button" — NOT type="submit"
    PASSWORD_INPUT = 'input[type="password"]'

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Enter email: {email}")
    def input_email(self, email: str):
        self.page.get_by_placeholder(self.EMAIL_PLACEHOLDER).fill(email)

    @allure.step("Enter password")
    def input_password(self, password: str):
        self.page.get_by_placeholder(self.PASSWORD_PLACEHOLDER).fill(password)

    @allure.step("Click login button")
    def click_login(self):
        self.page.locator(self.LOGIN_BUTTON).click()

    @allure.step("Double-click login button")
    def double_click_login(self):
        self.page.locator(self.LOGIN_BUTTON).dblclick()

    @allure.step("Login with email '{email}'")
    def login(self, email: str, password: str):
        self.input_email(email)
        self.input_password(password)
        with self.page.expect_navigation(wait_until="load"):
            self.click_login()
        self.page.wait_for_load_state("networkidle")