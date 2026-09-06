from constants.validation_rules import MAX_LENGTH_PUSH_TITLE


class EventHomeTestData:
    PREV_PAGE_BUTTON = "前へ"                                 # 前ページボタン
    NEXT_PAGE_BUTTON = "次へ"                                 # 次ページボタン
    PER_PAGE_DEFAULT = "25"                                  # 表示件数の初期値


TITLE_OVERFLOW_INPUT = "A" * (MAX_LENGTH_PUSH_TITLE + 1)
CSV_UPLOAD_RADIO_LABEL = "CSVからアップロードする"
