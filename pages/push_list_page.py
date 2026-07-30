import allure
from playwright.sync_api import Page

from constants.locators import PushListLocators
from pages.base_page import BasePage


class PushListPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------
    @allure.step("Click delivery button")
    def click_delivery_button(self):
        self.click_by_text(PushListLocators.DELIVERY_BUTTON)

    @allure.step("Click delivery list")
    def click_delivery_list(self):
        self.page.locator(PushListLocators.DELIVERY_LIST).click()
    
    @allure.step("Open create push modal")
    def open_create_push_modal(self):
        self.click_by_role("button",PushListLocators.CREATE_BUTTON,)

    @allure.step("Select scheduled delivery")
    def select_scheduled_delivery(self):
        self.click_by_role("radio",PushListLocators.SCHEDULE_DELIVERY_RADIO)

    @allure.step("Click cancel button")
    def click_cancel(self):
        self.click_by_role("button",PushListLocators.CANCEL_BUTTON)

    @allure.step("Click close button")
    def click_close(self):
        self.click_by_role("button",PushListLocators.CLOSE_BUTTON)

    @allure.step("Input title")
    def input_title(self, title: str):
        self.fill_by_placeholder(PushListLocators.TITLE_PLACEHOLDER,title)

    @allure.step("Input message")
    def input_message(self, message: str):
        self.fill_by_placeholder(PushListLocators.MESSAGE_PLACEHOLDER,message)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Verify schedule area displayed")
    def verify_schedule_area_displayed(self):
        self.expect_visible(PushListLocators.SCHEDULE_AREA)

    @allure.step("Verify schedule date displayed")
    def verify_schedule_date_displayed(self):
        self.expect_visible(PushListLocators.SCHEDULE_DATE)

    @allure.step("Verify schedule time displayed")
    def verify_schedule_time_displayed(self):
        self.expect_visible(PushListLocators.SCHEDULE_TIME)

    @allure.step("Verify modal closed")
    def verify_modal_closed(self):
        self.expect_not_visible(PushListLocators.MODAL)

    @allure.step("Verify title is cleared")
    def verify_title_cleared(self):
        self.expect_empty_placeholder(PushListLocators.TITLE_PLACEHOLDER)

    @allure.step("Verify message is cleared")
    def verify_message_cleared(self):
        self.expect_empty_placeholder(PushListLocators.MESSAGE_PLACEHOLDER)