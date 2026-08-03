import re

import allure
from playwright.sync_api import Page, expect

from constants.locators import MemberListPageLocators as locators
from pages.base_page import BasePage


class MemberListPage(BasePage):
    """会員一覧ページ / Member list page."""

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
        raise AssertionError("Column header '状態' is not visible")

    @allure.step("Get all 状態 column values from member table")
    def get_status_column_values(self) -> list[str]:
        status_idx = self._status_column_index()
        rows = self.page.locator(locators.TABLE_ROWS)
        row_count = rows.count()
        if row_count == 0:
            raise AssertionError("Member table has no data rows")

        values: list[str] = []
        for row_index in range(row_count):
            cell_text = rows.nth(row_index).locator(locators.TABLE_CELLS).nth(status_idx).inner_text().strip()
            values.append(cell_text)
        return values

    @allure.step("Expect every 状態 cell is 有効 or 無効")
    def expect_all_status_values_valid(self) -> None:
        values = self.get_status_column_values()
        for row_index, value in enumerate(values):
            assert value in ("有効", "無効"), (
                f"Status column value must be '有効' or '無効' and must not be empty "
                f"(row={row_index + 1}, value={value!r})"
            )

    # -----------------------------------------------------------------------
    # Sub-tab helpers
    # -----------------------------------------------------------------------

    def _tab_locator(self, tab_name: str):
        return self.page.locator(locators.SUB_TABS).filter(has_text=tab_name)

    @allure.step("Navigate to member sub-tab: {tab_name}")
    def navigate_to_tab(self, tab_name: str) -> None:
        tab = self._tab_locator(tab_name)
        tab.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Verify sub-tab '{tab_name}' is active with URL and panel")
    def verify_tab(
        self, tab_name: str, expected_hash: str, panel_selector: str
    ) -> None:
        tab = self._tab_locator(tab_name)
        expect(tab, "Sub-tab is not active after navigation").to_have_class(
            re.compile(rf".*{re.escape(locators.MEMBER_LIST_TAB_ACTIVE_CLASS)}.*")
        )
        expect(self.page, "URL hash did not update for the selected sub-tab").to_have_url(
            re.compile(re.escape(expected_hash))
        )
        panel = self.page.locator(panel_selector)
        expect(panel, "Sub-tab panel content is not visible").to_be_visible()
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

    @allure.step("Expect first member row checkbox is checked")
    def expect_first_member_selected(self) -> None:
        """check row đầu tiên to_be_checked。"""
        first_row = self.page.locator(locators.TABLE_ROWS).first
        expect(first_row.locator(locators.ROW_CHECKBOX)).to_be_checked()


    @allure.step("Expect new member registration URL")
    def expect_new_member_registration_url(self) -> None:
        """check url màn hình đăng ký mới member."""
        expect(self.page).to_have_url(re.compile(r".*/member_create\.html$"))
