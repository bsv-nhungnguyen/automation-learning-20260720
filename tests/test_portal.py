import os
from pathlib import Path

import allure
from playwright.sync_api import Page

from helpers import description_md
from pages.portal_page import PortalPage

TESTDATA_DIR = Path(__file__).resolve().parents[1] / "testdata"
PORTAL_ICON_PNG = TESTDATA_DIR / "portal_icon_100x100.png"
PORTAL_ICON_JPG = TESTDATA_DIR / "portal_icon_100x100.jpg"
PORTAL_HOME_PATH = "/portal_home.html"


@allure.feature("ポータル")
@allure.story("ポータルホーム")
@allure.link(
    f"{os.getenv('APP_URL', '').rstrip('/')}{PORTAL_HOME_PATH}",
    name="Portal home",
)
@description_md(
    "Test cases ポータル_001 – ポータル_008 in file portal home — "
    "verify portal name validation and portal icon upload section."
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
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
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
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
        portal.expect_save_button_disabled()
        with allure.step("[PASSED] Save button is disabled when form is empty"):
            pass

    # -------------------------------------------------------------------
    # ポータル_003
    # -------------------------------------------------------------------
    @allure.title(
        "ポータル_003: Verify nhập ポータル名 hợp lệ làm enable nút 保存する"
    )
    @description_md(
        """
- **前提条件**: Mở trang portal home, ô ポータル名 đang trống
- **テスト手順**:
  1. Kiểm tra nút 保存する đang disabled
  2. Nhập「Automation Portal Test」vào ô ポータル名
- **期待する結果**: Nút 保存する chuyển từ disabled sang enabled
        """
    )
    def test_save_button_is_enabled_after_entering_portal_name(
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)

        portal.expect_save_button_disabled()
        portal.enter_portal_name("Automation Portal Test")
        portal.expect_save_button_enabled()

        with allure.step(
            "[PASSED] Save button is enabled after entering portal name"
        ):
            pass

    # -------------------------------------------------------------------
    # ポータル_004
    # -------------------------------------------------------------------
    @allure.title(
        "ポータル_004: Verify giá trị nhập vào ô ポータル名 được giữ đúng"
    )
    @description_md(
        """
- **前提条件**: Mở trang portal home
- **テスト手順**:
  1. Nhập chuỗi có tiếng Nhật, tiếng Việt và khoảng trắng vào ô ポータル名
  2. Lấy giá trị thực tế của input bằng input_value()
- **期待する結果**: Giá trị được giữ nguyên, không bị cắt hoặc sai encoding
        """
    )
    def test_portal_name_value_is_preserved(
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)

        portal_name = "自動化テスト Cổng thông tin"
        portal.enter_portal_name(portal_name)
        portal.expect_portal_name_value(portal_name)

        with allure.step(
            "[PASSED] Portal name value is preserved correctly"
        ):
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
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
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
- **テスト手順**:
  1. Kiểm tra input #portal_icon tồn tại / accept chứa .png/.jpg
  2. Upload ảnh PNG từ testdata/portal_icon_100x100.png
  3. Upload ảnh JPG từ testdata/portal_icon_100x100.jpg
- **期待する結果**: type=file, accept chứa .png/.jpg; upload PNG và JPG đều thành công (preview + filename)
        """
    )
    def test_file_input_accepts_png_and_jpg(
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
        portal.expect_file_input_accepts_png_jpg(PORTAL_ICON_PNG)
        portal.expect_file_input_accepts_png_jpg(PORTAL_ICON_JPG)
        with allure.step(
            "[PASSED] File input accepts PNG/JPG and upload works for both"
        ):
            pass

    # -------------------------------------------------------------------
    # ポータル_007
    # -------------------------------------------------------------------
    @allure.title(
        "ポータル_007: Verify icon tooltip (?) hiển thị nội dung khi hover/click"
    )
    @description_md(
        """
- **前提条件**: Mở trang portal home
- **テスト手順**:
  1. Hover (hoặc click) icon (?) cạnh ポータル名
  2. Hover (hoặc click) icon (?) cạnh ポータルアイコン
- **期待する結果**: Tooltip/popup xuất hiện với nội dung hướng dẫn tương ứng
        """
    )
    def test_portal_help_tooltips_show_guide_content_on_hover(
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
        portal.hover_portal_name_tooltip_button()
        portal.expect_portal_name_tooltip_content()
        portal.hover_portal_icon_tooltip_button()
        portal.expect_portal_icon_tooltip_content()
        with allure.step(
            "[PASSED] Portal name and icon tooltips show guide content on hover"
        ):
            pass

    # -------------------------------------------------------------------
    # ポータル_008
    # -------------------------------------------------------------------
    @allure.title(
        "ポータル_008: Verify tab 'ポータル' ở trạng thái active khi đang ở trang này"
    )
    @description_md(
        """
- **前提条件**: Điều hướng tới trang portal-home
- **テスト手順**: 1. Kiểm tra tab navigation trên header
- **期待する結果**: Tab ポータル có class/màu active (gạch cam); các tab khác không active
        """
    )
    def test_portal_nav_tab_is_active_on_portal_home(
        self, page: Page, app_url: str
    ):
        portal = PortalPage(page)
        portal.open_portal_screen(app_url)
        portal.expect_nav_tab_active("ポータル")
        with allure.step(
            "[PASSED] ポータル tab is active with orange underline; other tabs are not"
        ):
            pass
