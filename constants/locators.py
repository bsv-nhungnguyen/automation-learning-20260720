# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"           # ログインボタン

class PushListLocators:

    # Radio
    IMMEDIATE_DELIVERY_RADIO = "即時配信する"
    SCHEDULE_DELIVERY_RADIO = "予約配信する"

    # DateTime
    SCHEDULE_AREA = "#schedule_area"
    SCHEDULE_DATE = "#schedule_date"
    SCHEDULE_TIME = "#schedule_time"

    # Button
    CREATE_BUTTON = "新規作成"
    CANCEL_BUTTON = "キャンセル"
    CLOSE_BUTTON = "閉じる"
    DELIVERY_BUTTON = "配信する"
    DELIVERY_LIST = "a[href*='push_list.html']"

    # Dialog? Modal?
    MODAL = "aside[role='dialog']"


    # Input
    TITLE_PLACEHOLDER = "管理用タイトルを入力してください（ユーザーには送信されません）"
    MESSAGE_PLACEHOLDER = "配信内容を入力してください"