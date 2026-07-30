# Automation Rules

## Project Structure

```text
project-root/
├── pages/             # Page Object Models — locators and actions
├── helpers/           # Shared utilities (e.g. description_md)
├── tests/             # Test files grouped by feature area
├── constants/         # Text, error messages, and UI constants
├── conftest.py        # Pytest fixtures (setup / teardown)
├── pytest.ini         # Pytest execution config
└── .env               # Environment variables (URL, credentials)
```

When creating a **new test file**, copy `my_skill/assets/template_testcase.py` under `tests/<area>/`,
replace all placeholders, and follow the inline comments.

---

## Coding Conventions

- Python 3.11+; type hints on all public methods.
- One class per file; file name matches class name in snake_case.
- Constants defined at module level in UPPER_CASE.
- No bare `except:` — catch specific exceptions or use `except Exception`.
- Remove unused imports; keep imports sorted (stdlib → third-party → local).
- No duplicate logic — extract helper methods when an action is repeated across tests or POM methods.
- Never hardcode credentials in tests, page objects, scripts, or documentation; read them from `.env`.

---

## Locator Strategy (priority order)

1. `get_by_role` — semantic and resilient (e.g., `get_by_role("button", name="ログイン")`).
2. `get_by_placeholder` — for input fields with visible placeholder text.
3. `get_by_text` / `filter(has_text=...)` — for visible text labels.
4. `get_by_label` — when a `<label>` is explicitly associated.
5. CSS attribute selectors (`input[type="email"]`) — only when no user-facing locator works.
6. XPath — last resort; document the reason in a comment.

For **existing POM files**, follow the local locator style first to maintain consistency.

**Never** use auto-generated IDs or positional indexes like `nth(0)` unless the element is
genuinely dynamic and no stable alternative exists.

**Scope searches to avoid false matches.** `get_by_text("会員ID")` may match hidden tooltip
elements before the visible `<th>`. Prefer `locator("th").filter(has_text=...)` for table column
checks, or use page-object helpers like `is_column_header_visible()` that already scope correctly.

**Locators live in `constants/locators.py`, not inside page classes.** Every page class
must have a corresponding locator class in `constants/locators.py` and import it as `locators`:

```python
# constants/locators.py
class AccountLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"  # メールアドレス入力欄
    LOGIN_BUTTON      = "#login_button"   # ログインボタン

# pages/account_page.py
from constants.locators import AccountLocators as locators

class AccountPage(BasePage):
    def login(self, ...):
        self.fill(locators.EMAIL_PLACEHOLDER, email)
```

Each locator entry must have a short Japanese comment describing the UI element it targets.

### Locator Discovery Process

Before adding a new locator to a POM, verify it against the running app:

1. **Navigate to the target screen** — use existing fixtures or `.env` credentials; do not
   hardcode credentials anywhere.
2. **Verify uniqueness** — call `locator.count()` and confirm exactly one element is matched.
3. **Confirm visibility/state** — ensure the element is visible and enabled when the test needs it.
4. **Scope DOM inspection** — capture only the relevant container around the target; never dump
   or commit full-page HTML.
5. **Avoid `.first` as a workaround** — use `.first` only when the UI intentionally has repeated
   elements and the test clearly targets the first one. Document the reason with a short comment.

---

## Naming Conventions

| Artifact | Pattern | Example |
|---|---|---|
| Test method | `test_<subject>_<condition>_<expected>` | `test_member_list_member_id_column_is_displayed_correctly` |
| `@allure.title` | `<area>_<NNN>: <short English description>` | `"会員リスト_001: Navigate to 会員管理 shows the 会員リスト screen"` |
| Test ID in title | `<sheet_tab>_<zero-padded-3-digit-number>` | `会員リスト_001`, `会員リスト_010` |
| Fixture | snake_case noun phrase | `member_list`, `access_to_login_screen` |
| Test class | `Test` + Japanese sheet name using `_` | `Test会員管理_会員リスト` |
| Page class | PascalCase + `Page` suffix | `MemberListPage` |
| Constant | SCREAMING_SNAKE_CASE | `REQUIRED_COLUMNS` |
| Assertion message | Short English string starting with subject | `"Column 'X' is not visible"` |

**Zero-pad test IDs to 3 digits** in `@allure.title` so Allure's text sort matches the spec
sequence (e.g. `052`, `100`, not `52`, `100`).

---

## `@description_md` Rule

Every test **method** and test **class** must carry a `@description_md(...)` decorator.
Import it from `helpers`:

```python
from helpers import description_md
```

`description_md` wraps `allure.description(textwrap.dedent(text))` — content lines may be
indented in source for readability; Allure receives cleanly dedented markdown. Do **not** use
raw `@allure.description(...)` in individual test files.

### Class-level — links the file to the spec sheet

```python
@description_md(
    "Test cases 会員リスト_001 – 会員リスト_010 in file "
    "（主催者コンソール）セキュリティバージョンアップ_項目書 — シート: 会員リスト"
)
class TestMemberList:
    ...
```

### Method-level — one block per test, sourced from the CSV spec

The three fields map directly to the CSV columns:

| `@description_md` field | CSV column |
|---|---|
| `前提条件` | 前提条件 (column D) |
| `テスト手順` | 手順 (column E) |
| `期待する結果` | 期待結果 (column F) |

**Required format** (markdown bullet list):

```python
@description_md(
    """
- **前提条件**: 〇〇画面を表示中
- **テスト手順**: 1. 〇〇を押下する
- **期待する結果**: 〇〇が表示されること
    """
)
def test_example(self, fixture):
    ...
```

Multi-line steps or results use indented sub-bullets:

```python
@description_md(
    """
- **前提条件**: 会員リスト画面を表示中
- **テスト手順**: 1. ログインIDを確認する
- **期待する結果**:
  - 文字列型（英数字）の場合、ログインIDが正しく表示されること
  - メールアドレス形の場合、メールアドレスが正しく表示されること
    """
)
```

---

## Test Design Principles

- **Independence** — every test must be runnable alone; no shared mutable state.
- **Single assertion focus** — each test validates one specific expectation.
- **Fast setup** — fixtures use direct URL navigation where possible; avoid multi-step UI navigation in setup.
- **No hard sleeps** — use `wait_for_load_state("networkidle")` or explicit Playwright waits.
- **Screenshot + video evidence** — conftest captures a screenshot (pass + fail) and video (fail only) via Allure.
- **Header + body data** — tests that verify a column must check both the column header (`<th>`) AND that body cells contain the expected data. Columns where blank values are valid (e.g. 管理用メモ, 外部連携用ユーザーID, プロモーションコード) only need the header check.
- **No `@allure.severity`** — do not add `@allure.severity` decorators; severity is not used in this project.

### Mandatory `[PASSED]` ending step

Every non-skipped test function must end with:

```python
with allure.step("[PASSED] <short summary>"):
    pass
```

### Incomplete spec → explicit skip

When the spec does not provide enough information to implement a test reliably, create the
function, mark it skipped immediately, and do **not** guess behavior:

```python
@allure.title("会員リスト_062: ...")
def test_xxx(self, fixture):
    pytest.skip(
        "Spec incomplete for 会員リスト_062: insufficient information about "
        "<unclear part> to implement automation safely"
    )
```

The skip reason must name the testcase ID and describe which part is unclear.

### Assertion strictness

- Assert the **exact wording** from the spec (placeholder text, URL hint, error copy).
- Do **not** widen assertions with `or` to accept alternate spellings or formats.
- Use `or` only when the **spec itself** documents multiple equally valid outcomes.
- If the app diverges from the spec, the test should **fail** so the team can reconcile.

### Random data for length-based tests

When testing character limits, generate random strings via `BasePage` helpers instead of
hardcoded repeated characters:

```python
# Wrong
self.fill(self.INPUT, "A" * 255)

# Correct
self.fill(self.INPUT, self.random_chars(length=255))
```

---

## POM Structure Rules

- `BasePage` owns all generic interaction helpers (`click`, `fill`, `expect_visible`, …).
- Page-specific POM classes inherit `BasePage` and expose only domain-level actions.
- Assertions using `expect()` live in POM methods named `expect_*`.
- Boolean checks (`is_text_visible`, `is_column_header_visible`) return `bool` and are used in
  `assert` statements inside tests — they do NOT raise on their own.
- Fixtures in `conftest.py` create page objects; tests do not instantiate page classes directly.
- All locators live in POM files; no raw locators in test bodies.

---

## Fixtures

| Fixture | Purpose |
|---|---|
| `access_to_login_screen` | Opens the browser to the Login page. |
| `access_to_home_screen` | Logs in and navigates to the home page. |

Fixtures manage page initialization and navigation; test code should never set up browser state
independently.

---

## Constants and Messages

- Never hardcode UI strings or error messages in test code.
- Define them in `constants/messages.py` and import where needed.

```python
# constants/messages.py
ERROR_REQUIRED_EMAIL = "メールアドレスは必須です"

# test file
assert ERROR_REQUIRED_EMAIL in login.get_error_message()
```

---

## CI / Reporting

- Headless / headed mode is controlled by `HEADED` in `.env` (`true` = headed for local dev, `false` / absent = headless for CI).
- Allure results are written to `allure-results/` and reports to `allure-report/`.
- Screenshots are stored under `screenshots/<test_name>_<outcome>_<timestamp>.png`.
- Run `bash run_and_open_allure_report.sh` locally to execute tests, generate and open the Allure report.
- The GitHub Actions workflow uploads `allure-report/index.html` as artifact `html-report`.
- Never commit HTML dumps, screenshots, storage states, cookies, tokens, or files containing credentials.

---

## Adding a New Test File (checklist)

1. Copy `my_skill/assets/template_testcase.py` to `tests/<area>/test_<feature>.py`.
2. Add class-level `@allure.feature`, `@allure.story`, `@allure.url`, `@description_md`.
3. For each test: add `@allure.title` with zero-padded ID `<area>_<NNN>: <desc>` and
   `@description_md` with 前提条件 / テスト手順 / 期待する結果 from the CSV spec.
4. Use only POM methods in the test body — no raw locators.
5. Add assertion messages from `constants/messages.py`.
6. End every non-skipped test with a `with allure.step("[PASSED] ...")` block.
7. For any testcase where the spec is incomplete, use `pytest.skip(...)` with the reason.
