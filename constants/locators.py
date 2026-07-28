# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
# ---------------------------------------------------------------------------

class LoginLocators:
    EMAIL_PLACEHOLDER = "メールアドレス"    # <input id="mail_address" type="text">
    PASSWORD_PLACEHOLDER = "パスワード"      # <input id="password" type="password">
    LOGIN_BUTTON = "#login_button"          # ログインボタン

class EventHomeLocators:
    # Navigation tabs
    NAVIGATION_TABS = "a.navigation__item__name"  # ナビゲーションタブ一覧
    EVENT_TAB = 'イベント'
    PORTAL_TAB = 'ポータル'
    MEMBER_TAB = '会員管理'
    MAIL_TAB = '配信する'
    REPORT_TAB = 'レポート'

    # Widgets
    USAGE_LABEL = ".usage__label"
    DAU_LABEL = "1日ごと利用者（DAU）の合計"
    MEMBER_LABEL = "累計会員数（増加数）"


    TOOLTIP_ICON = ".tooltip-description i"
    TOOLTIP_CONTENT = ".v-tooltip__content"
    DAU_TOOLTIP_CONTENT = "イベントのWeb&Appへの訪問者数の合計です。「毎日の訪問者数（DAU）」の一ヶ月分の合計値です。"
    MEMBER_TAB_TOOLTIP_CONTENT = "現時点での会員登録数と、今月の新規会員登録数です。"

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
    EVENT_LIST_VIEW = "#event_list_view"              # リストエリア
    ACTIVE_BUTTON_CLASS = "v-btn--active"
