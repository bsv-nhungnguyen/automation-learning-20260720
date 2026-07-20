# ---------------------------------------------------------------------------
# Locator constants — shared across all page object classes
# Each entry has a comment with the Japanese field/element name
# ---------------------------------------------------------------------------
class CommonLocators:
    
    # -----------------------------------------------------------------------
    # ボタン / Buttons
    # -----------------------------------------------------------------------
    BUTTON_SAVE = "保存する"  # 保存するボタン
    BUTTON_SAVE_1 = "保存"  # 保存ボタン（別パターン）
    BUTTON_CANCEL = "キャンセル"  # キャンセルボタン
    BUTTON_NO = "いいえ"  # いいえボタン
    BUTTON_RUN = "実行"  # 実行ボタン
    BUTTON_DELETE = "削除する"  # 削除ボタン
    COMPONENT_LAYOUT = "//main[@class = 'v-content home-layout']"  # コンポーネントレイアウト
    DIAGLOG_ACTIVE = "//div[contains(@class,'v-dialog--active')]" # アクティブなダイアログ全般
    DATE_PICKER_YEAR = "//div[contains(@class,'v-dialog--active')]//ul[contains(@class,'v-date-picker-years')]"  # 日付ピッカーの年リスト
    DATE_PICKER_YEAR_ITEM = "//div[contains(@class,'v-dialog--active')]//ul[contains(@class,'v-date-picker-years')]//li"  # 年リストの各アイテム
    DATE_PICKER_MONTH = "//div[contains(@class,'v-date-picker-table--month')]"  # 日付ピッカーの月グリッド
    DATE_PICKER_MONTH_BTN = "//div[contains(@class,'v-dialog--active')]//div[contains(@class,'v-date-picker-table--month')]//button"  # 月グリッドのボタン（アクティブダイアログ内）
    DATE_PICKER_DATE = "//div[contains(@class,'v-dialog--active')]//div[contains(@class,'v-date-picker-table--date')]"  # 日付ピッカーの日グリッド（アクティブダイアログ内）
    DATE_PICKER_DAY_BTN_ENABLED = "//div[contains(@class,'v-dialog--active')]//div[contains(@class,'v-date-picker-table--date')]//button[not(contains(@class,'v-btn--disabled'))]"  # 選択可能な日ボタン（アクティブダイアログ内）
    # HEADER_DATE_PICKER_YEAR = "//div[contains(@class,'v-dialog--active')]//div[contains(@class,'v-date-picker-title__year')]"  # 日付ピッカータイトル内の年（クリックで年リストへ遷移、アクティブダイアログ内）

class DatePickerLocators:

    # -----------------------------------------------------------------------
    # ダイアログ / Dialog
    # -----------------------------------------------------------------------
    DIALOG = "//div[contains(@class,'v-dialog--active') and not(contains(@class,'v-dialog--scrollable'))]"  # 日付ピッカーダイアログ（edit formのv-dialog--scrollableを除外）

    # -----------------------------------------------------------------------
    # ヘッダー / Header
    # -----------------------------------------------------------------------
    HEADER = ".v-date-picker-header"                          # 日付ピッカーヘッダー
    HEADER_VALUE = ".v-date-picker-header__value"             # ヘッダー内の年月テキストエリア
    HEADER_VALUE_BTN = ".v-date-picker-header__value button"  # ヘッダー内の年月切替ボタン

    # -----------------------------------------------------------------------
    # 年リスト / Year list
    # -----------------------------------------------------------------------
    YEAR_LIST = ".v-date-picker-years"       # 年リストコンテナ
    YEAR_ITEMS = ".v-date-picker-years li"   # 年リストの各アイテム（JS evaluate 用）

    # -----------------------------------------------------------------------
    # 月グリッド / Month grid
    # -----------------------------------------------------------------------
    MONTH_TABLE = ".v-date-picker-table--month"          # 月グリッドコンテナ
    MONTH_BUTTONS = ".v-date-picker-table--month button"  # 月グリッドの各ボタン

    # -----------------------------------------------------------------------
    # 日グリッド / Day grid
    # -----------------------------------------------------------------------
    DATE_TABLE = ".v-date-picker-table--date"                              # 日グリッドコンテナ
    DATE_BUTTONS_ENABLED = ".v-date-picker-table--date button:not(.v-btn--disabled)"  # 選択可能な日ボタン


# ---------------------------------------------------------------------------
# TU DAY TRO XUONG: moi team tu them class locator rieng cho man hinh minh
# phu trach (Event-home / Portal / Member / Push-list), theo dung format o
# tren. KHONG sua CommonLocators / DatePickerLocators ma khong bao nhom truoc.
#
# Vi du:
# class EventHomeLocators:
#     SEARCH_INPUT_PLACEHOLDER = "キーワードを入力"  # o tim kiem event
#     ...
# ---------------------------------------------------------------------------
