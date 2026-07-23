# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"          # ログインボタン


class PortalLocators:
    # --- ポータル名 ---
    PORTAL_NAME_TITLE = ".submit__name .submit__title"  # ポータル名ラベル
    REQUIRED_MARK = ".submit__name span.required"  # ※必須（赤）
    PORTAL_NAME_PLACEHOLDER = "ポータル名を入力してください"  # ポータル名入力欄（placeholder）
    PORTAL_NAME_INPUT = "#portal_name"  # ポータル名入力欄

    # --- 保存する ---
    SAVE_BUTTON = "#portal_save_button"  # 保存するボタン
    SAVE_BUTTON_NAME = "保存する"  # 保存する（role name）
    DISABLED_BUTTON_CLASS = "disabled-button"  # 無効時のグレー表示class

    # --- ポータルアイコン ---
    ICON_SECTION = ".submit__icon"  # ポータルアイコンブロック
    ICON_PLACEHOLDER = "#portal_icon_placeholder"  # アイコンプレースホルダー
    SELECT_FILE_BUTTON = "#btn_select_file"  # ファイルを選択ボタン
    SELECT_FILE_BUTTON_NAME = "ファイルを選択"  # ファイルを選択（role name）
    FILE_INPUT = "#portal_icon"  # ファイルinput（accept=.png,.jpg,.jpeg）
    ICON_GUIDE_TEXT = ".submit__icon .text__size"  # サイズ案内テキスト

    # --- ツールチップ (?) ---
    TOOLTIP_NAME_ARIA = "ポータル名の説明"  # ポータル名の(?)ボタン
    TOOLTIP_ICON_ARIA = "ポータルアイコンの説明"  # ポータルアイコンの(?)ボタン
    TOOLTIP_ACTIVE = ".v-tooltip__content--active"  # 表示中のツールチップ
    TOOLTIP_MESSAGE = ".v-tooltip__content--active .tooltip-message"  # ツールチップ本文

    # --- ヘッダーナビ ---
    NAV_ACTIVE_TAB = "ul.navigation .navigation__item__name .active"  # アクティブタブ
    NAV_TABS = "ul.navigation .navigation__item__name > div"  # 全タブ