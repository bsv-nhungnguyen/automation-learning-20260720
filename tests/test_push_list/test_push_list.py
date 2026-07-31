import allure
from helpers import description_md

from pages.push_list_page import PushListPage


class Testプッシュ配信一覧:

    # -------------------------------------------------------------------
    # TC07
    # -------------------------------------------------------------------
    @allure.title("TC07: Verify chuyển 配信タイプ sang '予約配信する' hiển thị trường ngày giờ")
    @description_md( """
- **前提条件**: Đang mở màn hình tạo Push Notification
- **テスト手順**:
    1. Chọn radio 「予約配信する」
- **期待する結果**:
    - Hiển thị khu vực đặt lịch
    - Hiển thị trường 配信日
    - Hiển thị trường 配信時刻
        """)
    
    def test_verify_schedule_delivery_show_datetime_fields(self, access_to_push_list: PushListPage):
        push_list = access_to_push_list
        push_list.select_scheduled_delivery()
        push_list.verify_schedule_area_displayed()
        push_list.verify_schedule_date_displayed()
        push_list.verify_schedule_time_displayed()

        with allure.step("[PASSED] Schedule delivery displays date and time fields"):
            pass

    # -------------------------------------------------------------------
    # TC08
    # -------------------------------------------------------------------
    @allure.title("TC08: Verify nút キャンセル đóng drawer và không lưu dữ liệu")
    @description_md( """
- **前提条件**: Đang mở màn hình tạo Push Notification
- **テスト手順**:
    1. Nhập Title
    2. Nhập Message
    3. Click 「キャンセル」
- **期待する結果**:
    - Drawer đóng
    - Không lưu dữ liệu
        """)
    
    def test_verify_cancel_button_close_modal_without_saving(self, access_to_push_list: PushListPage):
        push_list = access_to_push_list
        push_list.input_title("Automation Test")
        push_list.input_message("Automation Message")
        push_list.click_cancel()
        push_list.verify_modal_closed()

        push_list.open_create_push_modal()
        push_list.verify_title_cleared()
        push_list.verify_message_cleared()

        with allure.step("[PASSED] Cancel closes drawer without saving data"):
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
    def test_verify_switch_to_csv_upload(self, access_to_push_list: PushListPage):
        push_list = access_to_push_list

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
    def test_verify_title_maxlength_255(self, access_to_push_list: PushListPage):
        push_list = access_to_push_list

        push_list.input_title("A" * 300)
        push_list.verify_title_maxlength()

        with allure.step("[PASSED] Title accepts maximum 255 characters"):
            pass