import allure
from playwright.sync_api import Page

from helpers import description_md
from pages.member_list_page import MemberListPage

# Expected UI text for 会員リスト
MEMBER_LIST_HEADING_WITH_COUNT = "会員リスト（{count}）"
REQUIRED_MEMBER_LIST_COLUMNS = [
    "会員ID",
    "ユーザーID",
    "外部連携用ユーザーID",
    "ログインID",
    "管理用メモ",
    "状態",
    "登録日",
]


@allure.feature("会員管理")
@allure.story("会員リスト")
@description_md(
    "Test cases 会員リスト_001 – 会員リスト_004"
)
class Test会員管理_会員リスト:

    # -------------------------------------------------------------------
    # 会員リスト_001
    # -------------------------------------------------------------------
    @allure.title(
        "会員リスト_001: Verify tab '会員リスト' active mặc định và đúng số lượng"
    )
    @description_md(
        """
- **前提条件**: Đã login (account bất kỳ) và đang ở màn hình 会員リスト
- **テスト手順**: 1. Quan sát tab 会員リスト và số lượng 会員
- **期待する結果**:
  - Tab 会員リスト đang active mặc định
  - Text 会員リスト（3） hiển thị đúng số lượng 会員 hiện tại
        """
    )
    def test_member_list_tab_is_active_by_default_and_shows_correct_count(
        self, access_to_home_screen: Page, app_url: str
    ):
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        assert member_list.is_member_list_tab_active(), (
            "会員リスト tab is not active by default"
        )

        expected_count = member_list.get_member_count()
        member_list.expect_member_list_heading_with_count(expected_count)
        assert expected_count == member_list.get_visible_member_row_count(), (
            "Heading member count does not match visible table rows: "
            f"heading={expected_count}, rows={member_list.get_visible_member_row_count()}"
        )

        with allure.step(
            f"[PASSED] 会員リスト tab is active and heading shows {expected_count}"
        ):
            pass

    # -------------------------------------------------------------------
    # 会員リスト_002
    # -------------------------------------------------------------------
    @allure.title(
        "会員リスト_002: Verify header cột của bảng 会員リスト"
    )
    @description_md(
        """
- **前提条件**: Đã login (account bất kỳ) và đang ở màn hình 会員リスト
- **テスト手順**: 1. Quan sát header các cột của bảng 会員リスト
- **期待する結果**: Hiển thị đúng 7 cột theo thứ tự
  会員ID / ユーザーID / 外部連携用ユーザーID / ログインID / 管理用メモ / 状態 / 登録日
        """
    )
    def test_member_list_table_headers_are_displayed_in_correct_order(
        self, access_to_home_screen: Page, app_url: str
    ):
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        actual_headers = member_list.get_member_table_header_names()
        assert actual_headers == REQUIRED_MEMBER_LIST_COLUMNS, (
            "会員リスト table headers mismatch: "
            f"expected {REQUIRED_MEMBER_LIST_COLUMNS}, got {actual_headers}"
        )
        assert len(actual_headers) == 7, (
            f"Expected exactly 7 columns, got {len(actual_headers)}"
        )

        with allure.step(
            f"[PASSED] 会員リスト table shows 7 headers in the expected order: {REQUIRED_MEMBER_LIST_COLUMNS}"
        ):
            pass
        
    # -------------------------------------------------------------
    # 会員リスト_003
    # -------------------------------------------------------------
    @allure.title(
        "会員リスト_003: Verify sắp xếp theo 会員ID sau khi click header"
    )
    @description_md(
        """
        - **前提条件**: Đã login (account bất kỳ) và đang ở màn hình 会員リスト
        - **テスト手順**: 1. Click header 会員ID (có mũi tên ↑)
        - **期待する結果**: Dữ liệu bảng được sắp xếp tăng dần theo 会員ID
        """
    )
    def test_member_id_column_sorted_ascending_after_clicking_header(
        self, access_to_home_screen: Page, app_url: str
    ):
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        member_ids_before = member_list.get_member_id_values()

        member_list.sort_by_member_id()

        member_ids_after = member_list.get_member_id_values()
        assert member_ids_after == sorted(member_ids_before), (
            f"会員ID column is not sorted ascending after clicking header: "
            f"before={member_ids_before}, after={member_ids_after}"
        )
        assert member_list.is_member_id_header_sorted_ascending(), (
            "会員ID header aria-sort attribute is not 'ascending' after clicking"
        )

        with allure.step(
            f"[PASSED] 会員ID column sorted ascending: {member_ids_after}"
        ):
            pass

    # -------------------------------------------------------------
    # 会員リスト_004
    # -------------------------------------------------------------
    @allure.title(
        "会員リスト_004: Verify nút 検索 mở panel tìm kiếm"
    )
    @description_md(
        """
        - **前提条件**: Đã login (account bất kỳ) và đang ở màn hình 会員リスト
        - **テスト手順**: 1. Click nút 検索 (màu đen)
        - **期待する結果**: Panel tìm kiếm xuất hiện với các trường lọc: 会員ID, ログインID, 状態
        """
    )
    def test_search_panel_opens_with_filter_fields_after_clicking_search_button(
        self, access_to_home_screen: Page, app_url: str
    ):
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        member_list.open_search_panel()
        member_list.expect_search_panel_visible_with_filters()

        with allure.step(
            "[PASSED] Search panel opened with all filter fields visible"
        ):
            pass