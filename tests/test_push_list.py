import allure
from playwright.sync_api import Page

from helpers import description_md
from pages.push_list_page import PushListPage


@allure.feature("プッシュ配信")
@allure.story("配信する")
@description_md(
    "Test cases 配信する_001 - 配信する_002 trong file "
    "'Training_Automation_Sprint1 - 04_Push-list.csv' (TC01-02, phu trach: Phi) - "
    "verify cac truong bat buoc (*) va gia tri mac dinh cua 2 nhom radio button "
    "trong form/drawer tao chien dich day tin (プッシュ配信新規作成)."
)
class Testプッシュ配信_配信する:

    # -------------------------------------------------------------------
    # 配信する_001 (TC01)
    # -------------------------------------------------------------------
    @allure.title("配信する_001: Verify required fields are marked with (*) in push creation form")
    @description_md(
        """
- **前提条件**: プッシュ配信一覧画面を表示中
- **テスト手順**: 1. 「新規作成」ボタンを押下し、プッシュ配信作成ドロワーを開く
- **期待する結果**:
  - 配信管理用タイトルのラベル横に必須マーク（*）が表示されること
  - セグメントルールを選択するのラベル横に必須マーク（*）が表示されること
  - メッセージのラベル横に必須マーク（*）が表示されること
        """
    )
    def test_push_create_form_required_fields_show_asterisk(
        self, access_to_home_screen: Page, app_url: str
    ):
        push_list = PushListPage(access_to_home_screen)
        push_list.navigate_to_push_list(app_url)
        push_list.open_create_drawer()

        push_list.expect_title_required_mark_visible()
        push_list.expect_segment_required_mark_visible()
        push_list.expect_message_required_mark_visible()

        with allure.step(
            "[PASSED] 配信管理用タイトル / セグメントルールを選択する / メッセージ "
            "are marked with required (*) mark"
        ):
            pass

    # -------------------------------------------------------------------
    # 配信する_002 (TC02)
    # -------------------------------------------------------------------
    @allure.title("配信する_002: Verify default radio selections in push creation form")
    @description_md(
        """
- **前提条件**: プッシュ配信作成ドロワーを表示中（初期状態）
- **テスト手順**: 1. 「新規作成」ボタンを押下し、プッシュ配信作成ドロワーを開いた直後の各ラジオボタングループの選択状態を確認する
- **期待する結果**:
  - 「配信する対象の作成方法」で「セグメントルールから選ぶ」がデフォルトで選択されていること
  - 「配信タイプ」で「即時配信する」がデフォルトで選択されていること
        """
    )
    def test_push_create_form_default_radios_are_preselected(
        self, access_to_home_screen: Page, app_url: str
    ):
        push_list = PushListPage(access_to_home_screen)
        push_list.navigate_to_push_list(app_url)
        push_list.open_create_drawer()

        push_list.expect_target_method_defaults_to_segment()
        push_list.expect_send_type_defaults_to_immediate()

        with allure.step(
            "[PASSED] Default radios are セグメントルールから選ぶ and 即時配信する"
        ):
            pass
