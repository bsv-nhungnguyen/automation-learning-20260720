import random
import time
from collections.abc import Callable

import allure
from playwright.sync_api import Page, expect


class BasePage:
    """Base cho moi Page Object — chi giu cac ham dung chung can thiet.

    Moi team tu them helper rieng cua man hinh minh vao Page Object cua team,
    chi day len day khi that su dung chung >= 2 man hinh.
    """

    def __init__(self, page: Page) -> None:
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
    def navigate_to(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    # -----------------------------------------------------------------------
    # Interaction
    # -----------------------------------------------------------------------

    @allure.step("Click element: {selector}")
    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    @allure.step("Fill '{selector}' with value")
    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    @allure.step("Click by role '{role}' with name '{name}'")
    def click_by_role(self, role: str, name: str) -> None:
        self.page.get_by_role(role, name=name).click()

    @allure.step("Fill placeholder '{placeholder}' with value")
    def fill_by_placeholder(self, placeholder: str, value: str) -> None:
        self.page.get_by_placeholder(placeholder).fill(value)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect element visible: {selector}")
    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    @allure.step("Expect element NOT visible: {selector}")
    def expect_not_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).not_to_be_visible()

    @allure.step("Expect element '{selector}' contains text '{text}'")
    def expect_text(self, selector: str, text: str) -> None:
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
    
    @allure.step(
    "Generate random input data with Japanese, Vietnamese and spaces "
    "(total length={length})"
)
    def random_data_input_field_with_prefix(
        self,
        length: int = 25,
    ) -> str:
        prefix = "Automationtest"

        japanese_chars = "自動化テストあいうえおかきくけこ"
        vietnamese_chars = "Cổng thông tin tự động hóa đê"
        characters = japanese_chars + vietnamese_chars

        remaining_length = length - len(prefix)

        if remaining_length <= 0:
            return prefix[:length]

        random_part = "".join(
            random.choice(characters)
            for _ in range(remaining_length - 2)
        )

        random_part = random_part + " " + random.choice(japanese_chars)
        random_part = random_part + " " + random.choice(vietnamese_chars)

        return (prefix + random_part)[:length]
