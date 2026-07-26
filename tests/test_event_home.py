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