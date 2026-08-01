import allure
from playwright.sync_api import Page, expect
from constants.locators import PushListLocators as locators
from pages.base_page import BasePage


class PushListPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Click delivery button")
    def click_delivery_button(self):
        self.click_by_text(locators.DELIVERY_BUTTON)

    @allure.step("Click delivery list")
    def click_delivery_list(self):
        self.page.locator(locators.DELIVERY_LIST).click()
    
    @allure.step("Open push notification create drawer")
    def open_create_drawer(self):
        self.click(locators.CREATE_BUTTON)
        expect(self.page.locator(locators.DRAWER)).to_be_visible()

    @allure.step("Select scheduled delivery")
    def select_scheduled_delivery(self):
        self.click_by_role("radio",locators.SCHEDULE_DELIVERY_RADIO)

    @allure.step("Click cancel button")
    def click_cancel(self):
        self.click_by_role("button",locators.CANCEL_BUTTON)

    @allure.step("Click close button")
    def click_close(self):
        self.click_by_role("button",locators.CLOSE_BUTTON)

    def fill_title(self, title: str):
        self.fill_by_placeholder(locators.TITLE_PLACEHOLDER, title)
      
    def fill_message(self, message: str):
        self.fill_by_placeholder(locators.MESSAGE_PLACEHOLDER, message)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Verify schedule area displayed")
    def verify_schedule_area_displayed(self):
        self.expect_visible(locators.SCHEDULE_AREA)

    @allure.step("Verify schedule date displayed")
    def verify_schedule_date_displayed(self):
        self.expect_visible(locators.SCHEDULE_DATE)

    @allure.step("Verify schedule time displayed")
    def verify_schedule_time_displayed(self):
        self.expect_visible(locators.SCHEDULE_TIME)

    @allure.step("Verify modal closed")
    def verify_modal_closed(self):
        self.expect_not_visible(locators.DRAWER)

    @allure.step("Verify title is cleared")
    def verify_title_cleared(self):
        self.expect_empty_placeholder(locators.TITLE_PLACEHOLDER)

    @allure.step("Verify message is cleared")
    def verify_message_cleared(self):
        self.expect_empty_placeholder(locators.MESSAGE_PLACEHOLDER)

    @allure.step("Navigate to push notification list screen")
    def navigate_to_push_list(self, app_url: str):
        self.navigate_to(f"{app_url}/push_list/push_list.html")

    