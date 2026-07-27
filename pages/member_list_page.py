import allure
from playwright.sync_api import Page

from constants.locators import MemberListPageLocators
from pages.base_page import BasePage


class MemberListPage(BasePage):
    """会員一覧ページ / Member list page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------      

    @allure.step("Open member search panel")
    def open_search_panel(self) -> None:
        self.click(MemberListPageLocators.SEARCH_BUTTON)
    
    @allure.step("Sort member list by member ID")
    def sort_by_member_id(self) -> None:
        self.click(MemberListPageLocators.MEMBER_ID_HEADER)

    @allure.step("Select the first member row")
    def select_first_member(self) -> None:
        first_row = self.page.locator(MemberListPageLocators.TABLE_ROWS).first
        first_row.locator(MemberListPageLocators.ROW_CHECKBOX).check()

    @allure.step("Navigate to new member registration")
    def navigate_to_new_member_registration(self) -> None:
        self.click(MemberListPageLocators.NEW_MEMBER_REGISTRATION_BUTTON)
        self.page.wait_for_load_state("networkidle")

    SUB_TAB_LOCATORS = {
    "会員リスト": MemberListPageLocators.MEMBER_LIST_TAB,
    "会員属性の設定": MemberListPageLocators.MEMBER_ATTRIBUTE_SETTINGS_TAB,
    "会員登録フォーム": MemberListPageLocators.MEMBER_REGISTRATION_FORM_TAB,
    "アプリ利用者": MemberListPageLocators.APP_USERS_TAB,
    "会員退会設定": MemberListPageLocators.MEMBER_WITHDRAWAL_SETTINGS_TAB,
    }

    @allure.step("Navigate to member sub-tab: {tab_name}")
    def navigate_to_tab(self, tab_name: str) -> None:
        """指定した会員管理サブタブへ遷移する。"""
        try:
            tab_locator = self.SUB_TAB_LOCATORS[tab_name]
        except KeyError as exc:
            raise ValueError(f"Unsupported member sub-tab: {tab_name}") from exc

        self.click(tab_locator)
    
    # -----------------------------------------------------------------------
    # Boolean / data helpers
    # -----------------------------------------------------------------------
    @allure.step("get number of members")
    def get_member_count(self) -> int:
        text = self.page.locator(MemberListPageLocators.MEMBER_COUNT).inner_text()
        parsed_text = "".join(filter(str.isdigit, text))
        return int(parsed_text) if parsed_text else 0

    @allure.step("get member table header names")
    def get_member_table_header_names(self) -> list[str]:
        all_headers = self.page.locator(
            MemberListPageLocators.TABLE_COLUMN_HEADERS
        ).all_inner_texts()
        return [header.strip() for header in all_headers[1:]]

    @allure.step("get member id values")
    def get_member_id_values(self) -> list[int]:
        """Lấy danh sách 会員ID của các dòng đang hiển thị."""
        member_ids = self.page.locator(
            MemberListPageLocators.TABLE_ROWS
        ).locator(MemberListPageLocators.MEMBER_ID_CELL_IN_ROW).all_inner_texts()
        return [int(member_id.strip()) for member_id in member_ids]

    
