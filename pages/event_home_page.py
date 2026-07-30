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

    # -----------------------------------------------------------------------
    # イベント一覧 — ページャー / Pagination
    # -----------------------------------------------------------------------

    def _pagination(self):
        """Pager cua bang イベント一覧 (pager con lai tren trang khong co 表示件数)."""
        return self.page.locator(self.locator.PAGINATION_WRAPPER)

    def get_pagination_summary_text(self) -> str:
        return self._pagination().locator(self.locator.PAGINATION_SUMMARY).inner_text()

    @allure.step("Expect pagination button '{button_name}' is disabled")
    def expect_pagination_button_disabled(self, button_name: str) -> None:
        expect(
            self._pagination().get_by_role("button", name=button_name)
        ).to_be_disabled()

    def get_selected_per_page(self) -> str:
        return self._pagination().locator(self.locator.PER_PAGE_SELECT).input_value()
