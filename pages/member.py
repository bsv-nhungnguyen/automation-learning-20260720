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
    """会員管理 / 会員リスト画面."""

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Navigation
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
        rows = self.page.locator(locators.TABLE_BODY_ROW)
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
            re.compile(rf".*{re.escape(locators.TAB_ACTIVE_CLASS)}.*")
        )
        expect(self.page, MSG_MEMBER_TAB_URL_MISMATCH).to_have_url(
            re.compile(re.escape(expected_hash))
        )

        panel = self.page.locator(f"{locators.PANEL_PREFIX}{panel_key}")
        expect(panel, MSG_MEMBER_TAB_PANEL_NOT_VISIBLE).to_be_visible()
        expect(panel.get_by_role("heading", name=tab_name)).to_be_visible()
