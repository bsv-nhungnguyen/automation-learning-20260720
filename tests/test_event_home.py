import allure
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

    @allure.title("Verify section title is displayed")
    def test_02_verify_widgets_are_displayed(self, access_to_home_screen: Page):
        event_home_page = EventHomePage(access_to_home_screen)
        # Verify section title is displayed
        assert event_home_page.is_section_title_displayed(
            EventHomeLocators.SECTION_STATISTICS_TITLE) is True
        # Verify usage widget labels are displayed
        assert event_home_page.get_usage_widget_label(
            EventHomeLocators.DAU_LABEL) is True
        assert event_home_page.get_usage_widget_label(
            EventHomeLocators.MEMBER_LABEL) is True
        # Verify tooltip content is displayed
        assert event_home_page.is_tooltip_content_visible(
            EventHomeLocators.DAU_LABEL,
            EventHomeLocators.DAU_TOOLTIP_CONTENT,
        ) is True
        assert event_home_page.is_tooltip_content_visible(
            EventHomeLocators.MEMBER_LABEL,
            EventHomeLocators.MEMBER_TAB_TOOLTIP_CONTENT,
        ) is True
        allure.attach(
            access_to_home_screen.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )