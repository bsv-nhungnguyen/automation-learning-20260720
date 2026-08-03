import allure

from constants.locators import PushListLocators as locators
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
        self, access_to_push_list_drawer: PushListPage
    ):
        push_list = access_to_push_list_drawer

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
        self, access_to_push_list_drawer: PushListPage
    ):
        push_list = access_to_push_list_drawer

        push_list.expect_target_method_defaults_to_segment()
        push_list.expect_send_type_defaults_to_immediate()

        with allure.step(
            "[PASSED] Default radios are セグメントルールから選ぶ and 即時配信する"
        ):
            pass

    # -------------------------------------------------------------------
    # 配信する_003 (TC03)
    # -------------------------------------------------------------------
    @allure.title("配信する_003: Verify submit button (配信する) is disabled when required fields are empty")
    @description_md(
        """
- **前提条件**: プッシュ配信作成ドロワーを表示中（各入力欄は空の状態）
- **テスト手順**: 1. 何も入力せず、配信するボタンの状態を確認する
- **期待する結果**: 配信するボタンがdisabled状態であること
        """
    )
    def test_submit_button_form_empty_disabled(
        self, access_to_push_list_drawer: PushListPage
    ):
        push_list = access_to_push_list_drawer

        push_list.expect_submit_button_disabled()

        with allure.step("[PASSED] Submit button is disabled when form is empty"):
            pass

    # -------------------------------------------------------------------
    # 配信する_004 (TC04)
    # -------------------------------------------------------------------
    @allure.title("配信する_004: Verify submit button (配信する) becomes enabled after required fields are filled")
    @description_md(
        """
- **前提条件**: プッシュ配信作成ドロワーを表示中（フォームは空の状態）
- **テスト手順**:
  1. 配信管理用タイトルを入力する
  2. セグメントルールを選択する
  3. メッセージを入力する
- **期待する結果**: 配信するボタンがenabled状態に変わること
        """
    )
    def test_submit_button_required_fields_filled_enabled(
        self, access_to_push_list_drawer: PushListPage
    ):
        push_list = access_to_push_list_drawer

        push_list.fill_required_fields(
            title="Automation Push Test",
            segment_rule_label=locators.SEGMENT_RULE_OPTION_1_LABEL,
            message="Nội dung tin nhắn test automation",
        )
        push_list.expect_submit_button_enabled()

        with allure.step("[PASSED] Submit button enabled after required fields filled"):
            pass
    
    # -------------------------------------------------------------------
    # TC05
    # -------------------------------------------------------------------
    @allure.title("TC05: Verify chuyển đổi phương thức tạo đối tượng sang 'CSVからアップロードする'")
    @description_md("""
- **前提条件**: Đang mở màn hình tạo Push Notification
- **テスト手順**:
    1. Chọn radio 「CSVからアップロードする」
- **期待する結果**:
    - Khu vực セグメントルール không hiển thị
    - Hiển thị khu vực upload CSV
        """)
    def test_verify_switch_to_csv_upload(self, access_to_push_list_drawer: PushListPage):
        push_list = access_to_push_list_drawer

        push_list.select_csv_upload()
        push_list.verify_segment_area_hidden()
        push_list.verify_csv_area_displayed()

        with allure.step("[PASSED] CSV upload area displayed"):
            pass

    # -------------------------------------------------------------------
    # TC06
    # -------------------------------------------------------------------
    @allure.title("TC06: Verify giới hạn ký tự (255) của trường 配信管理用タイトル")
    @description_md("""
- **前提条件**: Đang mở màn hình tạo Push Notification
- **テスト手順**:
    1. Nhập chuỗi vượt quá 255 ký tự vào trường 配信管理用タイトル
- **期待する結果**:
    - Chỉ nhập tối đa 255 ký tự
        """)
    def test_verify_title_maxlength_255(self, access_to_push_list_drawer: PushListPage):
        push_list = access_to_push_list_drawer

        push_list.input_title("A" * 300)
        push_list.verify_title_maxlength()

        with allure.step("[PASSED] Title accepts maximum 255 characters"):
            pass