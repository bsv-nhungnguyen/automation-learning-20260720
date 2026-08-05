import re
import allure
from playwright.sync_api import Page ,expect

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

        with allure.step(
            f"Get event table header names ({len(cleaned)}): {cleaned}"
        ):
            pass

        return cleaned


    def click_create_event(self) -> None:
        self.page.locator(self.locator.CREATE_EVENT_BUTTON).click()

    def close_create_event_form(self) -> None:
        self.page.locator(self.locator.CREATE_EVENT_CLOSE).click()

    def expect_create_event_form_visible(self) -> None:
        expect(self.page.get_by_text(self.locator.CREATE_EVENT_FORM_LABEL)).to_be_visible()

    def click_grid_view(self) -> None:
        self.page.locator(self.locator.GRID_VIEW_BUTTON).click()

    def click_list_view(self) -> None:
        self.page.locator(self.locator.LIST_VIEW_BUTTON).click()

    def expect_grid_view_displayed(self) -> None:
        expect(self.page.locator(self.locator.EVENT_GRID_VIEW)).to_be_visible()
        expect(self.page.locator(self.locator.EVENT_LIST_VIEW)).to_be_hidden()
        expect(self.page.locator(self.locator.GRID_VIEW_BUTTON)).to_have_class(
            re.compile(self.locator.ACTIVE_BUTTON_CLASS)
        )

    def expect_list_view_displayed(self) -> None:
        expect(self.page.locator(self.locator.EVENT_LIST_VIEW)).to_be_visible()
        expect(self.page.locator(self.locator.EVENT_GRID_VIEW)).to_be_hidden()
        expect(self.page.locator(self.locator.LIST_VIEW_BUTTON)).to_have_class(
            re.compile(self.locator.ACTIVE_BUTTON_CLASS)
        )