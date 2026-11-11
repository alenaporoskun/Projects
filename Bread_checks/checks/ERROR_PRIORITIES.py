# ⚠️ ERROR PRIORITIES — пріоритети помилок
# Опис: пріоритети помилок для перевірки Weight

ERROR_PRIORITIES = {
    # 🔴 CRITICAL — критичні помилки
    "EMPTY_WEIGHT": "CRITICAL",
    "WEIGHT_NOT_NUMBER": "CRITICAL",
    "WEIGHT_OUT_OF_RANGE": "CRITICAL",
    "WEIGHT_MISMATCH": "CRITICAL",
    "COUNT_MISMATCH": "CRITICAL",
    "PACK_SET_MISMATCH": "CRITICAL",

    # 🟡 WARNING — попередження
    "ID_SKU+ARTICLE_WEIGHT_DIFFERENT": "WARNING",
    "ID_SKU+ARTICLE_PACKAGE_COUNT_DIFFERENT": "WARNING",

    # 🔵 INFO — інформаційні повідомлення
    "NO_WEIGHT_FOUND": "INFO",
    "WEIGHT_UNIT_IN_NAME": "INFO",
}