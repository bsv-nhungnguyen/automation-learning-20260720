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