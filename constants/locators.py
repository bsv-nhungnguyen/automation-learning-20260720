# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"          # ログインボタン


class MemberListPageLocators:
    NAV_MEMBER = "会員管理"                            # ヘッダーナビ「会員管理」
    MEMBER_TABLE = "#member_table"                    # 会員リストのデータテーブル
    TABLE_HEADER = "#member_table thead th"           # テーブルヘッダー（列名）
    TABLE_BODY_ROW = "#member_table tbody tr"         # テーブル本文の各行
    STATUS_COLUMN_HEADER = "状態"                     # 状態列のヘッダー文言
    SUB_TABS = ".member-list__tabs .v-tabs__item"     # 会員管理のサブタブ群
    TAB_ACTIVE_CLASS = "v-tabs__item--active"         # アクティブなサブタブのクラス
    PANEL_PREFIX = "#panel_"                          # サブタブパネル id 接頭辞 (panel_*)