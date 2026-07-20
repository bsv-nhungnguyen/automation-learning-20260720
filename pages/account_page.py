import allure
from playwright.sync_api import Page

from constants.locators import LoginLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    """ログイン画面 / Login screen."""

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Enter email: {email}")
    def input_email(self, email: str):
        self.page.get_by_placeholder(LoginLocators.EMAIL_PLACEHOLDER).fill(email)

    @allure.step("Enter password")
    def input_password(self, password: str):
        self.page.get_by_placeholder(LoginLocators.PASSWORD_PLACEHOLDER).fill(password)

    @allure.step("Click login button")
    def click_login(self):
        self.page.locator(LoginLocators.LOGIN_BUTTON).click()

    @allure.step("Login with email '{email}'")
    def login(self, email: str, password: str):
        self.input_email(email)
        self.input_password(password)
        with self.page.expect_navigation(wait_until="load"):
            self.click_login()
        self.page.wait_for_load_state("networkidle")
