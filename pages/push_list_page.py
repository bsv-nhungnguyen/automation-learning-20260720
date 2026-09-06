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

    @allure.step("Open push notification create drawer")
    def open_create_drawer(self):
        self.click(locators.CREATE_BUTTON)
        expect(self.page.locator(locators.DRAWER)).to_be_visible()

    @allure.step("Navigate to push notification list screen")
    def navigate_to_push_list(self, app_url: str) -> None:
        self.page.goto(f"{app_url.rstrip('/')}/push_list/push_list.html")
        self.page.wait_for_load_state("networkidle")

    def submit_button(self):
        return self.page.locator(locators.SUBMIT_BUTTON)

    def fill_title(self, title: str):
        self.fill_by_placeholder(locators.TITLE_PLACEHOLDER, title)

    def select_segment_rule(self):
        option_value = self.page.locator(locators.SEGMENT_FIRST_OPTION).get_attribute("value")
        self.page.locator(locators.SEGMENT_SELECT).select_option(value=option_value)

    def fill_message(self, message: str):
        self.fill_by_placeholder(locators.MESSAGE_PLACEHOLDER, message)

    def fill_required_fields(self, title: str, message: str):
        self.fill_title(title)
        self.select_segment_rule()
        self.fill_message(message)

    @allure.step("Select CSV upload")
    def select_csv_upload(self, radio_label: str):
        self.page.get_by_role(
            "radio",
            name=radio_label,
        ).click()

    @allure.step("Select scheduled delivery")
    def select_scheduled_delivery(self):
        self.click_by_role("radio", locators.SCHEDULE_DELIVERY_RADIO)

    @allure.step("Click cancel button")
    def click_cancel(self):
        self.click_by_role("button", locators.CANCEL_BUTTON)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect required mark visible next to 配信管理用タイトル")
    def expect_title_required_mark_visible(self):
        expect(self.page.locator(locators.TITLE_REQUIRED_MARK)).to_be_visible()

    @allure.step("Expect required mark visible next to セグメントルールを選択する")
    def expect_segment_required_mark_visible(self):
        expect(self.page.locator(locators.SEGMENT_REQUIRED_MARK)).to_be_visible()

    @allure.step("Expect required mark visible next to メッセージ")
    def expect_message_required_mark_visible(self):
        expect(self.page.locator(locators.MESSAGE_REQUIRED_MARK)).to_be_visible()

    @allure.step("Expect 配信する対象の作成方法 defaults to セグメントルールから選ぶ")
    def expect_target_method_defaults_to_segment(self):
        expect(
            self.page.get_by_role("radio", name=locators.TARGET_SEGMENT_RADIO_LABEL)
        ).to_be_checked()
        
    @allure.step("Expect segment area hidden")
    def verify_segment_area_hidden(self):
        expect(
            self.page.locator(locators.SEGMENT_AREA)
        ).not_to_be_visible()


    @allure.step("Expect CSV upload area displayed")
    def verify_csv_area_displayed(self):
        expect(
            self.page.locator(locators.CSV_AREA)
        ).to_be_visible()


    @allure.step("Expect 配信管理用タイトル maximum length to be 255 characters")
    def verify_title_maxlength(self):
        value = self.page.locator(
            locators.TITLE_INPUT
        ).input_value()

        assert len(value) == 255

    @allure.step("Expect 配信タイプ defaults to 即時配信する")
    def expect_send_type_defaults_to_immediate(self):
        expect(
            self.page.get_by_role("radio", name=locators.SEND_IMMEDIATE_RADIO_LABEL)
        ).to_be_checked()

    @allure.step("Expect submit button disabled")
    def expect_submit_button_disabled(self):
        expect(self.submit_button()).to_be_disabled()

    @allure.step("Expect submit button enabled")
    def expect_submit_button_enabled(self):
        expect(self.submit_button()).to_be_enabled()

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
