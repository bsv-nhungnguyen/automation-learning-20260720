import allure
from playwright.sync_api import Page, expect

from constants.locators import MemberListPageLocators as locators
from pages.base_page import BasePage


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
