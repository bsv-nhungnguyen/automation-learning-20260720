import allure
from playwright.sync_api import Page

from pages.event_home_page import EventHomePage


@allure.story("Event Home Page")
class TestEventHomePage:
    @allure.title("Verify navigation tabs are visible")
    def test_01_verify_nav_tabs_render_correctly(self, access_to_home_screen: Page):
        event_home_page = EventHomePage(access_to_home_screen)
        assert event_home_page.navigate_tabs_count() == 5
        assert event_home_page.navigate_tab_render_correctly()
        expected_tab_names = [
        "イベント",
    "ポータル",
    "会員管理",
    "配信する",
    "レポート"
]

assert event_home_page.get_navigation_tab_names() == expected
        assert event_home_page.is_tab_active("イベント") is True
        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
