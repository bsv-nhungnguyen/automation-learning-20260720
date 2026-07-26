import allure
from playwright.sync_api import Page

from constants.locators import EventHomeLocators
from pages.base_page import BasePage


class EventHomePage(BasePage):
    """ホーム画面 / Home screen."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.locator = EventHomeLocators

    def get_navigation_tab_names(self):
        return self.page.locator(self.locator.NAVIGATION_TABS).all_inner_texts()

    def is_navigation_tab_order_correct(self):
        return self.page.locator(self.locator.NAVIGATION_TABS).all_text_contents() == [
            self.locator.EVENT_TAB,
            self.locator.PORTAL_TAB,
            self.locator.MEMBER_TAB,
            self.locator.MAIL_TAB,
            self.locator.REPORT_TAB,
        ]

    def is_tab_active(self, tab_name):
        tab = self.page.get_by_role('link', name=tab_name).locator('div')
        return tab.get_attribute('class') == 'active'

    def is_section_title_displayed(self, title):
        return self.page.get_by_role("heading", name=title).is_visible()

    def is_usage_label_visible(self, label: str) -> bool:
        return self.page.locator(
                self.locator.USAGE_LABEL,
            has_text=label,
        ).is_visible()

    def hover_tooltip_by_label(self, label: str):
        return self.page.locator(
            self.locator.USAGE_LABEL,
            has_text=label,
            ).locator(
                self.locator.TOOLTIP_ICON,
                ).hover()

    def is_tooltip_content_visible(self, tooltip: str):
        return self.page.locator(
            self.locator.TOOLTIP_CONTENT
            ).filter(
                has_text=tooltip
                ).is_visible()