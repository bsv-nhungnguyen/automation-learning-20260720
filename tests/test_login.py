import os
import re

import allure
from playwright.sync_api import expect

from constants.messages import MSG_LOGIN_INVALID_CREDENTIALS
from helpers import description_md
from pages.account_page import AccountPage


@allure.feature("アカウント")
@allure.story("ログイン")
@description_md(
    "Test cases ログイン_001 - ログイン_002 - xac nhan luong dang nhap co ban "
    "truoc khi tung team bat dau code testcase rieng cua man hinh minh."
)
class Testアカウント_ログイン:
    # -------------------------------------------------------------------
    # ログイン_001
    # -------------------------------------------------------------------
    @allure.title("ログイン_001: Login với thông tin hợp lệ vào được Event-home")
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
        expect(login.page).to_have_url(re.compile(r".*(event[-_]home|console).*"))
        with allure.step("[PASSED] Login with valid credentials navigates to Event-home"):
            pass

    # -------------------------------------------------------------------
    # ログイン_002
    # -------------------------------------------------------------------
    @allure.title("ログイン_002: Click ログイン with empty email and password shows error message")
    @description_md(
        """
- **前提条件**: Đang ở màn hình login, chưa nhập gì vào 2 ô メールアドレス / パスワード
- **テスト手順**: 1. Không nhập メールアドレス và パスワード
                 2. Nhấn nút ログイン
- **期待する結果**: Vẫn ở màn hình login và hiển thị message
  「メールアドレスまたはパスワードが正しくありません。」
        """
    )
    def test_login_with_empty_credentials_shows_invalid_credentials_message(
        self, access_to_login_screen: AccountPage
    ):
        login = access_to_login_screen
        login.submit_login_expecting_failure()
        login.expect_error_message(MSG_LOGIN_INVALID_CREDENTIALS)
        expect(login.page).not_to_have_url(re.compile(r".*(event[-_]home|console).*"))
        with allure.step("[PASSED] Empty credentials show the invalid credentials message"):
            pass