import re

import allure
from playwright.sync_api import Locator, Page, expect

from pages.PortalPageLocators import PortalLocators as locators
from pages.base_page import BasePage

PORTAL_URL = "https://bsv-nhungnguyen.github.io/sample_UI/portal_home.html"


class PortalPage(BasePage):
    """ポータル画面 / Portal home screen (TC01–TC02)."""

    def __init__(self, page: Page):
        super().__init__(page)

    def required_mark(self) -> Locator:
        return self.page.locator(locators.REQUIRED_MARK)

    def portal_name_title(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_TITLE)

    def save_button(self) -> Locator:
        return self.page.locator(locators.SAVE_BUTTON)

    @allure.step("Open portal home page")
    def open(self) -> None:
        self.navigate_to(PORTAL_URL)

    @allure.step("Expect required mark ※必須 visible on portal name")
    def expect_required_mark_visible(self) -> None:
        self.expect_visible(locators.REQUIRED_MARK)
        self.expect_text(locators.REQUIRED_MARK, "※必須")
        self.expect_text(locators.PORTAL_NAME_TITLE, "ポータル名")

    @allure.step("Expect save button disabled")
    def expect_save_button_disabled(self) -> None:
        btn = self.save_button()
        expect(btn).to_be_disabled()
        expect(btn).to_have_class(
            re.compile(rf"\b{re.escape(locators.DISABLED_BUTTON_CLASS)}\b")
        )
