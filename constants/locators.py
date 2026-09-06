# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"          # ログインボタン

class PushListLocators:
    CREATE_BUTTON = "#btn_push_create"  # プッシュ配信一覧: 「新規作成」ボタン
    DRAWER = "#push_drawer"             # プッシュ配信作成ドロワー（右側スライドパネル）

    # CSS attribute (adjacent sibling): required の "*" は role/label で一意に
    # 特定できないため、対応する <label for="..."> の直後の要素として scope する。
    TITLE_REQUIRED_MARK = "label[for='push_title'] + span.required"        # 配信管理用タイトル: 必須マーク
    SEGMENT_REQUIRED_MARK = "label[for='segment_select'] + span.required"  # セグメントルールを選択する: 必須マーク
    MESSAGE_REQUIRED_MARK = "label[for='push_message'] + span.required"    # メッセージ: 必須マーク

    TARGET_SEGMENT_RADIO_LABEL = "セグメントルールから選ぶ"  # 配信する対象の作成方法: ラジオ（デフォルト選択）
    SEND_IMMEDIATE_RADIO_LABEL = "即時配信する"              # 配信タイプ: ラジオ（デフォルト選択）
    
    # --- Thêm cho 配信する_003 / 配信する_004 (TC03-04) ---
    TITLE_PLACEHOLDER = "管理用タイトルを入力してください（ユーザーには送信されません）"  # 配信管理用タイトル入力欄
    MESSAGE_PLACEHOLDER = "配信内容を入力してください"  # メッセージ入力欄
    SEGMENT_SELECT = "#segment_select"  # セグメントルールを選択するセレクトボックス
    SUBMIT_BUTTON = "#push_submit"  # 配信するボタン（id はユニークなので画面 id 不要）
    SEGMENT_FIRST_OPTION = "#segment_select option:nth-child(2)"  # セグメントルール: 1番目の選択肢（プレースホルダーの次）
    

    SEGMENT_AREA = "#segment_area"  # セグメントルール入力エリア
    CSV_AREA = "#csv_area"  # CSVアップロードエリア
    TITLE_INPUT = "#push_title"  # 配信管理用タイトル入力欄

     # --- Thêm cho TC07-08 ---
    SCHEDULE_DELIVERY_RADIO = "予約配信する"
    SCHEDULE_AREA = "#schedule_area"
    SCHEDULE_DATE = "#schedule_date"
    SCHEDULE_TIME = "#schedule_time"
    CANCEL_BUTTON = "キャンセル"

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


class EventHomeLocators:
    # Navigation tabs
    NAVIGATION_TABS = "a.navigation__item__name"  # ナビゲーションタブ一覧
    EVENT_TAB = 'イベント'
    PORTAL_TAB = 'ポータル'
    MEMBER_TAB = '会員管理'
    MAIL_TAB = '配信する'
    REPORT_TAB = 'レポート'

    # Widgets
    WIDGET_LABEL = ".usage__label"
    TOOLTIP_ICON = ".tooltip-description i"
    TOOLTIP_CONTENT = ".v-tooltip__content"

    # Event table / イベント一覧テーブル
    EVENT_TABLE_HEADERS = "table th"  # テーブルヘッダー（list view）
    EVENT_LIST_VIEW = "#event_list_view"  # リスト表示エリア

    EVENT_TABLE_COLUMN_HEADERS = [
        "ID",
        "リリース環境",
        "画像",
        "イベント名",
        "住所",
        "ジャンル",
        "説明文",
        "開催期間",
        "自社ポータル",
        "備考",
        "編集",
    ]

    # Create event / 新規イベント作成
    CREATE_EVENT_BUTTON = "#btn_create_event"        # 新規イベント作成ボタン
    CREATE_EVENT_CLOSE = "#create_event_close"        # ダイアログ閉じる
    CREATE_EVENT_FORM_LABEL = "イベント名※必須"       # form mở (marker)

    # View toggle
    GRID_VIEW_BUTTON = "#btn_grid_view"               # グリッド
    LIST_VIEW_BUTTON = "#btn_list_view"               # リスト
    EVENT_GRID_VIEW = "#event_grid_view"              # グリッドエリア
    ACTIVE_BUTTON_CLASS = "v-btn--active"

    # Announcements / お知らせ
    ANNOUNCEMENT_LIST = "ul.information__list"
    ANNOUNCEMENT_ITEM = "ul.information__list > li.information__item"
    ANNOUNCEMENT_DATE = "span.information__date"
    ANNOUNCEMENT_TAG = "span.information__tag"
    ANNOUNCEMENT_TITLE = "a.information__title"
    ANNOUNCEMENT_NEW_BADGE = "span.information__new"

    # イベント一覧 — キーワード検索
    SEARCH_PLACEHOLDER = "キーワードを入力"                  # キーワード検索入力欄 <input id="event_search_input">
    EVENT_TABLE_ROW_VISIBLE = "#event_table tbody tr:visible" # 絞り込み後に表示されているイベント行
    EVENT_NAME_CELL = "#event_table tbody tr td:nth-child(4)" # イベント名セル（4列目）
    TRUNCATION_SUFFIXES = ("...", "…")                       # イベント名が省略表示された場合の末尾記号

    # イベント一覧 — ページャー（表示件数を持つ方がイベント一覧用）
    PAGINATION_WRAPPER = ".pagination__wrapper:has(#per_page_select)"  # イベント一覧のページャー領域
    PAGINATION_SUMMARY = "#pagination_summary"               # 件数サマリー「2件中 1 - 2件目」
    PAGINATION_TOTAL_PATTERN = r"(\d+)\s*件中"                # サマリーから総件数を取り出す正規表現
    PER_PAGE_SELECT = "#per_page_select"                     # 表示件数プルダウン <select id="per_page_select">


class PortalLocators:
    # --- ポータル名 ---
    PORTAL_NAME_TITLE = ".submit__name .submit__title"  # ポータル名ラベル
    REQUIRED_MARK = ".submit__name span.required"  # ※必須（赤）
    PORTAL_NAME_INPUT = "#portal_name"  # ポータル名入力欄

    # --- 保存する ---
    SAVE_BUTTON = "#portal_save_button"  # 保存するボタン
    DISABLED_BUTTON_CLASS = "disabled-button"  # 無効時のグレー表示class

    # --- ポータルアイコン ---
    ICON_SECTION = ".submit__icon"  # ポータルアイコンブロック
    ICON_PLACEHOLDER = "#portal_icon_placeholder"  # アイコンプレースホルダー
    SELECT_FILE_BUTTON = "#btn_select_file"  # ファイルを選択ボタン
    SELECT_FILE_BUTTON_NAME = "ファイルを選択"  # ファイルを選択（role name）
    FILE_INPUT = "#portal_icon"  # ファイルinput（accept=.png,.jpg,.jpeg）
    ICON_FILENAME = "#portal_icon_filename"  # アップロード後のファイル名表示
    REMOVE_FILE_BUTTON = "#btn_remove_file"  # 画像を削除ボタン
    ICON_PREVIEW = "#portal_icon_placeholder img"  # アップロード後のプレビュー画像

    # --- ツールチップ (?) ---
    TOOLTIP_NAME_ARIA = "ポータル名の説明"  # ポータル名の(?)ボタン
    TOOLTIP_ICON_ARIA = "ポータルアイコンの説明"  # ポータルアイコンの(?)ボタン
    TOOLTIP_MESSAGE = ".v-tooltip__content--active .tooltip-message"  # ツールチップ本文

    # --- ヘッダーナビ ---
    
    NAV_TABS = "ul.navigation .navigation__item__name > div"  # 全タブ
