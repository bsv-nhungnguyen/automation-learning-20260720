import time
from collections.abc import Callable

import allure
from playwright.sync_api import Page, expect


class BasePage:
    """Base cho moi Page Object — chi giu cac ham dung chung can thiet.

    Moi team tu them helper rieng cua man hinh minh vao Page Object cua team,
    chi day len day khi that su dung chung >= 2 man hinh.
    """

    def __init__(self, page: Page):
        self.page = page

    def wait_until(
        self,
        condition: Callable[[], bool],
        *,
        timeout_ms: int = 10000,
        poll_interval_ms: int = 200,
        message: str = "Condition was not met before timeout",
    ) -> None:
        """Poll until condition() is True (compatible with Playwright versions without expect.poll)."""
        deadline = time.monotonic() + timeout_ms / 1000
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                if condition():
                    return
            except Exception as exc:
                last_error = exc
            self.page.wait_for_timeout(poll_interval_ms)
        detail = f" ({last_error})" if last_error else ""
        raise AssertionError(f"{message}{detail}")

    # -----------------------------------------------------------------------
    # Navigation
    # -----------------------------------------------------------------------

    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    # -----------------------------------------------------------------------
    # Interaction
    # -----------------------------------------------------------------------

    @allure.step("Click element: {selector}")
    def click(self, selector: str):
        self.page.locator(selector).click()

    @allure.step("Fill '{selector}' with value")
    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    @allure.step("Click by role '{role}' with name '{name}'")
    def click_by_role(self, role: str, name: str):
        self.page.get_by_role(role, name=name).click()

    @allure.step("Fill placeholder '{placeholder}' with value")
    def fill_by_placeholder(self, placeholder: str, value: str):
        self.page.get_by_placeholder(placeholder).fill(value)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect element visible: {selector}")
    def expect_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()

    @allure.step("Expect element NOT visible: {selector}")
    def expect_not_visible(self, selector: str):
        expect(self.page.locator(selector)).not_to_be_visible()

    @allure.step("Expect element '{selector}' contains text '{text}'")
    def expect_text(self, selector: str, text: str):
        expect(self.page.locator(selector)).to_contain_text(text)

    @allure.step("Expect input '{placeholder}' is empty")
    def expect_empty_placeholder(self, placeholder: str):
        expect(self.page.get_by_placeholder(placeholder)).to_have_value("")


    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def is_text_visible(self, text: str) -> bool:
        return self.page.get_by_text(text).first.is_visible()

    def text_count(self, text: str) -> int:
        return self.page.get_by_text(text).count()
