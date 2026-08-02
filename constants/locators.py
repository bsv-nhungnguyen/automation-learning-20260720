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
    
    # サブタブ（page.get_by_role("link", name=..., exact=True) で使用）
    MEMBER_LIST_TAB = "会員リスト"  # 会員リストタブ
    MEMBER_ATTRIBUTE_SETTINGS_TAB = "会員属性の設定"  # 会員属性の設定タブ
    MEMBER_REGISTRATION_FORM_TAB = "会員登録フォーム"  # 会員登録フォームタブ
    APP_USERS_TAB = "アプリ利用者"  # アプリ利用者タブ
    MEMBER_WITHDRAWAL_SETTINGS_TAB = "会員退会設定"  # 会員退会設定タブ

    # サブタブリンク（active 判定用）
    MEMBER_LIST_TAB_LINK = ".member-list__tabs a[data-panel='list']"  # 会員リストタブリンク
    MEMBER_LIST_TAB_ACTIVE_CLASS = "v-tabs__item--active"  # タブアクティブ状態クラス
    SUB_TABS = ".member-list__tabs .v-tabs__item"     # 会員管理のサブタブ群
    TAB_ACTIVE_CLASS = "v-tabs__item--active"         # アクティブなサブタブのクラス

    # サブタブの表示パネル
    MEMBER_WITHDRAWAL_SETTINGS_PANEL = "#panel_withdraw"  # 会員退会設定パネル
    # tab_name → (URL hash, panel selector)
    MEMBER_SUB_TABS = {
        "会員属性の設定": ("#attribute", "#panel_attribute"),
        "会員登録フォーム": ("#form", "#panel_form"),
        "アプリ利用者": ("#app", "#panel_app"),
        "会員退会設定": ("#withdraw", "#panel_withdraw"),
    }

    # 会員リスト上部
    MEMBER_LIST_TITLE = "#panel_list .section-head"  # 会員リスト見出し（会員リスト（N））
    MEMBER_COUNT = "#panel_list .member-list__count"  # 会員数（見出し内）
    MEMBER_LIST_SUMMARY = ".member-list__summary"  # 表示件数サマリー
    MEMBERS_PER_PAGE_SELECT = "#member_per_page"  # 表示件数セレクトボックス
    SEARCH_BUTTON = "#btn_search"  # 検索ボタン
    NEW_MEMBER_REGISTRATION_BUTTON = "#btn_new_member"  # 新規会員登録ボタン

    # 検索パネル
    SEARCH_PANEL = "#search_panel"  # 検索条件パネル
    FILTER_MEMBER_ID_INPUT = "#filter_member_id"  # 会員ID検索入力欄
    FILTER_LOGIN_ID_INPUT = "#filter_login_id"  # ログインID検索入力欄
    FILTER_STATUS_SELECT = "#filter_status"  # 状態検索セレクトボックス
    EXECUTE_SEARCH_BUTTON = "#btn_do_search"  # この条件で検索ボタン
    CLOSE_SEARCH_BUTTON = "#btn_close_search"  # 検索パネルを閉じるボタン

    # 会員一覧テーブル
    MEMBER_TABLE = "#member_table"  # 会員一覧テーブル
    TABLE_HEADER = "#member_table thead th"           # テーブルヘッダー（列名）
    TABLE_BODY_ROW = "#member_table tbody tr"         # テーブル本文の各行
    TABLE_CELLS = "td"
    STATUS_COLUMN_HEADER = "状態"                     # 状態列のヘッダー文言
    TABLE_COLUMN_HEADERS = "#member_table thead th[role='columnheader']"  # 列ヘッダー
    TABLE_ROWS = "#member_table tbody tr"  # 会員データ行
    MEMBER_ID_HEADER = "#member_table thead th[data-col='1']"  # 会員ID列ヘッダー
    MEMBER_ID_CELL_IN_ROW = "td:nth-child(2)"  # 会員IDセル
    LOGIN_ID_CELL_IN_ROW = "td:nth-child(5)"  # ログインIDセル
    STATUS_CELL_IN_ROW = "td:nth-child(7) .v-chip"  # 状態セル
    SELECT_ALL_CHECKBOX = "#check_all"  # 全会員選択チェックボックス
    ROW_CHECKBOX = "input.member-row__check"  # 会員行選択チェックボックス

    # テーブル下部の一括操作
    MAIL_DELIVERY_BUTTON = "#btn_mail_send"  # メール配信ボタン
    BULK_ACTION_BUTTON = "#btn_bulk_action"  # 詳しい操作ボタン
