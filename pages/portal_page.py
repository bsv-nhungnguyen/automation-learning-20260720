import re

import allure
from playwright.sync_api import Locator, Page, expect

from PortalPageLocators import PortalLocators as locators
from pages.base_page import BasePage

PORTAL_URL = "https://bsv-nhungnguyen.github.io/sample_UI/portal_home.html"

ICON_GUIDE_LINES = (
    "推奨サイズ： 1024×1024(px)",
    "最小サイズ： 100px × 100px",
    "対応: PNG・JPG",
)

TOOLTIP_NAME_TEXT = "ポータルの管理用タイトルを入力します。"
TOOLTIP_ICON_TEXT = "ポータルの管理用アイコンを指定します"

 # create a class for portal page
class PortalPage(BasePage):
    """ポータル画面 / Portal home screen.

    Page Object: actions + reusable helpers. Test scenarios live in tests/.
    """

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Locators (expose for tests / helpers — avoid raw selectors in tests)
    # -----------------------------------------------------------------------

    def required_mark(self) -> Locator:
        return self.page.locator(locators.REQUIRED_MARK)

    def portal_name_title(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_TITLE)

    def portal_name_input(self) -> Locator:
        return self.page.locator(locators.PORTAL_NAME_INPUT)

    def save_button(self) -> Locator:
        return self.page.locator(locators.SAVE_BUTTON)

    def icon_section(self) -> Locator:
        return self.page.locator(locators.ICON_SECTION)

    def icon_placeholder(self) -> Locator:
        return self.page.locator(locators.ICON_PLACEHOLDER)

    def select_file_button(self) -> Locator:
        return self.page.locator(locators.SELECT_FILE_BUTTON)

    def file_input(self) -> Locator:
        return self.page.locator(locators.FILE_INPUT)

    def tooltip_active(self) -> Locator:
        return self.page.locator(locators.TOOLTIP_ACTIVE)

    def tooltip_message(self) -> Locator:
        return self.page.locator(locators.TOOLTIP_MESSAGE)

    def nav_active_tab(self) -> Locator:
        return self.page.locator(locators.NAV_ACTIVE_TAB)

    # -----------------------------------------------------------------------
    # Navigation
    # -----------------------------------------------------------------------

    @allure.step("Open portal home page")
    def open(self) -> None:
        self.navigate_to(PORTAL_URL)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Fill portal name: {name}")
    def fill_portal_name(self, name: str) -> None:
        self.fill(locators.PORTAL_NAME_INPUT, name)

    @allure.step("Get portal name input value")
    def get_portal_name_value(self) -> str:
        return self.portal_name_input().input_value()

    @allure.step("Click portal name tooltip (?)")
    def click_portal_name_tooltip(self) -> None:
        self.click_by_role("button", locators.TOOLTIP_NAME_ARIA)

    @allure.step("Click portal icon tooltip (?)")
    def click_portal_icon_tooltip(self) -> None:
        self.click_by_role("button", locators.TOOLTIP_ICON_ARIA)

    @allure.step("Hover portal name tooltip (?)")
    def hover_portal_name_tooltip(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_NAME_ARIA).hover()

    @allure.step("Hover portal icon tooltip (?)")
    def hover_portal_icon_tooltip(self) -> None:
        self.page.get_by_role("button", name=locators.TOOLTIP_ICON_ARIA).hover()

    @allure.step("Upload portal icon: {file_path}")
    def upload_portal_icon(self, file_path: str) -> None:
        self.file_input().set_input_files(file_path)

    # -----------------------------------------------------------------------
    # Reusable UI helpers (not test cases — tests call these)
    # -----------------------------------------------------------------------

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

    @allure.step("Expect save button enabled")
    def expect_save_button_enabled(self) -> None:
        btn = self.save_button()
        expect(btn).to_be_enabled()
        expect(btn).not_to_have_class(
            re.compile(rf"\b{re.escape(locators.DISABLED_BUTTON_CLASS)}\b")
        )

    @allure.step("Expect portal name value is '{expected}'")
    def expect_portal_name_value(self, expected: str) -> None:
        expect(self.portal_name_input()).to_have_value(expected)

    @allure.step("Expect portal icon section content")
    def expect_icon_section_content(self) -> None:
        self.expect_visible(locators.ICON_PLACEHOLDER)
        self.expect_visible(locators.SELECT_FILE_BUTTON)
        for line in ICON_GUIDE_LINES:
            self.expect_text(locators.ICON_SECTION, line)

    @allure.step("Expect file input accessible")
    def expect_file_input_accessible(self) -> None:
        file_input = self.file_input()
        expect(file_input).to_have_attribute("type", "file")
        accept = file_input.get_attribute("accept") or ""
        assert ".png" in accept, f"accept missing .png: {accept}"
        assert ".jpg" in accept, f"accept missing .jpg: {accept}"

    @allure.step("Expect tooltip contains '{text}'")
    def expect_tooltip_contains(self, text: str) -> None:
        self.expect_visible(locators.TOOLTIP_ACTIVE)
        self.expect_text(locators.TOOLTIP_MESSAGE, text)

    @allure.step("Expect portal tab active")
    def expect_portal_tab_active(self) -> None:
        self.expect_visible(locators.NAV_ACTIVE_TAB)
        self.expect_text(locators.NAV_ACTIVE_TAB, "ポータル")
