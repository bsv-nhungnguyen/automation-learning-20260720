import pytest
from playwright.sync_api import Page

from pages.push_list_page import PushListPage


@pytest.fixture
def access_to_push_list(access_to_home_screen: Page) -> PushListPage:
    page = access_to_home_screen
    push_list = PushListPage(page)
    push_list.click_delivery_button()
    push_list.click_delivery_list()
    push_list.open_create_push_modal()
    page.wait_for_load_state("networkidle")

    return push_list