import allure

from helpers import description_md
from pages.member import MEMBER_SUB_TABS, MemberListPage


@allure.feature("会員管理")
@allure.story("会員リスト")
@description_md(
    "Test cases 会員リスト_007 – 会員リスト_008 in file "
    "Training_Automation_Sprint1.xlsx — シート: 03_Member"
)
class Test会員管理_会員リスト:

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
