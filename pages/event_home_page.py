import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class EventHomePage(BasePage):
    """ホーム画面 / Home screen."""

    def __init__(self, page: Page):
        super().__init__(page)