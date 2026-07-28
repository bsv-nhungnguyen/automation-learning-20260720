import re
import allure
from playwright.sync_api import Page ,expect

from constants.locators import EventHomeLocators
from pages.base_page import BasePage

@allure.feature("Event Home Page")
class EventHomePage(BasePage):
    """ホーム画面 / Home screen."""
    @allure.step("Initialize EventHomePage")
    def __init__(self, page: Page):
        super().__init__(page)
        self.locator = EventHomeLocators
    @allure.step("Get navigation tab names")
    def get_navigation_tab_names(self):
        return self.page.locator(self.locator.NAVIGATION_TABS).all_inner_texts()
    @allure.step("Check if navigation tab order is correct")
    def is_navigation_tab_order_correct(self):
        return self.page.locator(self.locator.NAVIGATION_TABS).all_text_contents() == [
            self.locator.EVENT_TAB,
            self.locator.PORTAL_TAB,
            self.locator.MEMBER_TAB,
            self.locator.MAIL_TAB,
            self.locator.REPORT_TAB,
        ]
    @allure.step("Check if tab is active")
    def is_tab_active(self, tab_name):
        tab = self.page.get_by_role('link', name=tab_name).locator('div')
        return tab.get_attribute('class') == 'active'
    @allure.step("Check if section title is displayed")
    def is_section_title_displayed(self, title):
        return self.page.get_by_role("heading", name=title).is_visible()
    @allure.step("Check if usage label is visible")
    def is_usage_label_visible(self, label: str) -> bool:
        return self.page.locator(
                self.locator.USAGE_LABEL,
            has_text=label,
        ).is_visible()
    @allure.step("Hover tooltip by label")
    def hover_tooltip_by_label(self, label: str):
        return self.page.locator(
            self.locator.USAGE_LABEL,
            has_text=label,
            ).locator(
                self.locator.TOOLTIP_ICON,
                ).hover()
    @allure.step("Check if tooltip content is visible")
    def is_tooltip_content_visible(self, tooltip: str):
        return self.page.locator(
            self.locator.TOOLTIP_CONTENT
            ).filter(
                has_text=tooltip
                ).is_visible()
    @allure.step("Get event table header names")
    def get_event_table_header_names(self) -> list[str]:
        headers = self.page.locator(
            f"{self.locator.EVENT_LIST_VIEW} {self.locator.EVENT_TABLE_HEADERS}"
        ).all_inner_texts()

        cleaned = []
        for text in headers:
            name = (
                text.replace("arrow_upward", "")
                .replace("help_outline", "")
                .split("\n")[0]
                .strip()
            )
            cleaned.append(name)
        return cleaned

    @allure.step("Click create event button")
    def click_create_event(self) -> None:
        self.page.locator(self.locator.CREATE_EVENT_BUTTON).click()
    @allure.step("Close create event form")
    def close_create_event_form(self) -> None:
        self.page.locator(self.locator.CREATE_EVENT_CLOSE).click()
    @allure.step("Expect create event form visible")
    def expect_create_event_form_visible(self) -> None:
        expect(self.page.get_by_text(self.locator.CREATE_EVENT_FORM_LABEL)).to_be_visible()
    @allure.step("Click grid view button")
    def click_grid_view(self) -> None:
        self.page.locator(self.locator.GRID_VIEW_BUTTON).click()
    @allure.step("Click list view button")
    def click_list_view(self) -> None:
        self.page.locator(self.locator.LIST_VIEW_BUTTON).click()
    @allure.step("Expect grid view displayed")
    def expect_grid_view_displayed(self) -> None:
        expect(self.page.locator(self.locator.EVENT_GRID_VIEW)).to_be_visible()
        expect(self.page.locator(self.locator.EVENT_LIST_VIEW)).to_be_hidden()
        expect(self.page.locator(self.locator.GRID_VIEW_BUTTON)).to_have_class(
            re.compile(self.locator.ACTIVE_BUTTON_CLASS)
        )
    @allure.step("Expect list view displayed")
    def expect_list_view_displayed(self) -> None:
        expect(self.page.locator(self.locator.EVENT_LIST_VIEW)).to_be_visible()
        expect(self.page.locator(self.locator.EVENT_GRID_VIEW)).to_be_hidden()
        expect(self.page.locator(self.locator.LIST_VIEW_BUTTON)).to_have_class(
            re.compile(self.locator.ACTIVE_BUTTON_CLASS)
        )