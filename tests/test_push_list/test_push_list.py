import allure
from helpers import description_md

from pages.push_list_page import PushListPage


class Testプッシュ配信一覧:
        
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