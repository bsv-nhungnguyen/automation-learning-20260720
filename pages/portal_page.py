import re

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import PortalLocators as locators
from pages.base_page import BasePage

PORTAL_URL = "https://bsv-nhungnguyen.github.io/sample_UI/portal_home.html"


class PortalPage(BasePage):
    """ポータル画面 / Portal home screen (TC01–TC02, TC05–TC06)."""

    def __init__(self, page: Page):
        super().__init__(page)

    def required_mark(self) -> Locator:
        return self.page.locator(locators.REQUIRED_MARK)

    def portal_name_title(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_TITLE)

    def save_button(self) -> Locator:
        return self.page.locator(locators.SAVE_BUTTON)

    def icon_placeholder(self) -> Locator:
        return self.page.locator(locators.ICON_PLACEHOLDER)

    def select_file_button(self) -> Locator:
        return self.page.locator(locators.SELECT_FILE_BUTTON)

    def file_input(self) -> Locator:
        return self.page.locator(locators.FILE_INPUT)

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

    @allure.step("Expect portal icon section content displayed")
    def expect_icon_section_content(self, guide_lines: tuple[str, ...] | list[str]) -> None:
        self.expect_visible(locators.ICON_PLACEHOLDER)
        self.expect_visible(locators.SELECT_FILE_BUTTON)
        expect(self.select_file_button()).to_contain_text(locators.SELECT_FILE_BUTTON_NAME)
        for line in guide_lines:
            self.expect_text(locators.ICON_SECTION, line)

    @allure.step("Expect file input accepts PNG and JPG")
    def expect_file_input_accepts_png_jpg(self) -> None:
        file_input = self.file_input()
        expect(file_input).to_be_attached()
        expect(file_input).to_have_attribute("type", "file")
        accept = file_input.get_attribute("accept") or ""
        assert ".png" in accept, f"accept missing .png: {accept}"
        assert ".jpg" in accept, f"accept missing .jpg: {accept}"

    @allure.step("Upload portal icon: {file_path}")
    def upload_portal_icon(self, file_path: str) -> None:
        self.page.locator(locators.FILE_INPUT).set_input_files(file_path)

    @allure.step("Expect portal icon uploaded: {file_name}")
    def expect_portal_icon_uploaded(self, file_name: str) -> None:
        expect(self.page.locator(locators.ICON_PREVIEW)).to_be_visible()
        expect(self.page.locator(locators.ICON_FILENAME)).to_contain_text(file_name)
        expect(self.page.locator(locators.REMOVE_FILE_BUTTON)).to_be_visible()