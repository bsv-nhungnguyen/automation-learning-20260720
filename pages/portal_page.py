import os
import re

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import PortalLocators as locators
from constants.messages import (
    ICON_GUIDE_LINES,
    MSG_ACCEPT_MISSING_JPG,
    MSG_ACCEPT_MISSING_PNG,
    MSG_PORTAL_URL_MISSING,
    PORTAL_NAME_LABEL,
    REQUIRED_MARK_COLOR,
    REQUIRED_MARK_TEXT,
    TOOLTIP_PORTAL_ICON_TEXT,
    TOOLTIP_PORTAL_NAME_TEXT,
    NAV_OTHER_TABS,
    NAV_TAB_ACTIVE_CLASS,
    NAV_TAB_ACTIVE_COLOR,
    NAV_TAB_PORTAL,
)
from pages.base_page import BasePage


class PortalPage(BasePage):
    """ポータル画面 / Portal home screen (TC01–TC08)."""

    def __init__(self, page: Page):
        super().__init__(page)

    def required_mark(self) -> Locator:
        return self.page.locator(locators.REQUIRED_MARK)

    def portal_name_title(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_TITLE)

    def portal_name_input(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_INPUT)

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
        url = os.getenv("PORTAL_URL")
        if not url:
            raise RuntimeError(MSG_PORTAL_URL_MISSING)
        self.navigate_to(url.rstrip("/"))

    @allure.step("Expect required mark ※必須 visible on portal name")
    def expect_required_mark_visible(self) -> None:
        self.expect_visible(locators.REQUIRED_MARK)
        self.expect_text(locators.REQUIRED_MARK, REQUIRED_MARK_TEXT)
        self.expect_text(locators.PORTAL_NAME_TITLE, PORTAL_NAME_LABEL)

    @allure.step("Expect required mark ※必須 has red color")
    def expect_required_mark_color(self) -> None:
        expect(self.required_mark()).to_have_css("color", REQUIRED_MARK_COLOR)

    @allure.step("Expect save button disabled")
    def expect_save_button_disabled(self) -> None:
        btn = self.save_button()
        expect(btn).to_be_disabled()
        expect(btn).to_have_class(
            re.compile(rf"\b{re.escape(locators.DISABLED_BUTTON_CLASS)}\b")
        )

    @allure.step("Enter portal name: {portal_name}")
    def enter_portal_name(self, portal_name: str) -> None:
        self.portal_name_input().fill(portal_name)

    @allure.step("Expect save button enabled")
    def expect_save_button_enabled(self) -> None:
        expect(self.save_button()).to_be_enabled()

    @allure.step("Expect portal name value: {portal_name}")
    def expect_portal_name_value(self, portal_name: str) -> None:
        actual_value = self.portal_name_input().input_value()
        assert actual_value == portal_name, (
            f"Portal name value mismatch: expected {portal_name!r}, "
            f"got {actual_value!r}"
        )

    @allure.step("Expect portal icon section content displayed")
    def expect_icon_section_content(
        self, guide_lines: tuple[str, ...] | list[str] | None = None
    ) -> None:
        lines = ICON_GUIDE_LINES if guide_lines is None else guide_lines
        self.expect_visible(locators.ICON_PLACEHOLDER)
        expect(self.select_file_button()).to_be_visible()
        expect(self.select_file_button()).to_contain_text(locators.SELECT_FILE_BUTTON_NAME)
        for line in lines:
            self.expect_text(locators.ICON_SECTION, line)

    @allure.step("Expect file input accepts PNG and JPG")
    def expect_file_input_accepts_png_jpg(self) -> None:
        file_input = self.file_input()
        expect(file_input).to_be_attached()
        expect(file_input).to_have_attribute("type", "file")
        accept = file_input.get_attribute("accept") or ""
        assert ".png" in accept, f"{MSG_ACCEPT_MISSING_PNG}: {accept}"
        assert ".jpg" in accept, f"{MSG_ACCEPT_MISSING_JPG}: {accept}"

    @allure.step("Upload portal icon: {file_path}")
    def upload_portal_icon(self, file_path: str) -> None:
        self.file_input().set_input_files(file_path)

    @allure.step("Expect portal icon uploaded: {file_name}")
    def expect_portal_icon_uploaded(self, file_name: str) -> None:
        expect(self.page.locator(locators.ICON_PREVIEW)).to_be_visible()
        expect(self.page.locator(locators.ICON_FILENAME)).to_contain_text(file_name)
        expect(self.page.locator(locators.REMOVE_FILE_BUTTON)).to_be_visible()

    @allure.step("Expect portal name tooltip content on hover")
    def expect_portal_name_tooltip_on_hover(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_NAME_ARIA).hover()
        tooltip = self.page.locator(locators.TOOLTIP_MESSAGE)
        expect(tooltip).to_be_visible()
        expect(tooltip).to_contain_text(TOOLTIP_PORTAL_NAME_TEXT)

    @allure.step("Expect portal icon tooltip content on hover")
    def expect_portal_icon_tooltip_on_hover(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_ICON_ARIA).hover()
        tooltip = self.page.locator(locators.TOOLTIP_MESSAGE)
        expect(tooltip).to_be_visible()
        expect(tooltip).to_contain_text(TOOLTIP_PORTAL_ICON_TEXT)

    @allure.step("Expect nav tab ポータル is active (orange underline)")
    def expect_portal_tab_active(self) -> None:
        active = self.page.locator(locators.NAV_ACTIVE_TAB)
        expect(active).to_be_visible()
        expect(active).to_have_text(NAV_TAB_PORTAL)
        expect(active).to_have_class(NAV_TAB_ACTIVE_CLASS)
        expect(active).to_have_css("color", NAV_TAB_ACTIVE_COLOR)
        expect(active).to_have_css("border-bottom-color", NAV_TAB_ACTIVE_COLOR)

        tabs = self.page.locator(locators.NAV_TABS)
        expect(tabs.filter(has_text=NAV_TAB_PORTAL)).to_have_class(NAV_TAB_ACTIVE_CLASS)
        for tab_name in NAV_OTHER_TABS:
            other = tabs.filter(has_text=tab_name)
            expect(other).to_be_visible()
            expect(other).not_to_have_class(NAV_TAB_ACTIVE_CLASS)