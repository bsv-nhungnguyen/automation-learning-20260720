import re
import allure
from helpers import description_md
from playwright.sync_api import Page

from constants.locators import EventHomeLocators
from pages.event_home_page import EventHomePage


@allure.story("Event Home Page")
class TestEventHomePage:
    @allure.title("Verify navigation tabs are visible")
    def test_01_verify_nav_tabs_are_displayed(self, access_to_home_screen: Page):
        event_home_page = EventHomePage(access_to_home_screen)
        expected_tab_names = [
            EventHomeLocators.EVENT_TAB,
            EventHomeLocators.PORTAL_TAB,
            EventHomeLocators.MEMBER_TAB,
            EventHomeLocators.MAIL_TAB,
            EventHomeLocators.REPORT_TAB,
        ]
        assert event_home_page.get_navigation_tab_names() == expected_tab_names
        assert event_home_page.is_navigation_tab_order_correct()
        assert event_home_page.is_tab_active(EventHomeLocators.EVENT_TAB) is True
        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    @allure.title("Verify usage widgets are displayed")
    def test_02_verify_usage_widgets_are_displayed(self, access_to_home_screen: Page):
        event_home_page = EventHomePage(access_to_home_screen)
        assert event_home_page.is_usage_label_visible(EventHomeLocators.DAU_LABEL) is True
        event_home_page.hover_tooltip_by_label(EventHomeLocators.DAU_LABEL)

        assert event_home_page.is_tooltip_content_visible(
            EventHomeLocators.DAU_TOOLTIP_CONTENT) is True

        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        assert event_home_page.is_usage_label_visible(EventHomeLocators.MEMBER_LABEL) is True
        event_home_page.hover_tooltip_by_label(EventHomeLocators.MEMBER_LABEL)
        
        assert event_home_page.is_tooltip_content_visible(
            EventHomeLocators.MEMBER_TAB_TOOLTIP_CONTENT) is True
       
        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    @allure.title("Event-home_007: Verify event table column headers")
    def test_event_table_headers_are_displayed(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)

        actual = event_home.get_event_table_header_names()
        expected = EventHomeLocators.EVENT_TABLE_COLUMN_HEADERS

        assert actual == expected, f"Headers mismatch.\nExpected: {expected}\nActual: {actual}"

        with allure.step("[PASSED] Event table has 11 correct column headers"):
            pass

    @allure.title("Event-home_008: Verify create button and grid/list toggle")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Click 新規イベント作成 2. Đóng form 3. Toggle grid/list
- **期待する結果**: Form mở; layout đổi đúng
        """
    )
    def test_create_button_and_view_toggle(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)

        event_home.click_create_event()
        event_home.expect_create_event_form_visible()
        event_home.close_create_event_form()

        event_home.click_grid_view()
        event_home.expect_grid_view_displayed()

        event_home.click_list_view()
        event_home.expect_list_view_displayed()

        with allure.step("[PASSED] Create opens form; grid/list toggle switches layout"):
            pass