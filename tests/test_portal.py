import allure
from playwright.sync_api import Page, expect

from helpers import description_md
from pages.portal_page import PortalPage

REQUIRED_MARK_COLOR = "rgb(229, 57, 53)"  # #e53935 — màu đỏ ※必須 trên sample UI


@allure.feature("ポータル")
@allure.story("ポータルホーム")
@description_md(
    "Test cases ポータル_001 – ポータル_002 - verify required label and "
    "save button disabled when portal form is empty."
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
    def test_portal_name_required_mark_is_displayed(self, page: Page):
        portal = PortalPage(page)
        portal.open()
        portal.expect_required_mark_visible()
        expect(portal.required_mark()).to_have_css("color", REQUIRED_MARK_COLOR)
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
    def test_save_button_is_disabled_when_form_empty(self, page: Page):
        portal = PortalPage(page)
        portal.open()
        portal.expect_save_button_disabled()
        with allure.step("[PASSED] Save button is disabled when form is empty"):
            pass
