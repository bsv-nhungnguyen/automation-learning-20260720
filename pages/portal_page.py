from __future__ import annotations

import re

import allure
from playwright.sync_api import expect

from constants.locators import PortalLocators as locators
from constants.messages import (
    ICON_GUIDE_LINES,
    PORTAL_NAME_LABEL,
    REQUIRED_MARK_COLOR,
    REQUIRED_MARK_TEXT,
    TOOLTIP_PORTAL_ICON_TEXT,
    TOOLTIP_PORTAL_NAME_TEXT,
    NAV_TAB_ACTIVE_CLASS,
    NAV_TAB_ACTIVE_COLOR_ORANGE,
    NAV_TAB_PORTAL,
)
from pages.base_page import BasePage

NAV_OTHER_TABS = ("イベント", "会員管理", "配信する", "レポート")


class PortalPage(BasePage):
    """ポータル画面 / Portal home screen (TC01–TC08)."""

    @allure.step("Open portal home screen")
    def open_portal_screen(self, app_url: str) -> None:
        self.page.goto(f"{app_url.rstrip('/')}/portal_home.html")
        self.page.wait_for_load_state("networkidle")

    @allure.step("Expect required mark ※必須 visible on portal name")
    def expect_required_mark_visible(self) -> None:
        self.expect_visible(locators.REQUIRED_MARK)
        self.expect_text(locators.REQUIRED_MARK, REQUIRED_MARK_TEXT)
        self.expect_text(locators.PORTAL_NAME_TITLE, PORTAL_NAME_LABEL)

    @allure.step("Expect required mark ※必須 has red color")
    def expect_required_mark_color(self) -> None:
        expect(self.page.locator(locators.REQUIRED_MARK)).to_have_css(
            "color", REQUIRED_MARK_COLOR
        )

    @allure.step("Expect save button disabled")
    def expect_save_button_disabled(self) -> None:
        btn = self.page.locator(locators.SAVE_BUTTON)
        expect(btn).to_be_disabled()
        expect(btn).to_have_class(
            re.compile(rf"\b{re.escape(locators.DISABLED_BUTTON_CLASS)}\b")
        )

    @allure.step("Enter portal name: {portal_name}")
    def enter_portal_name(self, portal_name: str) -> None:
        self.fill(locators.PORTAL_NAME_INPUT, portal_name)

    @allure.step("Expect save button enabled")
    def expect_save_button_enabled(self) -> None:
        expect(self.page.locator(locators.SAVE_BUTTON)).to_be_enabled()

    @allure.step("Expect portal name value: {portal_name}")
    def expect_portal_name_value(self, portal_name: str) -> None:
        expect(self.page.locator(locators.PORTAL_NAME_INPUT)).to_have_value(
            portal_name
        )

    @allure.step("Expect portal icon section content displayed")
    def expect_icon_section_content(
        self, guide_lines: tuple[str, ...] | list[str] | None = None
    ) -> None:
        lines = ICON_GUIDE_LINES if guide_lines is None else guide_lines
        self.expect_visible(locators.ICON_PLACEHOLDER)
        btn = self.page.locator(locators.SELECT_FILE_BUTTON)
        expect(btn).to_be_visible()
        expect(btn).to_contain_text(locators.SELECT_FILE_BUTTON_NAME)
        for line in lines:
            self.expect_text(locators.ICON_SECTION, line)

    @allure.step("Expect file input accepts PNG and JPG")
    def expect_file_input_accepts_png_jpg(self) -> None:
        file_input = self.page.locator(locators.FILE_INPUT)
        expect(file_input).to_be_attached()
        expect(file_input).to_have_attribute("type", "file")
        accept = file_input.get_attribute("accept") or ""
        assert ".png" in accept, f"File input accept is missing .png: {accept!r}"
        assert ".jpg" in accept, f"File input accept is missing .jpg: {accept!r}"

    @allure.step("Upload portal icon: {file_path}")
    def upload_portal_icon(self, file_path: str) -> None:
        self.page.locator(locators.FILE_INPUT).set_input_files(file_path)

    @allure.step("Expect portal icon uploaded: {file_name}")
    def expect_portal_icon_uploaded(self, file_name: str) -> None:
        expect(self.page.locator(locators.ICON_PREVIEW)).to_be_visible()
        expect(self.page.locator(locators.ICON_FILENAME)).to_contain_text(file_name)
        expect(self.page.locator(locators.REMOVE_FILE_BUTTON)).to_be_visible()

    @allure.step("Hover portal name (?) tooltip button")
    def hover_portal_name_tooltip_button(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_NAME_ARIA).hover()

    @allure.step("Hover portal icon (?) tooltip button")
    def hover_portal_icon_tooltip_button(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_ICON_ARIA).hover()

    @allure.step("Expect portal name tooltip shows guide content")
    def expect_portal_name_tooltip_content(self) -> None:
        tooltip = self.page.locator(locators.TOOLTIP_MESSAGE)
        expect(tooltip).to_be_visible()
        expect(tooltip).to_contain_text(TOOLTIP_PORTAL_NAME_TEXT)

    @allure.step("Expect portal icon tooltip shows guide content")
    def expect_portal_icon_tooltip_content(self) -> None:
        tooltip = self.page.locator(locators.TOOLTIP_MESSAGE)
        expect(tooltip).to_be_visible()
        expect(tooltip).to_contain_text(TOOLTIP_PORTAL_ICON_TEXT)

    @allure.step("Expect nav tab ポータル is active (orange underline)")
    def expect_portal_tab_active(self) -> None:
        active = self.page.locator(locators.NAV_ACTIVE_TAB)
        expect(active).to_be_visible()
        expect(active).to_have_text(NAV_TAB_PORTAL)
        expect(active).to_have_class(NAV_TAB_ACTIVE_CLASS)
        expect(active).to_have_css("color", NAV_TAB_ACTIVE_COLOR_ORANGE)
        expect(active).to_have_css(
            "border-bottom-color", NAV_TAB_ACTIVE_COLOR_ORANGE
        )

        tabs = self.page.locator(locators.NAV_TABS)
        expect(tabs.filter(has_text=NAV_TAB_PORTAL)).to_have_class(NAV_TAB_ACTIVE_CLASS)
        for tab_name in NAV_OTHER_TABS:
            other = tabs.filter(has_text=tab_name)
            expect(other).to_be_visible()
            expect(other).not_to_have_class(NAV_TAB_ACTIVE_CLASS)
