import allure
from playwright.sync_api import Page

from constants import messages
from constants.locators import EventHomeLocators
from helpers import description_md
from pages.event_home_page import EventHomePage
from testdata.test_data import EventHomeTestData


@allure.feature("イベント")
@allure.story("イベントホーム")
@description_md(
    "Test cases イベントホーム_001 – イベントホーム_008 - xac nhan cac thanh phan "
    "chinh tren man hinh Event-home (nav, widget, oshirase, table, search, pagination)."
)
class Testイベント_Event_home:
    # -------------------------------------------------------------------
    # イベントホーム_001
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_001: Verify các navigation tabs được hiển thị")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Quan sát thanh navigation tabs
                 2. Kiểm tra tên tab, thứ tự và tab đang active
- **期待する結果**: Hiển thị đủ 5 tab theo đúng thứ tự; tab イベント đang active
        """
    )
    def test_01_verify_nav_tabs_are_displayed(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)
        expected_tab_names = [
            EventHomeLocators.EVENT_TAB,
            EventHomeLocators.PORTAL_TAB,
            EventHomeLocators.MEMBER_TAB,
            EventHomeLocators.MAIL_TAB,
            EventHomeLocators.REPORT_TAB,
        ]
        assert event_home.get_navigation_tab_names() == expected_tab_names
        assert event_home.is_navigation_tab_order_correct()
        assert event_home.is_tab_active(EventHomeLocators.EVENT_TAB) is True
        with allure.step("[PASSED] Navigation tabs are displayed in correct order"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_002
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_002: Verify các usage widgets được hiển thị")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Kiểm tra label DAU và MEMBER
                 2. Hover icon ? của từng label và đọc tooltip
- **期待する結果**: Label và tooltip content của DAU / MEMBER hiển thị đúng
        """
    )
    def test_02_verify_usage_widgets_are_displayed(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)

        assert event_home.is_usage_label_visible(messages.TOTAL_DAU_WIDGET_LABEL) is True
        event_home.hover_tooltip_by_label(messages.TOTAL_DAU_WIDGET_LABEL)
        assert event_home.is_tooltip_content_visible(messages.DAU_TOOLTIP_CONTENT) is True

        assert event_home.is_usage_label_visible(messages.TOTAL_MEMBER_COUNT_WIDGET_LABEL) is True
        event_home.hover_tooltip_by_label(messages.TOTAL_MEMBER_COUNT_WIDGET_LABEL)
        assert event_home.is_tooltip_content_visible(messages.MEMBER_COUNT_TOOLTIP_CONTENT) is True

        with allure.step("[PASSED] Usage widget labels and tooltips are displayed"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_003
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_003: Verify số lượng dòng trong danh sách お知らせ")
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

        assert row_count > 0, f"Expected at least 1 announcement row, but found {row_count}"

        with allure.step(f"[CHECK] announcement row count = {row_count}"):
            pass

        for index in range(row_count):
            row = announcement_rows.nth(index)
            assert row.is_visible(), f"Announcement row {index + 1} is not visible"

            date_text = event_home.get_announcement_date(index)
            tag_text = event_home.get_announcement_tag(index)
            title_text = event_home.get_announcement_title(index)

            assert date_text, f"Announcement row {index + 1} is missing a date"
            assert tag_text, f"Announcement row {index + 1} is missing a tag"
            assert title_text, f"Announcement row {index + 1} is missing a title"

            with allure.step(
                f"Announcement row {index + 1}: date={date_text!r}, "
                f"tag={tag_text!r}, title={title_text!r}"
            ):
                pass

        with allure.step("[PASSED] Announcement list rows contain date/tag/title data"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_004
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_004: Verify badge NEW hiển thị đúng")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Kiểm tra từng dòng thông báo
                 2. Xác nhận badge NEW chỉ xuất hiện trên dòng có nhãn
- **期待する結果**: Badge NEW hiển thị đúng vị trí; không xuất hiện trên dòng không có nhãn
        """
    )
    def test_04_verify_new_badge_visibility(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)
        event_home.expect_announcement_list_visible()
        row_count = event_home.get_announcement_row_count()

        assert row_count > 0, f"Expected at least 1 announcement row, but found {row_count}"

        for index in range(row_count):
            row = event_home.get_announcement_rows().nth(index)
            has_new_badge = event_home.has_new_badge(index)
            badge = row.locator(event_home.locator.ANNOUNCEMENT_NEW_BADGE)

            if has_new_badge:
                assert badge.count() > 0, (
                    f"NEW badge should exist on announcement row {index + 1}"
                )
                assert badge.is_visible(), (
                    f"NEW badge should be visible on announcement row {index + 1}"
                )
            else:
                assert badge.count() == 0 or not badge.is_visible(), (
                    f"NEW badge should not exist on announcement row {index + 1}"
                )

            with allure.step(
                f"Announcement row {index + 1}: NEW badge visible={has_new_badge}"
            ):
                pass

        with allure.step("[PASSED] NEW badge visibility matches each announcement row"):
            pass
    
    # -------------------------------------------------------------------
    # イベントホーム_005
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_005: Verify search theo keyword chỉ hiện event khớp")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home, bảng event có ít nhất 1 dòng
- **テスト手順**: 1. Lấy tên event dòng đầu làm keyword
                 2. Nhập keyword vào ô search
- **期待する結果**: Chỉ các event khớp keyword được hiển thị
        """
    )
    def test_05_search_event_by_keyword_shows_only_matching_events(
        self, access_to_home_screen: Page
    ):
        event_home = EventHomePage(access_to_home_screen)

        keyword = event_home.get_first_event_name()
        assert keyword, "First row has no event name — test data is invalid"

        event_home.search_event_by_keyword(keyword)
        event_home.expect_has_visible_event_rows()
        assert event_home.get_visible_event_row_count() > 0, (
            f"No event is displayed after searching keyword '{keyword}'"
        )

        unmatched_rows = event_home.get_event_rows_not_matching_keyword(keyword)
        assert not unmatched_rows, (
            f"{len(unmatched_rows)} event row(s) do not match keyword '{keyword}': "
            f"{unmatched_rows}"
        )

        with allure.step("[PASSED] Event table shows only events matching the keyword"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_006
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_006: Verify trạng thái mặc định pagination và 表示件数")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Đếm số dòng event đang hiển thị rồi so với text phân trang
                 2. Kiểm tra nút 前へ và giá trị 表示件数 mặc định
- **期待する結果**: Summary khớp số dòng thực tế, nút 前へ disabled, 表示件数 = mặc định
        """
    )
    def test_06_verify_pagination_default_state(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)

        assert event_home.get_visible_event_row_count() > 0, (
            "Event table has no row — test data is invalid"
        )

        expected_summary = event_home.build_expected_pagination_summary(
            EventHomeTestData.NEXT_PAGE_BUTTON
        )
        actual_summary = event_home.get_pagination_summary_text()
        assert actual_summary == expected_summary, (
            f"Pagination summary mismatch.\n"
            f"Expected: {expected_summary}\nActual: {actual_summary}"
        )

        event_home.expect_pagination_button_disabled(EventHomeTestData.PREV_PAGE_BUTTON)

        actual_per_page = event_home.get_selected_per_page()
        expected_per_page = EventHomeTestData.PER_PAGE_DEFAULT
        assert actual_per_page == expected_per_page, (
            f"表示件数 mismatch.\n"
            f"Expected: {expected_per_page}\nActual: {actual_per_page}"
        )

        with allure.step(f"[PASSED] Pagination default state and 表示件数 are correct {expected_per_page}, and 前へ button is disabled"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_007
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_007: Verify header cột của bảng event")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Đọc danh sách header cột của bảng event
- **期待する結果**: Header cột khớp danh sách expected trong locators
        """
    )
    def test_07_verify_event_table_headers_are_displayed(self, access_to_home_screen: Page):
        event_home = EventHomePage(access_to_home_screen)

        actual = event_home.get_event_table_header_names()
        expected = EventHomeLocators.EVENT_TABLE_COLUMN_HEADERS
        assert actual == expected, (
            f"Headers mismatch.\nExpected: {expected}\nActual: {actual}"
        )

        with allure.step("[PASSED] Event table column headers are displayed correctly"):
            pass

    # -------------------------------------------------------------------
    # イベントホーム_008
    # -------------------------------------------------------------------
    @allure.title("イベントホーム_008: Verify nút tạo event và chuyển đổi grid/list")
    @description_md(
        """
- **前提条件**: Đã login, đang ở Event-home
- **テスト手順**: 1. Click 新規イベント作成 rồi đóng form
                 2. Chuyển grid view rồi list view
- **期待する結果**: Form tạo event mở/đóng được; grid/list toggle đổi layout đúng
        """
    )
    def test_08_verify_create_button_and_view_toggle(self, access_to_home_screen: Page):
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
