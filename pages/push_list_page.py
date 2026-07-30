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
