# eventos-automation-basic

Repo nền tảng cho training automation Eventos (sprint 20/07 - 27/07/2026).

**Nguồn gốc**: các file lõi trong repo này (`pages/base_page.py`, `pages/account_page.py`,
`helpers.py`, `constants/locators.py` phần dùng chung, `automation_rules.md`) được **port trực
tiếp** từ project nội bộ `eventos-automation-tests` bạn đã chia sẻ — không viết lại từ đầu, để
đảm bảo 4 team dùng đúng convention thật đang áp dụng, không phải một bộ quy tắc mới song song.

## 1. Setup lần đầu

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install

cp .env.example .env
# Điền APP_URL / VALID_EMAIL / VALID_PASSWORD thật vào .env

pytest tests/test_login.py -v
```

Nếu `ログイン_001` và `ログイン_002` đều pass, nghĩa là bạn đã setup đúng và đăng nhập được vào
Eventos — có thể bắt đầu code testcase của màn hình mình phụ trách.

## 2. Đọc `automation_rules.md` TRƯỚC khi code

File này copy nguyên vẹn từ `eventos-automation-tests` — đây là bộ quy tắc **thật** team đang
dùng, không phải quy tắc mới cho riêng đợt training. Các điểm quan trọng nhất:

- **Locator strategy ưu tiên**: `get_by_role` → `get_by_placeholder` → `get_by_text` →
  `get_by_label` → CSS attribute → XPath (chỉ dùng khi hết cách, phải ghi chú lý do).
- **Naming**: test method `test_<subject>_<condition>_<expected>`, `@allure.title` theo format
  `<khu_vực>_<NNN>: <mô tả>` (zero-pad 3 chữ số), test class `Test` + tên khu vực tiếng Nhật.
- **Mỗi test bắt buộc kết thúc bằng** `with allure.step("[PASSED] ..."): pass`.
- **`@description_md`** (import từ `helpers`) bắt buộc ở cả class và từng method — không dùng
  `@allure.description` thô.
- **Không dùng `@allure.severity`** trong project này.
- **Test độc lập**, không phụ thuộc thứ tự chạy hay state của test khác.
- **Spec chưa rõ** → tạo test, `pytest.skip(...)` kèm lý do cụ thể, không đoán hành vi.

Đọc kỹ phần "POM Structure Rules" và "Locator Discovery Process" trước khi tạo Page Object mới.

## 3. Cấu trúc thư mục

```
eventos-automation-basic/
├── automation_rules.md      # Bộ quy tắc thật - ĐỌC TRƯỚC KHI CODE
├── conftest.py               # Fixtures: access_to_login_screen, access_to_home_screen
├── helpers.py                # description_md decorator
├── constants/
│   ├── locators.py            # CommonLocators + DatePickerLocators (dùng chung)
│   └── messages.py            # Message liên quan Login
├── pages/
│   ├── base_page.py           # BasePage - click/fill/expect + random data generators
│   └── account_page.py        # AccountPage - login (KHÔNG sửa file này)
├── tests/
│   └── test_login.py          # Test xác nhận đăng nhập được - đã có sẵn
├── .env.example
├── requirements.txt
└── pytest.ini
```

## 4. Vì sao KHÔNG có sẵn locator/testcase cho Event-home / Portal / Member / Push-list

Repo `eventos-automation-tests` gốc thực ra đã có sẵn locator cho một số màn hình (ví dụ
`MemberListLocators`). Mình **cố tình không copy các class đó vào đây** — mục tiêu của sprint
này là để từng team tự trải qua quy trình khám phá locator thật (DevTools, `locator.count()`,
xác nhận uniqueness...) theo đúng "Locator Discovery Process" trong `automation_rules.md`, chứ
không phải paste sẵn đáp án. Nếu về sau cần tăng tốc, có thể xin phần đó từ Nhung.

## 5. Mỗi team triển khai tiếp như thế nào

Leader tạo trước (merge trước vào nhánh chung Tầng 2 của team), theo đúng thứ tự:

1. Thêm class locator riêng vào cuối `constants/locators.py`, ví dụ `EventHomeLocators`.
2. Tạo `pages/event_home_page.py` (hoặc `portal_page.py`, `member_list_page.py`,
   `push_notification_page.py`), **kế thừa `BasePage`**:

   ```python
   from pages.base_page import BasePage
   from constants.locators import EventHomeLocators as locators

   class EventHomePage(BasePage):
       def __init__(self, page):
           super().__init__(page)
       # thêm hàm riêng của màn hình ở đây, dùng self.click/self.fill/self.expect_visible...
   ```

3. Mỗi thành viên tạo file test riêng trong `tests/`, dùng fixture `access_to_home_screen` có sẵn
   để bắt đầu thẳng từ trạng thái đã đăng nhập:

   ```python
   from pages.event_home_page import EventHomePage

   class Testイベント_Event_home:
       @allure.title("Event-home_001: ...")
       @description_md("...")
       def test_xxx(self, access_to_home_screen):
           event_home = EventHomePage(access_to_home_screen)
           # ... code test case của bạn
           with allure.step("[PASSED] ..."):
               pass
   ```

4. Làm theo đúng quy tắc branch/commit/PR/review chéo trong file
   `Training_Automation_Eventos_Sprint1.xlsx` (sheet 00 và sheet màn hình tương ứng).

## 6. Report

```bash
allure serve allure-results
```

Screenshot (pass + fail) tự động đính kèm Allure report qua hook trong `conftest.py` — dùng
làm bằng chứng đính kèm MR theo quy tắc mới, không cần tự chụp/tự viết lại.

## 7. Lưu ý

- **Không sửa** `pages/base_page.py`, `pages/account_page.py`, `CommonLocators`/
  `DatePickerLocators` trong `constants/locators.py`, hoặc `conftest.py` mà không báo nhóm trước.
- File `.env` **không được commit** lên git.
- CI (GitHub Actions) chưa cấu hình ở repo này — bổ sung sau khi có secrets môi trường ổn định.
- 2 message lỗi login (`MSG_LOGIN_FAILED` / `MSG_LOGIN_FAILED_INPUT_CHECK`) trong
  `constants/messages.py` được port nguyên từ repo thật nhưng **có thể lệch với UI hiện tại** —
  cần xác nhận lại trước khi dùng để assert.
