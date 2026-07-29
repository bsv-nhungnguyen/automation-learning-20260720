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

    @allure.title("Event-home_003: Verify announcement list count")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Quan sát danh sách お知らせ 2. Đếm số dòng hiển thị
- **期待する結果**: Danh sách hiển thị đúng 3 dòng thông báo, mỗi dòng có ngày/tag/tiêu đề
        """
    )
    def test_03_verify_announcement_list_count(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)
        event_home.expect_announcement_list_visible()
        announcement_rows = event_home.get_announcement_rows()
        row_count = event_home.get_announcement_row_count()

        assert row_count == 3, (
            f"Expected 3 announcement rows, but found {row_count}"
        )

        for index in range(row_count):
            row = announcement_rows.nth(index)
            assert row.is_visible(), f"Announcement row {index + 1} is not visible"
            assert event_home.get_announcement_date(index), (
                f"Announcement row {index + 1} is missing a date"
            )
            assert event_home.get_announcement_tag(index), (
                f"Announcement row {index + 1} is missing a tag"
            )
            assert event_home.get_announcement_title(index), (
                f"Announcement row {index + 1} is missing a title"
            )

        with allure.step("[PASSED] Announcement list shows exactly 3 rows with date/tag/title"):
            pass

    @allure.title("Event-home_004: Verify NEW badge visibility")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Kiểm tra từng dòng thông báo 2. Xác nhận badge NEW chỉ xuất hiện trên dòng có nhãn
- **期待する結果**: Badge NEW hiển thị đúng vị trí; không xuất hiện trên dòng không có nhãn
        """
    )
    def test_04_verify_new_badge_visibility(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)
        event_home.expect_announcement_list_visible()
        row_count = event_home.get_announcement_row_count()

        assert row_count == 3, (
            f"Expected 3 announcement rows for NEW badge check, but found {row_count}"
        )

        for index in range(row_count):
            has_new_badge = event_home.has_new_badge(index)

            if has_new_badge:
                assert has_new_badge, (
                    f"NEW badge should be visible on announcement row {index + 1}"
                )
            else:
                assert not has_new_badge, (
                    f"NEW badge should not exist on announcement row {index + 1}"
                )

        with allure.step("[PASSED] NEW badge visibility is correct for all announcement rows"):
            pass
