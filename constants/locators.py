# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"          # ログインボタン


class MemberListPageLocators:
    
    # サブタブ（page.get_by_role("link", name=..., exact=True) で使用）

    # サブタブリンク（active 判定用）
    MEMBER_LIST_TAB_LINK = ".member-list__tabs a[data-panel='list']"  # 会員リストタブリンク
    MEMBER_LIST_TAB_ACTIVE_CLASS = "v-tabs__item--active"  # タブアクティブ状態クラス
    SUB_TABS = ".member-list__tabs .v-tabs__item"     # 会員管理のサブタブ群

    # サブタブ名
    MEMBER_ATTRIBUTE_SETTINGS_TAB = "会員属性の設定"
    MEMBER_REGISTRATION_FORM_TAB = "会員登録フォーム"
    APP_USERS_TAB = "アプリ利用者"
    MEMBER_WITHDRAWAL_SETTINGS_TAB = "会員退会設定"

    # サブタブ URL hash
    MEMBER_ATTRIBUTE_SETTINGS_HASH = "#attribute"
    MEMBER_REGISTRATION_FORM_HASH = "#form"
    APP_USERS_HASH = "#app"
    MEMBER_WITHDRAWAL_SETTINGS_HASH = "#withdraw"

    # サブタブパネル
    MEMBER_ATTRIBUTE_SETTINGS_PANEL = "#panel_attribute"
    MEMBER_REGISTRATION_FORM_PANEL = "#panel_form"
    APP_USERS_PANEL = "#panel_app"
    MEMBER_WITHDRAWAL_SETTINGS_PANEL = "#panel_withdraw"

    # 会員リスト上部
    MEMBER_LIST_TITLE = "#panel_list .section-head"  # 会員リスト見出し（会員リスト（N））
    MEMBER_COUNT = "#panel_list .member-list__count"  # 会員数（見出し内）
    SEARCH_BUTTON = "#btn_search"  # 検索ボタン
    NEW_MEMBER_REGISTRATION_BUTTON = "#btn_new_member"  # 新規会員登録ボタン

    # 検索パネル
    SEARCH_PANEL = "#search_panel"  # 検索条件パネル
    FILTER_MEMBER_ID_INPUT = "#filter_member_id"  # 会員ID検索入力欄
    FILTER_LOGIN_ID_INPUT = "#filter_login_id"  # ログインID検索入力欄
    FILTER_STATUS_SELECT = "#filter_status"  # 状態検索セレクトボックス

    # 会員一覧テーブル
    TABLE_HEADER = "#member_table thead th"           # テーブルヘッダー（列名）
    TABLE_CELLS = "td"
    STATUS_COLUMN_HEADER = "状態"                     # 状態列のヘッダー文言
    TABLE_COLUMN_HEADERS = "#member_table thead th[role='columnheader']"  # 列ヘッダー
    TABLE_ROWS = "#member_table tbody tr"  # 会員データ行
    MEMBER_ID_HEADER = "#member_table thead th[data-col='1']"  # 会員ID列ヘッダー
    MEMBER_ID_CELL_IN_ROW = "td:nth-child(2)"  # 会員IDセル
    ROW_CHECKBOX = "input.member-row__check"  # 会員行選択チェックボックス

    # テーブル下部の一括操作
