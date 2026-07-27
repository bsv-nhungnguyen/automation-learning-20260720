import os
import glob
import pytest
from datetime import datetime
from playwright.sync_api import Page
from dotenv import load_dotenv
import allure

load_dotenv()

from pages.account_page import AccountPage

# Globals — updated by pytest_configure before any test runs
_MAX_RERUNS: int = 0
_RERUN_FAIL_VIDEO_HOLD_MS: int = 1500


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _extract_page_from_item(item) -> "Page | None":
    """Return the Playwright Page from test fixtures, however it is nested."""
    page = item.funcargs.get("page")
    if page:
        return page
    # Moi team them ten fixture rieng cua man hinh minh vao tuple duoi day
    # (vi du "event_home", "portal_home", "push_list") de hook nay van chup
    # duoc screenshot/video dung cho fixture cua team.
    for name in ("access_to_login_screen", "access_to_home_screen"):
        fixture = item.funcargs.get(name)
        if fixture and hasattr(fixture, "page"):
            return fixture.page
    return None


def _is_rerun_enabled() -> bool:
    return _MAX_RERUNS > 0


def _is_event_loop_closed_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in ("event loop is closed", "connection closed", "target closed"))


def _get_video_path_without_rpc(video) -> "str | None":
    """Extract video path from internal Playwright object without making an RPC call."""
    impl = getattr(video, "_impl_obj", None)
    if impl:
        return getattr(impl, "_artifact_path", None)
    return None


def _find_recent_video_file_for_item(item_name: str) -> "str | None":
    """Find the most recently written video file, preferring files whose path contains item_name."""
    for pattern in ("videos/**/*.webm", "videos/**/*.mp4", ".videos/**/*.webm"):
        candidates = sorted(glob.glob(pattern, recursive=True), key=os.path.getmtime, reverse=True)
        named = [c for c in candidates if item_name in c]
        if named:
            return named[0]
        if candidates:
            return candidates[0]
    return None


# ---------------------------------------------------------------------------
# pytest hooks
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Apply HEADED setting from .env and capture --reruns count."""
    global _MAX_RERUNS
    headed = os.getenv("HEADED", "false").strip().lower() == "true"
    try:
        config.option.headed = headed
    except AttributeError:
        pass  # playwright plugin not yet loaded
    try:
        _MAX_RERUNS = int(getattr(config.option, "reruns", 0) or 0)
    except (AttributeError, TypeError, ValueError):
        _MAX_RERUNS = 0


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # `call` is required by pytest hook signature
    """Attach screenshot (pass+fail) and video (fail only) to Allure and pytest-html."""
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        setattr(item, "rep_call", result)

    if result.when == "call" and result.failed:
        if not hasattr(item, "first_fail"):
            setattr(item, "first_fail", True)
        page = _extract_page_from_item(item)
        if page and _is_rerun_enabled():
            try:
                page.wait_for_timeout(_RERUN_FAIL_VIDEO_HOLD_MS)
            except Exception:
                pass

    # ── Screenshot on every call (pass + fail) — dùng làm bằng chứng đính kèm MR ──
    if result.when == "call" and not getattr(item, "custom_screenshot_taken", False):
        page = _extract_page_from_item(item)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "FAILED" if result.failed else "PASSED"

        if page:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"{item.name}_{timestamp}_{status}",
                    attachment_type=allure.attachment_type.PNG,
                )
                print(f"📸 Screenshot captured for {item.name} ({status})")
            except Exception as e:
                allure.attach(
                    body=f"Could not capture screenshot: {e}",
                    name=f"{item.name}_{timestamp}_SCREENSHOT_ERROR",
                    attachment_type=allure.attachment_type.TEXT,
                )

    # ── Video on teardown (failed tests only) ───────────────────────────────
    if result.when == "teardown" and getattr(item, "rep_call", None) and item.rep_call.failed:
        current_attempt = getattr(item, "execution_count", 1)
        is_intermediate_rerun = _MAX_RERUNS > 0 and current_attempt <= _MAX_RERUNS

        page = _extract_page_from_item(item)
        video = getattr(page, "video", None) if page else None

        if video:
            try:
                video_path = video.path()
                if video_path and os.path.exists(video_path):
                    allure.attach.file(
                        video_path,
                        name=f"{item.name}_FAILED_VIDEO",
                        attachment_type=allure.attachment_type.MP4,
                    )
                    print(f"🎥 Video attached for {item.name}: {video_path}")
            except Exception as e:
                if _is_event_loop_closed_error(e):
                    fallback = (
                        _get_video_path_without_rpc(video)
                        or _find_recent_video_file_for_item(item.name)
                    )
                    if fallback and os.path.exists(fallback):
                        allure.attach.file(
                            fallback,
                            name=f"{item.name}_FAILED_VIDEO_FALLBACK",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                        print(f"🎥 Video (fallback) attached for {item.name}: {fallback}")
                else:
                    allure.attach(
                        body=f"Could not attach video: {e}",
                        name=f"{item.name}_VIDEO_ERROR",
                        attachment_type=allure.attachment_type.TEXT,
                    )

        if is_intermediate_rerun:
            print(f"🔁 Rerun attempt {current_attempt}/{_MAX_RERUNS + 1} failed — deferred to final attempt.")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app_url() -> str:
    url = os.getenv("APP_URL")
    if not url:
        raise RuntimeError("APP_URL chưa được set — thêm vào file .env (xem .env.example).")
    return url.rstrip("/")


def _login_url(app_url: str) -> str:
    """sample_UI uses login.html; console staging uses /login."""
    if "sample_UI" in app_url:
        return f"{app_url}/login.html"
    return f"{app_url}/login"


@pytest.fixture
def access_to_login_screen(page: Page, app_url: str) -> AccountPage:
    """Mở trang login, trả về AccountPage."""
    page.goto(_login_url(app_url))
    page.wait_for_load_state("networkidle")
    return AccountPage(page)


@pytest.fixture
def access_to_home_screen(page: Page, app_url: str) -> Page:
    """Login thành công, dừng lại ở event-home. Trả về raw Page - mỗi team tự
    bọc lại bằng Page Object của màn hình mình (kế thừa BasePage), ví dụ:

        def test_xxx(self, access_to_home_screen):
            event_home = EventHomePage(access_to_home_screen)
            ...

    Không tạo fixture riêng cho từng màn hình ở đây - mỗi team tự thêm fixture
    của mình trong file conftest.py con (vd tests/event_home/conftest.py) nếu
    cần, theo đúng pattern trong automation_rules.md.
    """
    page.goto(_login_url(app_url))
    page.wait_for_load_state("networkidle")
    login = AccountPage(page)
    login.login(
        os.getenv("VALID_EMAIL"),
        os.getenv("VALID_PASSWORD"),
    )
    return page
