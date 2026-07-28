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

    @allure.title("TC05: Search event by keyword shows only matching events")
    @description_md(
        """
- **前提条件**: ホーム画面のイベント一覧を表示中（イベントが1件以上存在すること）
- **テスト手順**:
  1. イベント一覧の1行目の「イベント名」を取得する
  2. 「キーワードを入力」欄に取得したイベント名を入力する
  3. Enterキーを押下する
- **期待する結果**: 検索結果が1件以上表示され、表示されるイベントはすべてキーワードに一致すること
        """
    )
    def test_05_search_event_by_keyword_shows_only_matching_events(
        self, access_to_home_screen: Page
    ):
        event_home_page = EventHomePage(access_to_home_screen)

        keyword = event_home_page.get_first_event_name()
        assert keyword, "First row has no event name — test data is invalid"

        event_home_page.search_event_by_keyword(keyword)

        event_home_page.expect_has_visible_event_rows()
        visible_rows = event_home_page.get_visible_event_row_texts()
        assert visible_rows, f"No event is displayed after searching keyword '{keyword}'"
        for row in visible_rows:
            assert keyword.lower() in row.lower(), (
                f"Event row does not match keyword '{keyword}': {row!r}"
            )

        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        with allure.step("[PASSED] Event table shows only events matching the keyword"):
            pass

    @allure.title("TC06: Verify pagination default state and 表示件数")
    def test_06_verify_pagination_default_state(self, access_to_home_screen: Page):
        event_home_page = EventHomePage(access_to_home_screen)

        assert (
            event_home_page.get_pagination_summary_text()
            == EventHomeLocators.PAGINATION_SUMMARY_TEXT
        )
        event_home_page.expect_pagination_button_disabled(EventHomeLocators.PREV_PAGE_BUTTON)
        assert event_home_page.get_selected_per_page() == EventHomeLocators.PER_PAGE_DEFAULT

        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        with allure.step("[PASSED] Pagination default state and 表示件数 are correct"):
            pass