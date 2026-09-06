import re

import allure
from playwright.sync_api import Page, expect

from constants.locators import EventHomeLocators
from pages.base_page import BasePage


class EventHomePage(BasePage):
    """ホーム画面 / Home screen."""

    PAGINATION_SUMMARY_FORMAT = "{total}件中 {start} - {end}件目"  # 件数サマリーの文言フォーマット

    def __init__(self, page: Page):
        super().__init__(page)
        self.locator = EventHomeLocators

    # -----------------------------------------------------------------------
    # ナビゲーションタブ / Navigation tabs
    # -----------------------------------------------------------------------

    @allure.step("Get navigation tab names")
    def get_navigation_tab_names(self) -> list[str]:
        return self.page.locator(self.locator.NAVIGATION_TABS).all_inner_texts()

    @allure.step("Check if navigation tab order is correct")
    def is_navigation_tab_order_correct(self) -> bool:
        return self.page.locator(self.locator.NAVIGATION_TABS).all_inner_texts() == [
            self.locator.EVENT_TAB,
            self.locator.PORTAL_TAB,
            self.locator.MEMBER_TAB,
            self.locator.MAIL_TAB,
            self.locator.REPORT_TAB,
        ]

    @allure.step("Check if tab is active")
    def is_tab_active(self, tab_name: str) -> bool:
        tab = self.page.get_by_role("link", name=tab_name).locator("div")
        class_name = tab.get_attribute("class") or ""
        return "active" in class_name

    # -----------------------------------------------------------------------
    # ウィジェット / Widgets
    # -----------------------------------------------------------------------

    @allure.step("Check if usage label is visible")
    def is_usage_label_visible(self, label: str) -> bool:
        return self.page.locator(
            self.locator.WIDGET_LABEL,
            has_text=label,
        ).is_visible()

    @allure.step("Hover tooltip by label")
    def hover_tooltip_by_label(self, label: str) -> None:
        self.page.locator(
            self.locator.WIDGET_LABEL,
            has_text=label,
        ).locator(self.locator.TOOLTIP_ICON).hover()

    @allure.step("Check if tooltip content is visible")
    def is_tooltip_content_visible(self, tooltip: str) -> bool:
        return (
            self.page.locator(self.locator.TOOLTIP_CONTENT)
            .filter(has_text=tooltip)
            .is_visible()
        )

    # -----------------------------------------------------------------------
    # イベント一覧 / Event list
    # -----------------------------------------------------------------------

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

        with allure.step(
            f"Get event table header names ({len(cleaned)}): {cleaned}"
        ):
            pass

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

    @allure.step("Get announcement list")
    def get_announcement_list(self):
        return self.page.locator(self.locator.ANNOUNCEMENT_LIST)

    @allure.step("Get announcement rows")
    def get_announcement_rows(self):
        return self.page.locator(self.locator.ANNOUNCEMENT_ITEM)

    @allure.step("Get announcement row count")
    def get_announcement_row_count(self) -> int:
        return self.get_announcement_rows().count()

    @allure.step("Expect announcement list visible")
    def expect_announcement_list_visible(self) -> None:
        expect(self.get_announcement_list()).to_be_visible()

    @allure.step("Get announcement date")
    def get_announcement_date(self, index: int) -> str:
        return self.get_announcement_rows().nth(index).locator(
            self.locator.ANNOUNCEMENT_DATE
        ).inner_text().strip()

    @allure.step("Get announcement tag")
    def get_announcement_tag(self, index: int) -> str:
        return self.get_announcement_rows().nth(index).locator(
            self.locator.ANNOUNCEMENT_TAG
        ).inner_text().strip()

    @allure.step("Get announcement title")
    def get_announcement_title(self, index: int) -> str:
        return self.get_announcement_rows().nth(index).locator(
            self.locator.ANNOUNCEMENT_TITLE
        ).inner_text().strip()

    @allure.step("Check if announcement row has NEW badge")
    def has_new_badge(self, index: int) -> bool:
        row = self.get_announcement_rows().nth(index)
        badge = row.locator(self.locator.ANNOUNCEMENT_NEW_BADGE)
        return badge.count() > 0 and badge.is_visible()

    # -----------------------------------------------------------------------
    # イベント一覧 — キーワード検索 / Keyword search
    # -----------------------------------------------------------------------

    @allure.step("Search event by keyword: {keyword}")
    def search_event_by_keyword(self, keyword: str) -> None:
        """Nhap keyword vao o 'キーワードを入力' va nhan Enter de loc danh sach."""
        search_input = self.page.get_by_placeholder(self.locator.SEARCH_PLACEHOLDER)
        search_input.fill(keyword)
        search_input.press("Enter")

    @allure.step("Get event name of the first row")
    def get_first_event_name(self) -> str:
        """Ten event o dong dau tien — dung lam keyword search.

        Ten hien thi co the bi cat ngan ("Automation test...") nen phai bo
        phan duoi cham thi keyword moi khop voi du lieu that.
        """
        name = (self.page.locator(self.locator.EVENT_NAME_CELL).first.inner_text() or "").strip()
        for suffix in self.locator.TRUNCATION_SUFFIXES:
            if name.endswith(suffix):
                return name[: -len(suffix)].strip()
        return name

    def get_visible_event_row_texts(self) -> list[str]:
        """Text cua cac dong dang hien thi — dung de assert ket qua loc."""
        return self.page.locator(self.locator.EVENT_TABLE_ROW_VISIBLE).all_inner_texts()

    @allure.step("Expect the event table still shows at least one row")
    def expect_has_visible_event_rows(self) -> None:
        """Cho den khi bang loc xong va van con it nhat 1 dong ket qua."""
        expect(self.page.locator(self.locator.EVENT_TABLE_ROW_VISIBLE).first).to_be_visible()

    @allure.step("Collect event rows that do not match keyword: {keyword}")
    def get_event_rows_not_matching_keyword(self, keyword: str) -> list[str]:
        keyword_lower = keyword.lower()
        return [
            row
            for row in self.get_visible_event_row_texts()
            if keyword_lower not in row.lower()
        ]

    @allure.step("Get the number of event rows currently displayed")
    def get_visible_event_row_count(self) -> int:
        return self.page.locator(self.locator.EVENT_TABLE_ROW_VISIBLE).count()

    # -----------------------------------------------------------------------
    # イベント一覧 — ページャー / Pagination
    # -----------------------------------------------------------------------

    @allure.step("Get pagination wrapper")
    def _pagination(self):
        return self.page.locator(self.locator.PAGINATION_WRAPPER)

    @allure.step("Get pagination summary text")
    def get_pagination_summary_text(self) -> str:
        return self._pagination().locator(self.locator.PAGINATION_SUMMARY).inner_text()

    @allure.step("Get total count from pagination summary")
    def get_pagination_total_count(self) -> int:
        summary = self.get_pagination_summary_text()
        matched = re.search(self.locator.PAGINATION_TOTAL_PATTERN, summary)
        assert matched, f"Cannot read total count from pagination summary: {summary!r}"
        return int(matched.group(1))

    @allure.step("Build the expected pagination summary of the first page")
    def build_expected_pagination_summary(self, next_button_name: str) -> str:
        row_count = self.get_visible_event_row_count()
        total = (
            row_count
            if self.is_pagination_button_disabled(next_button_name)
            else self.get_pagination_total_count()
        )
        return self.PAGINATION_SUMMARY_FORMAT.format(total=total, start=1, end=row_count)

    @allure.step("Expect pagination button '{button_name}' is disabled")
    def expect_pagination_button_disabled(self, button_name: str) -> None:
        expect(
            self._pagination().get_by_role("button", name=button_name)
        ).to_be_disabled()

    @allure.step("Check if pagination button '{button_name}' is disabled")
    def is_pagination_button_disabled(self, button_name: str) -> bool:
        return self._pagination().get_by_role("button", name=button_name).is_disabled()

    @allure.step("Get selected per page value")
    def get_selected_per_page(self) -> str:
        return self._pagination().locator(self.locator.PER_PAGE_SELECT).input_value()
