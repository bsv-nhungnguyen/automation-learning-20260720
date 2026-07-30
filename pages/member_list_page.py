import re

import allure
from playwright.sync_api import Page, expect

from constants.locators import MemberListPageLocators as locators
from constants.messages import (
    MEMBER_STATUS_VALID_VALUES,
    MSG_MEMBER_NO_ROWS,
    MSG_MEMBER_STATUS_COLUMN_MISSING,
    MSG_MEMBER_STATUS_INVALID,
    MSG_MEMBER_TAB_NOT_ACTIVE,
    MSG_MEMBER_TAB_PANEL_NOT_VISIBLE,
    MSG_MEMBER_TAB_URL_MISMATCH,
)
from pages.base_page import BasePage
# tab_name → (URL hash, panel data-panel / panel_* suffix)
MEMBER_SUB_TABS: dict[str, tuple[str, str]] = {
    "会員属性の設定": ("#attribute", "attribute"),
    "会員登録フォーム": ("#form", "form"),
    "アプリ利用者": ("#app", "app"),
    "会員退会設定": ("#withdraw", "withdraw"),
}


class MemberListPage(BasePage):
    """会員一覧ページ / Member list page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Open 会員リスト screen")
    def open_member_list_screen(self, app_url: str) -> None:
        self.page.goto(f"{app_url.rstrip('/')}/member_list.html")
        self.page.wait_for_load_state("networkidle")

    @allure.step("Open member search panel")
    def open_search_panel(self) -> None:
        self.click(locators.SEARCH_BUTTON)

    @allure.step("Sort member list by member ID")
    def sort_by_member_id(self) -> None:
        self.click(locators.MEMBER_ID_HEADER)

    @allure.step("Select the first member row")
    def select_first_member(self) -> None:
        # UI intentionally repeats rows; test targets the first visible data row.
        first_row = self.page.locator(locators.TABLE_ROWS).first
        first_row.locator(locators.ROW_CHECKBOX).check()

    @allure.step("Navigate to new member registration")
    def navigate_to_new_member_registration(self) -> None:
        self.click(locators.NEW_MEMBER_REGISTRATION_BUTTON)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Navigate to member sub-tab: {tab_name}")
    def navigate_to_tab(self, tab_name: str) -> None:
        self.page.get_by_role("link", name=tab_name, exact=True).click()

    # -----------------------------------------------------------------------
    # Boolean / data helpers
    # -----------------------------------------------------------------------

    @allure.step("Check whether 会員リスト tab is active")
    def is_member_list_tab_active(self) -> bool:
        tab_class = self.page.locator(locators.MEMBER_LIST_TAB_LINK).get_attribute("class") or ""
        return locators.MEMBER_LIST_TAB_ACTIVE_CLASS in tab_class.split()

    @allure.step("Get member count from heading")
    def get_member_count(self) -> int:
        return int(self.page.locator(locators.MEMBER_COUNT).inner_text().strip())

    @allure.step("Get visible member row count")
    def get_visible_member_row_count(self) -> int:
        return self.page.locator(locators.TABLE_ROWS).count()

    @allure.step("Get member table header names")
    def get_member_table_header_names(self) -> list[str]:
        """Return data-column header labels in display order (skip checkbox column)."""
        headers = self.page.locator(locators.TABLE_COLUMN_HEADERS)
        names: list[str] = []
        # Index 0 is the select-all checkbox column — not a data header.
        for index in range(1, headers.count()):
            name = headers.nth(index).evaluate(
                """(el) => {
                    const clone = el.cloneNode(true);
                    clone.querySelectorAll('.tooltip-description, .v-icon').forEach((n) => n.remove());
                    return (clone.textContent || '').replace(/\\s+/g, ' ').trim();
                }"""
            )
            names.append(name)
        return names

    @allure.step("Get member id values")
    def get_member_id_values(self) -> list[int]:
        """Lấy danh sách 会員ID của các dòng đang hiển thị."""
        member_ids = self.page.locator(locators.TABLE_ROWS).locator(
            locators.MEMBER_ID_CELL_IN_ROW
        ).all_inner_texts()
        return [int(member_id.strip()) for member_id in member_ids]

    # -----------------------------------------------------------------------
    # Expectations
    # -----------------------------------------------------------------------

    @allure.step("Expect member list heading shows count: {expected_count}")
    def expect_member_list_heading_with_count(self, expected_count: int) -> None:
        expected_text = f"会員リスト（{expected_count}）"
        expect(self.page.locator(locators.MEMBER_LIST_TITLE)).to_contain_text(expected_text)
        assert self.get_member_count() == expected_count, (
            f"Heading count is not {expected_count}"
        )
# -----------------------------------------------------------------------
    # -----------------------------------------------------------------------
    # Navigation (from header nav)
    # -----------------------------------------------------------------------

    @allure.step("Open 会員リスト from home via 会員管理")
    def open(self) -> None:
        """From event-home (access_to_home_screen), open 会員リスト via header nav."""
        self.page.get_by_role("link", name=locators.NAV_MEMBER).click()
        self.page.wait_for_load_state("networkidle")

    # -----------------------------------------------------------------------
    # Table helpers (TC07)
    # -----------------------------------------------------------------------

    def _status_column_index(self) -> int:
        headers = self.page.locator(locators.TABLE_HEADER)
        count = headers.count()
        for index in range(count):
            # Material Icons / tooltip may append extra lines — take first line only
            label = headers.nth(index).inner_text().split("\n")[0].strip()
            if label == locators.STATUS_COLUMN_HEADER:
                return index
        raise AssertionError(MSG_MEMBER_STATUS_COLUMN_MISSING)

    @allure.step("Get all 状態 column values from member table")
    def get_status_column_values(self) -> list[str]:
        status_idx = self._status_column_index()
        rows = self.page.locator(locators.TABLE_ROWS)
        row_count = rows.count()
        if row_count == 0:
            raise AssertionError(MSG_MEMBER_NO_ROWS)

        values: list[str] = []
        for row_index in range(row_count):
            cell_text = rows.nth(row_index).locator("td").nth(status_idx).inner_text().strip()
            values.append(cell_text)
        return values

    @allure.step("Expect every 状態 cell is 有効 or 無効")
    def expect_all_status_values_valid(self) -> None:
        values = self.get_status_column_values()
        for row_index, value in enumerate(values):
            assert value in MEMBER_STATUS_VALID_VALUES, (
                f"{MSG_MEMBER_STATUS_INVALID} (row={row_index + 1}, value={value!r})"
            )

    # -----------------------------------------------------------------------
    # Sub-tab helpers (TC08)
    # -----------------------------------------------------------------------

    def _tab_locator(self, tab_name: str):
        return self.page.locator(locators.SUB_TABS).filter(has_text=tab_name)

    @allure.step("Navigate to sub-tab '{tab_name}' and verify URL / active / panel")
    def navigate_and_verify_tab(self, tab_name: str) -> None:
        if tab_name not in MEMBER_SUB_TABS:
            raise ValueError(f"Unknown member sub-tab: {tab_name!r}")

        expected_hash, panel_key = MEMBER_SUB_TABS[tab_name]
        tab = self._tab_locator(tab_name)
        tab.click()
        self.page.wait_for_load_state("networkidle")

        expect(tab, MSG_MEMBER_TAB_NOT_ACTIVE).to_have_class(
            re.compile(rf".*{re.escape(locators.MEMBER_LIST_TAB_ACTIVE_CLASS)}.*")
        )
        expect(self.page, MSG_MEMBER_TAB_URL_MISMATCH).to_have_url(
            re.compile(re.escape(expected_hash))
        )

        panel = self.page.locator(f"{locators.PANEL_PREFIX}{panel_key}")
        expect(panel, MSG_MEMBER_TAB_PANEL_NOT_VISIBLE).to_be_visible()
        expect(panel.get_by_role("heading", name=tab_name)).to_be_visible()

    @allure.step("Expect search panel is visible with filter fields")
    def expect_search_panel_visible_with_filters(self) -> None:
        """Assert panel tìm kiếm và các trường lọc chính đều hiển thị."""
        expect(self.page.locator(locators.SEARCH_PANEL)).to_be_visible()
        expect(self.page.locator(locators.FILTER_MEMBER_ID_INPUT)).to_be_visible()
        expect(self.page.locator(locators.FILTER_LOGIN_ID_INPUT)).to_be_visible()
        expect(self.page.locator(locators.FILTER_STATUS_SELECT)).to_be_visible()

    def is_member_id_header_sorted_ascending(self) -> bool:
        """Kiểm tra header 会員ID có đang ở trạng thái sort ascending (aria-sort) không."""
        return (
            self.page.locator(locators.MEMBER_ID_HEADER).get_attribute("aria-sort")
            == "ascending"
        )
