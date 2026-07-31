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
    @allure.title("TC08: Verify nút キャンセル,close và không lưu dữ liệu")
    @description_md( """
- **前提条件**: Đang mở màn hình tạo Push Notification
- **テスト手順**:
    1. Nhập Title
    2. Nhập Message
    3. Click 「キャンセル」hoặc 「X]
- **期待する結果**:
    - Modal đóng
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

    def test_verify_close_button_close_modal_without_saving(self, access_to_push_list: PushListPage):
        push_list = access_to_push_list
        push_list.input_title("Automation Test")
        push_list.input_message("Automation Message")
        push_list.click_close()
        push_list.verify_modal_closed()
    
        push_list.open_create_push_modal()
        push_list.verify_title_cleared()
        push_list.verify_message_cleared()
    
        with allure.step("[PASSED] Cancel closes drawer without saving data"):
            pass