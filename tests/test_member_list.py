import allure
from playwright.sync_api import Page

from helpers import description_md
from pages.member_list_page import MemberListPage, MEMBER_SUB_TABS

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
                
                
    # -------------------------------------------------------------------
    # 会員リスト_007
    # -------------------------------------------------------------------
    @allure.title("会員リスト_007: Verify cột 状態 hiển thị giá trị hợp lệ cho từng dòng")
    @description_md(
        """
- **前提条件**: 会員リスト画面を表示中
- **テスト手順**: 1. テーブルの各行について状態列の値を確認する
- **期待する結果**: 各行の状態が「有効」または「無効」であり、空欄でないこと
        """
    )
    def test_member_list_status_column_values_are_valid(
        self, access_to_home_screen
    ):
        member = MemberListPage(access_to_home_screen)
        member.open()
        member.expect_all_status_values_valid()
        with allure.step("[PASSED] All 状態 column values are 有効 or 無効"):
            pass

        # -------------------------------------------------------------------
    # 会員リスト_008
    # -------------------------------------------------------------------
    @allure.title(
        "会員リスト_008: Verify chuyển đổi giữa các sub-tab "
        "(会員属性の設定, 会員登録フォーム, アプリ利用者, 会員退会設定)"
    )
    @description_md(
        """
- **前提条件**: 会員リスト画面を表示中
- **テスト手順**:
  - 1. サブタブ「会員属性の設定」を押下する
  - 2. サブタブ「会員登録フォーム」を押下する
  - 3. サブタブ「アプリ利用者」を押下する
  - 4. サブタブ「会員退会設定」を押下する
- **期待する結果**:
  - 各サブタブ押下後に URL / パネル内容が切り替わること
  - 押下したサブタブがアクティブ状態になること
        """
    )
    def test_member_list_sub_tabs_navigation_updates_url_and_active_state(
        self, access_to_home_screen
    ):
        member = MemberListPage(access_to_home_screen)
        member.open()
        for tab_name in MEMBER_SUB_TABS:
            member.navigate_and_verify_tab(tab_name)
        with allure.step("[PASSED] All member sub-tabs navigate and activate correctly"):
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
    # -------------------------------------------------------------------
    # 会員リスト_005
    # -------------------------------------------------------------------
    @allure.title("会員リスト_005: Verify first member row checkbox is selected")
    @description_md(
        """
        - **前提条件**: Đã đăng nhập và đang hiển thị màn hình danh sách thành viên
        - **テスト手順**: 1. Chọn checkbox ở dòng thành viên đầu tiên
        - **期待する結果**: Checkbox chuyển sang trạng thái đã chọn (checked)
        """
    )
    def test_first_member_row_checkbox_is_selected(
        self,
        access_to_home_screen: Page,
        app_url: str,
    ) -> None:
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        member_list.select_first_member()
        member_list.expect_first_member_selected()

        with allure.step("[PASSED] First member row checkbox is checked"):
            pass

    # -------------------------------------------------------------------
    # 会員リスト_006
    # -------------------------------------------------------------------
    @allure.title("会員リスト_006: Verify new member registration navigation")
    @description_md(
        """
        - **前提条件**: Đã đăng nhập và đang hiển thị màn hình danh sách thành viên
        - **テスト手順**: 1. Nhấn nút "Đăng ký thành viên mới" (新規会員登録)
        - **期待する結果**: Chuyển hướng sang màn hình đăng ký thành viên mới
        """
    )
    def test_new_member_registration_button_navigates_to_registration_screen(
        self,
        access_to_home_screen: Page,
        app_url: str,
    ) -> None:
        member_list = MemberListPage(access_to_home_screen)
        member_list.open_member_list_screen(app_url)

        member_list.navigate_to_new_member_registration()
        member_list.expect_new_member_registration_url()

        with allure.step("[PASSED] New member registration screen is displayed"):
            pass