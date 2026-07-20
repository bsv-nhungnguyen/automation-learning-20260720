import os
import re

import allure
from playwright.sync_api import expect

from constants.messages import MSG_LOGIN_FAILED_INPUT_CHECK
from helpers import description_md
from pages.account_page import AccountPage


@allure.feature("アカウント")
@allure.story("ログイン")
@description_md(
    "Test cases ログイン_001 – ログイン_002 - xac nhan luong dang nhap co ban "
    "truoc khi tung team bat dau code testcase rieng cua man hinh minh."
)
class Testアカウント_ログイン:

    # -------------------------------------------------------------------
    # ログイン_001
    # -------------------------------------------------------------------
    @allure.title("ログイン_001: Login với thông tin không hợp lệ hiển thị lỗi")
    @description_md(
        """
- **前提条件**: Đang ở màn hình login
- **テスト手順**: 1. Nhập email/password không hợp lệ rồi nhấn ログイン
- **期待する結果**: Hiển thị thông báo lỗi đăng nhập thất bại
        """
    )
    def test_login_with_invalid_credentials_shows_error(
        self, access_to_login_screen: AccountPage
    ):
        login = access_to_login_screen
        login.input_email("invalid_user@example.com")
        login.input_password("invalid_pass")
        login.click_login()
        expect(login.page.get_by_text(MSG_LOGIN_FAILED_INPUT_CHECK)).to_be_visible()
        with allure.step("[PASSED] Login with invalid credentials shows error message"):
            pass

    # -------------------------------------------------------------------
    # ログイン_002
    # -------------------------------------------------------------------
    @allure.title("ログイン_002: Login với thông tin hợp lệ vào được Event-home")
    @description_md(
        """
- **前提条件**: Đang ở màn hình login, đã có VALID_EMAIL/VALID_PASSWORD trong .env
- **テスト手順**: 1. Nhập email/password hợp lệ rồi nhấn ログイン
- **期待する結果**: Chuyển vào màn hình Event-home (console) thành công
        """
    )
    def test_login_with_valid_credentials_navigates_to_event_home(
        self, access_to_login_screen: AccountPage
    ):
        login = access_to_login_screen
        login.login(
            os.getenv("VALID_EMAIL"),
            os.getenv("VALID_PASSWORD"),
        )
        expect(login.page).to_have_url(re.compile(r".*(event-home|console).*"))
        with allure.step("[PASSED] Login with valid credentials navigates to Event-home"):
            pass
