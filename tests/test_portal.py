import os
from pathlib import Path

import allure

from helpers import description_md
from pages.portal_page import PortalPage

PORTAL_ICON_PNG = Path(__file__).resolve().parents[1] / "testdata" / "portal_icon_100x100.png"


@allure.feature("ポータル")
@allure.story("ポータルホーム")
@allure.link(os.getenv("PORTAL_URL") or "", name="Portal home")
@description_md(
    "Test cases ポータル_001 – ポータル_002, ポータル_005 – ポータル_006 in file "
    "portal home — verify required mark, disabled save, icon guide, and file upload."
)
class Testポータル_ホーム:

    # -------------------------------------------------------------------
    # ポータル_001
    # -------------------------------------------------------------------
    @allure.title("ポータル_001: Verify dấu ※必須 cạnh ポータル名")
    @description_md(
        """
- **前提条件**: Mở trang portal home
- **テスト手順**: 1. Kiểm tra label ポータル名 và dấu ※必須
- **期待する結果**: Dấu ※必須 màu đỏ hiển thị đúng cạnh label ポータル名
        """
    )
    def test_portal_name_required_mark_is_displayed(
        self, access_to_portal_screen: PortalPage
    ):
        portal = access_to_portal_screen
        portal.expect_required_mark_visible()
        portal.expect_required_mark_color()
        with allure.step("[PASSED] Required mark ※必須 is displayed in red next to ポータル名"):
            pass

    # -------------------------------------------------------------------
    # ポータル_002
    # -------------------------------------------------------------------
    @allure.title("ポータル_002: Verify nút 保存する disable khi form trống")
    @description_md(
        """
- **前提条件**: Mở trang portal home, chưa nhập gì
- **テスト手順**: 1. Kiểm tra trạng thái nút 保存する
- **期待する結果**: Nút 保存する ở trạng thái disabled (màu xám)
        """
    )
    def test_save_button_is_disabled_when_form_empty(
        self, access_to_portal_screen: PortalPage
    ):
        portal = access_to_portal_screen
        portal.expect_save_button_disabled()
        with allure.step("[PASSED] Save button is disabled when form is empty"):
            pass

    # -------------------------------------------------------------------
    # ポータル_005
    # -------------------------------------------------------------------
    @allure.title("ポータル_005: Portal icon section hiển thị đúng nội dung hướng dẫn")
    @description_md(
        """
- **前提条件**: Đang ở màn hình portal
- **テスト手順**: 1. Xác nhận khu vực ポータルアイコン
- **期待する結果**: Hiển thị placeholder, nút ファイルを選択 và 3 dòng hướng dẫn kích thước/format
        """
    )
    def test_portal_icon_section_content_is_displayed(
        self, access_to_portal_screen: PortalPage
    ):
        portal = access_to_portal_screen
        portal.expect_icon_section_content()
        with allure.step("[PASSED] Portal icon section content is displayed"):
            pass

    # -------------------------------------------------------------------
    # ポータル_006
    # -------------------------------------------------------------------
    @allure.title("ポータル_006: File input tương tác được và accept PNG/JPG")
    @description_md(
        """
- **前提条件**: Đang ở màn hình portal
- **テスト手順**: 1. Kiểm tra input #portal_icon tồn tại / accept  2. Upload ảnh PNG
- **期待する結果**: type=file, accept chứa .png/.jpg, upload thành công (preview + filename)
        """
    )
    def test_file_input_accepts_png_and_jpg(
        self, access_to_portal_screen: PortalPage
    ):
        portal = access_to_portal_screen
        portal.expect_file_input_accepts_png_jpg()
        portal.upload_portal_icon(str(PORTAL_ICON_PNG))
        portal.expect_portal_icon_uploaded(PORTAL_ICON_PNG.name)
        with allure.step("[PASSED] File input accepts PNG/JPG and upload works"):
            pass
