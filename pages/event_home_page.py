import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class EventHomePage(BasePage):
    """ホーム画面 / Home screen."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.navigationTabs = "//a[@class='navigation__item__name']"

        self.eventTab = "//a[@href='./event_home.html']//div[text()='イベント']"
        self.portalTab = "//a[@href='./portal_home.html']//div[text()='ポータル']"
        self.memberTab = "//a[@href='./member_list.html']//div[text()='会員管理']"
        self.mailTab = "//a[@href='./push_list/mail-send.html']//div[text()='配信する']"
        self.reportTab = "//a[contains(@href,'./not_implemented.html')]//div[text()='レポート']"

    def get_navigation_tab_names(self):
        return self.page.locator(self.navigationTabs).all_inner_texts()

    def navigate_tabs_count(self):
        return self.page.locator(self.navigationTabs).count()

    def navigate_tab_render_correctly(self):
        tabs = [
            self.eventTab,
            self.portalTab,
            self.memberTab,
            self.mailTab,
            self.reportTab
        ]
        return all(self.page.locator(tab).is_visible() for tab in tabs)

    def is_tab_active(self, tab_name):
        active_class = self.page.locator(
            f"//a[@class='navigation__item__name']//div[text()='{tab_name}']"
        ).get_attribute("class")
        return active_class is not None and "active" in active_class

    

