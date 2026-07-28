import os

import pytest
from playwright.sync_api import Page

from pages.account_page import AccountPage
from pages.member_list_page import MemberListPage


@pytest.fixture
def access_to_member_list_screen(page: Page, app_url: str) -> MemberListPage:
    """Login (sample UI chấp nhận account bất kỳ) rồi mở màn 会員リスト."""
    page.goto(f"{app_url}/login.html")
    page.wait_for_load_state("networkidle")
    login = AccountPage(page)
    login.login(
        os.getenv("VALID_EMAIL", "any@example.com"),
        os.getenv("VALID_PASSWORD", "any_password"),
    )
    page.goto(f"{app_url}/member_list.html")
    page.wait_for_load_state("networkidle")
    return MemberListPage(page)
