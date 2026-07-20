import re
import random
import string
import time
from collections.abc import Callable
from typing import Optional

import allure
from playwright.sync_api import Page, expect
from constants.locators import DatePickerLocators as dp


class BasePage:
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

    @staticmethod
    def input_by_label(label: str) -> str:
        # ラベルテキスト（span/h4）に紐づく入力フィールド
        return f"""
        //*[self::span or self::h4]
        [normalize-space()='{label}']
        /following-sibling::div//input
        """

    @staticmethod
    def checkbox_by_label(label: str) -> str:
        # ラベルテキストに紐づくチェックボックス
        return f"""
        //label[normalize-space()='{label}']
        /preceding-sibling::div
        //input[@type='checkbox']
        """

    @staticmethod
    def combobox_by_label(label: str) -> str:
        # ラベルテキスト（span）に紐づくコンボボックス
        return f"""
        //span[normalize-space()='{label}']
        /following-sibling::div
        //*[@role='combobox']
        """

    @staticmethod
    def button_by_text(text: str) -> str:
        # テキストで特定するボタン
        return f"""
        //button[normalize-space()='{text}']
        """
    
    @allure.step("Click button with text '{text}'")
    def click_button_by_text(self, text: str) -> None:
        self.page.locator(self.button_by_text(text)).click()
        
    @staticmethod
    def link_by_text(text: str) -> str:
        # テキストで特定するリンク
        return f"""
        //a[normalize-space()='{text}']
        """

    @allure.step("Click link with text '{text}'")
    def click_link_by_text(self, text: str) -> None:
        self.page.locator(self.link_by_text(text)).click()
    

    @staticmethod
    def input_in_section(section_label: str, field_label: str) -> str:
        # セクションラベル内にあるフィールドラベルに紐づく入力フィールド
        return f"""
        //*[self::span or self::h4][normalize-space()='{section_label}']
        /ancestor::*[
            .//*[self::span or self::h4][normalize-space()='{field_label}']
        ][1]
        //*[self::span or self::h4][normalize-space()='{field_label}']
        /following-sibling::div//input
        """
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

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def is_text_visible(self, text: str) -> bool:
        return self.page.get_by_text(text).first.is_visible()

    def text_count(self, text: str) -> int:
        return self.page.get_by_text(text).count()

    # -----------------------------------------------------------------------
    # Date picker — shared Vuetify calendar navigation
    # -----------------------------------------------------------------------

    def _fill_dialog_date_picker(self, trigger_locator, date_str: str) -> None:
        """Open a Vuetify date picker dialog and select date_str (YYYY/MM/DD).

        Three-step flow that matches the edit-page picker structure:
          1. Year  — JS scroll+click inside .v-date-picker-years
          2. Month — button text (Jan/Feb/...) inside .v-date-picker-table--month
          3. Day   — button text (1/2/...) inside .v-date-picker-table--date
                     (skipped automatically for month-type pickers that close after step 2)

        All interactions after opening are scoped to
        //div[@class='v-dialog v-dialog--active'] (exact class match), which uniquely
        identifies the date picker dialog inside the edit form overlay.
        """
        _MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        year_str, month_str, day_str = date_str.replace("/", "-").split("-")
        target_year, target_month, target_day = int(year_str), int(month_str), int(day_str)

        trigger_locator.click()

        modal = self.page.locator(dp.DIALOG).last
        modal.wait_for(state="visible", timeout=5000)

        # Navigate to year list view. Vuetify date picker may open in date view or month view,
        # requiring up to 2 header clicks to reach year list:
        #   date view → (click) → month view → (click) → year list view
        for _ in range(2):
            if modal.locator(dp.YEAR_LIST).count() > 0:
                break
            modal.locator(dp.HEADER_VALUE_BTN).first.click()
            self.page.wait_for_timeout(300)

        # Step 1: year — JS scroll+click (handles nested-dialog scroll containers)
        self.page.evaluate(
            f"""(year) => {{
                const items = Array.from(document.querySelectorAll('{dp.YEAR_ITEMS}'));
                const target = items.find(li => li.textContent.trim() === String(year));
                if (target) {{
                    target.scrollIntoView({{ block: 'center', behavior: 'instant' }});
                    target.click();
                }}
            }}""",
            target_year,
        )
        self.page.wait_for_timeout(300)

        # Step 2: month
        modal.locator(dp.MONTH_BUTTONS).filter(
            has_text=re.compile(
                rf"^\s*{_MONTH_LABELS[target_month - 1]}\s*$", re.IGNORECASE
            )
        ).first.click()
        self.page.wait_for_timeout(300)

        # Step 3: day (skipped for month-type pickers that close after step 2)
        date_table = modal.locator(dp.DATE_TABLE)
        if date_table.count() > 0 and date_table.first.is_visible():
            date_table.locator("button:not(.v-btn--disabled)").filter(
                has_text=re.compile(rf"^\s*{target_day}\s*$")
            ).first.click()

    def _open_and_fill_date_picker(self, trigger_locator, date_str: str) -> None:
        """Click trigger_locator to open a Vuetify v-date-picker, navigate to date_str (YYYY/MM/DD).

        Handles both date-type (day grid) and month-type (month grid) pickers.
        """
        _MONTH_ABBR = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                       "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        year_str, month_str, day_str = date_str.replace("/", "-").split("-")
        target_year, target_month, target_day = int(year_str), int(month_str), int(day_str)

        def _calendar_open() -> bool:
            return self.page.locator(".v-date-picker-header").first.is_visible()

        def _click_month_abbr():
            self.page.locator(dp.MONTH_BUTTONS).filter(
                has_text=re.compile(rf"^\s*{_MONTH_ABBR[target_month - 1]}\s*$", re.IGNORECASE)
            ).first.click()
            self.page.wait_for_timeout(300)

        trigger_locator.click()
        self.page.locator(dp.HEADER).first.wait_for(state="visible", timeout=5000)

        # Some pickers (e.g. edit-page dialog) open directly at year-list view;
        # skip the header-click loop in that case to avoid navigating away from it.
        used_year_picker = self.page.locator(dp.YEAR_LIST).count() > 0
        if not used_year_picker:
            for _ in range(2):
                self.page.locator(dp.HEADER_VALUE_BTN).first.click()
                self.page.wait_for_timeout(300)
                if self.page.locator(dp.YEAR_LIST).count() > 0:
                    used_year_picker = True
                    break

        if used_year_picker:
            # Use JS to scroll+click within the year list — Playwright's scroll_into_view_if_needed
            # scrolls the page/dialog viewport rather than the inner year-list scroll container,
            # so years far from the default (e.g. 2000 when list shows 1990) are never reached.
            self.page.evaluate(
                f"""(year) => {{
                    const items = Array.from(document.querySelectorAll('{dp.YEAR_ITEMS}'));
                    const target = items.find(li => li.textContent.trim() === String(year));
                    if (target) {{
                        target.scrollIntoView({{ block: 'center', behavior: 'instant' }});
                        target.click();
                    }}
                }}""",
                target_year,
            )
            self.page.wait_for_timeout(400)
            if self.page.locator(dp.MONTH_TABLE).count() > 0:
                _click_month_abbr()
                self.page.wait_for_timeout(500)
                if not _calendar_open():
                    return

        for _ in range(500):
            if not _calendar_open():
                return
            header_text = self.page.locator(dp.HEADER_VALUE).first.inner_text()
            m_dt = re.search(r"(\d{4})年(\d{1,2})", header_text)
            m_yr = re.search(r"\b(\d{4})\b", header_text) if not m_dt else None
            nav = self.page.locator(dp.HEADER + " button")
            if m_dt:
                cy, cm = int(m_dt.group(1)), int(m_dt.group(2))
                if cy == target_year and cm == target_month:
                    break
                (nav.last if (cy * 12 + cm) < (target_year * 12 + target_month)
                 else nav.first).click()
            elif m_yr:
                cy = int(m_yr.group(1))
                if cy == target_year:
                    break
                (nav.last if cy < target_year else nav.first).click()
            else:
                break
            self.page.wait_for_timeout(100)

        if not _calendar_open():
            return

        try:
            self.page.locator(dp.DATE_TABLE).first.wait_for(state="visible", timeout=2000)
        except Exception:
            pass

        if self.page.locator(dp.DATE_TABLE).first.is_visible():
            self.page.locator(dp.DATE_BUTTONS_ENABLED).filter(
                has_text=re.compile(rf"^\s*{target_day}\s*$")
            ).first.click()
            self.page.locator(dp.HEADER).first.wait_for(state="hidden", timeout=5000)
        elif self.page.locator(dp.MONTH_TABLE).first.is_visible():
            _click_month_abbr()
            self.page.locator(dp.HEADER).first.wait_for(state="hidden", timeout=3000)

    # -----------------------------------------------------------------------
    # Random data generators — reusable across test cases
    # -----------------------------------------------------------------------

    _SYMBOLS = "!@#$%"
    _PASSWORD_CHARSET = (
        string.ascii_lowercase + string.ascii_uppercase + string.digits + _SYMBOLS
    )

    @staticmethod
    def random_text_in_range(
        min_len: int,
        max_len: int,
        charset: str | None = None,
    ) -> str:
        """Random string with length chosen uniformly in [min_len, max_len]."""
        if min_len > max_len:
            raise ValueError(f"min_len ({min_len}) must be <= max_len ({max_len})")
        if min_len < 0:
            raise ValueError("min_len must be >= 0")
        length = random.randint(min_len, max_len)
        return BasePage.random_text(length, charset)

    @staticmethod
    def random_email_with_length(
        min_len: int = 1,
        max_len: int = 1000,
        domain: str = "@bravesoft.com.vn",
        prefix: str = "test",
        separator: str = "_",
    ) -> str:
        """Valid-format ASCII email with total length in [min_len, max_len].

        Total length = len(prefix) + len(separator) + len(random_suffix) + len(domain).
        The random part length is chosen so the full address stays within the bounds.
        """
        if min_len > max_len:
            raise ValueError(f"min_len ({min_len}) must be <= max_len ({max_len})")

        fixed_local = f"{prefix}{separator}"
        overhead = len(fixed_local) + len(domain)
        if max_len < overhead:
            raise ValueError(
                f"max_len ({max_len}) is too small for prefix '{prefix}', "
                f"separator '{separator}', and domain '{domain}' (need at least {overhead})"
            )

        suffix_min = max(0, min_len - overhead)
        suffix_max = max_len - overhead
        if suffix_max < suffix_min:
            raise ValueError(
                f"Cannot fit email in [{min_len}, {max_len}] with prefix '{prefix}', "
                f"separator '{separator}', domain '{domain}'"
            )

        pool = string.ascii_lowercase + string.digits
        suffix_len = random.randint(suffix_min, suffix_max)
        suffix = "".join(random.choices(pool, k=suffix_len))
        email = f"{fixed_local}{suffix}{domain}"
        assert min_len <= len(email) <= max_len, (
            f"Generated email length {len(email)} outside [{min_len}, {max_len}]"
        )
        return email

    @staticmethod
    def random_email_over_length(
        max_len: int = 1000,
        over_by: int = 1,
        domain: str = "@bravesoft.com.vn",
    ) -> str:
        """Email longer than max_len (default: 1001 chars when max_len=1000)."""
        target = max_len + over_by
        local_len = max(1, target - len(domain))
        local = BasePage.random_text(local_len, string.ascii_lowercase)
        return f"{local}{domain}"

    @staticmethod
    def random_email(prefix: str = "test") -> str:
        """Random valid ASCII email, well under 1000 chars.
        Pattern: {prefix}_<10 alphanum>@bravesoft.com.vn
        """
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{prefix}_{suffix}@bravesoft.com.vn"

    @staticmethod
    def random_password(min_len: int = 12, max_len: int = 20) -> str:
        """Random password: ASCII letters + digits + symbols (min_len–max_len).
        Guarantees at least one lowercase, uppercase, digit, and symbol when min_len >= 4.
        """
        if min_len > max_len:
            raise ValueError(f"min_len ({min_len}) must be <= max_len ({max_len})")
        pool = BasePage._PASSWORD_CHARSET
        required = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(BasePage._SYMBOLS),
        ]
        if min_len < 4:
            return BasePage.random_text_in_range(min_len, max_len, pool)
        rest = random.choices(pool, k=random.randint(max(0, min_len - 4), max_len - 4))
        chars = required + rest
        random.shuffle(chars)
        return "".join(chars)

    @staticmethod
    def random_text(length: int = 10, charset: str | None = None) -> str:
        """Random string of given length (default charset: ASCII letters)."""
        pool = charset if charset is not None else string.ascii_letters
        return "".join(random.choices(pool, k=length))

    @staticmethod
    def random_phone() -> str:
        """Random Japanese mobile number: 090XXXXXXXX (11 digits)."""
        return "090" + "".join(random.choices(string.digits, k=8))

    @staticmethod
    def random_data_input_field(
        length: int = 14,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        use_icon: bool = False,
        special_chars: Optional[str] = None,
    ) -> str:
        """Generate random data for input fields with configurable character types.

        Each enabled type contributes at least one character (when length allows).
        Falls back to random.choices for the remaining positions.
        """
        pool = ""
        types: list[str] = []

        if use_uppercase:
            pool += string.ascii_uppercase
            types.append(string.ascii_uppercase)
        if use_lowercase:
            pool += string.ascii_lowercase
            types.append(string.ascii_lowercase)
        if use_digits:
            pool += string.digits
            types.append(string.digits)
        if use_special:
            sp = special_chars if special_chars is not None else string.punctuation
            pool += sp
            types.append(sp)
        if use_icon:
            pool += "😀"
            types.append("😀")

        if not pool:
            raise ValueError("At least one character type must be selected.")

        result: list[str] = []
        if length >= len(types):
            result = [random.choice(t) for t in types]

        remaining = length - len(result)
        if remaining > 0:
            result += random.choices(pool, k=remaining)

        random.shuffle(result)
        generated = "".join(result[:length])
        with allure.step(f"Generate random {length}-char input field data: {generated}"):
            pass
        return generated

    @staticmethod
    def random_login_id(prefix: str = "test") -> str:
        """Random valid string-type login ID: prefix_<8 alphanum> (14 chars total, within 8–32).
        Allowed charset: half-width alpha/digit/symbol(_-.)
        """
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{prefix}_{suffix}"

    @staticmethod
    def add_random_chars(text: str, n: int = 1, charset: str | None = None) -> str:
        """Append n random chars — for over-limit boundary tests."""
        pool = charset if charset is not None else string.ascii_lowercase + string.digits
        return text + "".join(random.choices(pool, k=n))

    @staticmethod
    def remove_random_chars(text: str, n: int = 1) -> str:
        """Remove n randomly chosen chars — for under-limit boundary tests."""
        if n >= len(text):
            return ""
        indices = sorted(random.sample(range(len(text)), n), reverse=True)
        chars = list(text)
        for i in indices:
            chars.pop(i)
        return "".join(chars)

    # -----------------------------------------------------------------------
    # XPath builders — reusable locator helpers for common UI patterns
    # -----------------------------------------------------------------------

