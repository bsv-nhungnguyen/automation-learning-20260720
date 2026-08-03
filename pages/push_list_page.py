import allure
from playwright.sync_api import Page, expect

from constants.locators import PushListLocators as locators
from pages.base_page import BasePage


class PushListPage(BasePage):
    """プッシュ配信一覧画面 / プッシュ配信新規作成ドロワー."""

    def __init__(self, page: Page):
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Navigate to push notification list screen")
    def navigate_to_push_list(self, app_url: str):
        self.navigate_to(f"{app_url}/push_list/push_list.html")

    @allure.step("Open push notification create drawer")
    def open_create_drawer(self):
        self.click(locators.CREATE_BUTTON)
        expect(self.page.locator(locators.DRAWER)).to_be_visible()

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

    @allure.step("Expect 配信タイプ defaults to 即時配信する")
    def expect_send_type_defaults_to_immediate(self):
        expect(
            self.page.get_by_role("radio", name=locators.SEND_IMMEDIATE_RADIO_LABEL)
        ).to_be_checked()

    # -----------------------------------------------------------------------
    # Actions — bổ sung cho TC03-04
    # -----------------------------------------------------------------------

    def submit_button(self):
        return self.page.locator(locators.SUBMIT_BUTTON)

    def fill_title(self, title: str):
        self.fill_by_placeholder(locators.TITLE_PLACEHOLDER, title)

    def select_segment_rule(self, option_label: str):
        self.page.locator(locators.SEGMENT_SELECT).select_option(label=option_label)

    def fill_message(self, message: str):
        self.fill_by_placeholder(locators.MESSAGE_PLACEHOLDER, message)

    def fill_required_fields(self, title: str, segment_rule_label: str, message: str):
        self.fill_title(title)
        self.select_segment_rule(segment_rule_label)
        self.fill_message(message)

    # -----------------------------------------------------------------------
    # Assertions — bổ sung cho TC03-04
    # -----------------------------------------------------------------------

    @allure.step("Expect submit button disabled")
    def expect_submit_button_disabled(self):
        expect(self.submit_button()).to_be_disabled()

    @allure.step("Expect submit button enabled")
    def expect_submit_button_enabled(self):
        expect(self.submit_button()).to_be_enabled()
        
    # -----------------------------------------------------------------------
    # Actions — Bổ sung cho TC05-06
    # -----------------------------------------------------------------------

    @allure.step("Select CSV upload")
    def select_csv_upload(self):
        self.page.get_by_role(
            "radio",
            name=locators.CSV_UPLOAD_RADIO
        ).click()

    @allure.step("Input title")
    def input_title(self, title: str):
        self.fill_by_placeholder(
            locators.TITLE_PLACEHOLDER,
            title
        )

    # -----------------------------------------------------------------------
    # Assertions — Bổ sung cho TC05-06
    # -----------------------------------------------------------------------

    @allure.step("Verify segment area hidden")
    def verify_segment_area_hidden(self):
        expect(
            self.page.locator(locators.SEGMENT_AREA)
        ).not_to_be_visible()

    @allure.step("Verify CSV area displayed")
    def verify_csv_area_displayed(self):
        expect(
            self.page.locator(locators.CSV_AREA)
        ).to_be_visible()

    @allure.step("Verify title maxlength is 255")
    def verify_title_maxlength(self):
        value = self.page.locator(
            locators.TITLE_INPUT
        ).input_value()

        assert len(value) == 255
        

