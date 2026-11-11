# ⚖️ WEIGHT UTILS

import re
import pandas as pd


WEIGHT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(кг|kg|г|гр|g)\b",
    re.IGNORECASE,
)

# Спеціальний формат: 60/68 г
SLASH_WEIGHT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*/\s*\d+(?:\.\d+)?\s*(кг|kg|г|гр|g)\b",
    re.IGNORECASE,
)

COUNT_FIRST_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*шт\s*[xх×*]\s*"
    r"(\d+(?:\.\d+)?)\s*(кг|kg|г|гр|g)\b",
    re.IGNORECASE,
)

COUNT_LAST_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(кг|kg|г|гр|g)\s*[xх×*]\s*"
    r"(\d+(?:\.\d+)?)\s*шт\b",
    re.IGNORECASE,
)

MULTIPLY_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*[xх×*]+\s*"
    r"(\d+(?:\.\d+)?)\s*(кг|kg|г|гр|g)\b",
    re.IGNORECASE,
)

WEIGHT_COUNT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(кг|kg|г|гр|g)\s*[xх×*]+\s*"
    r"(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)

PIECES_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*шт\b",
    re.IGNORECASE,
)


def clean(value):
    """Очищує текст перед пошуком ваги."""

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    value = str(value).lower().replace(",", ".")
    value = re.sub(r"[\xa0\u2009\u202f]", " ", value)

    return re.sub(r"\s+", " ", value).strip()


def to_kg(value, unit):
    """Переводить грами в кілограми."""

    unit = unit.lower()

    if unit in ("г", "гр", "g"):
        return round(value / 1000, 5)

    return round(value, 5)


def extract(text):
    """
    Повертає:
        (weight, package_count, unit_error)

    Звичайні грами конвертуються в кг:
        41,4 г -> 0.0414

    Для формату X/Y г береться перше число без конвертації:
        60/68 г -> 60.0
    """

    text = clean(text)

    if not text:
        return None, "", False

    # 1. Ваговий товар.
    if "ваг" in text:
        matches = list(WEIGHT_RE.finditer(text))

        if matches:
            m = matches[-1]
            weight = float(m.group(1))
            unit = m.group(2).lower()

            return to_kg(weight, unit), "Ваг", False

        return 1, "Ваг", False

    # 2. Формат 60/68 г.
    # Беремо перше число: 60, а не 68.
    m = SLASH_WEIGHT_RE.search(text)

    if m:
        return round(float(m.group(1)), 5), "", False

    # 3. Формат 6 шт*50 г.
    m = COUNT_FIRST_RE.search(text)

    if m:
        count = float(m.group(1))
        weight = float(m.group(2))
        unit = m.group(3).lower()

        unit_name = "G" if unit in ("г", "гр", "g") else "KG"

        return (
            to_kg(count * weight, unit),
            f"({count:g}*{weight:g}{unit_name})",
            False,
        )

    # 4. Формат 90 г*2 шт.
    m = COUNT_LAST_RE.search(text)

    if m:
        weight = float(m.group(1))
        unit = m.group(2).lower()
        count = float(m.group(3))

        unit_name = "G" if unit in ("г", "гр", "g") else "KG"

        return (
            to_kg(weight * count, unit),
            f"({count:g}*{weight:g}{unit_name})",
            False,
        )

    # 5. Формат 4*40 г або 3x150 г.
    m = MULTIPLY_RE.search(text)

    if m:
        count = float(m.group(1))
        weight = float(m.group(2))
        unit = m.group(3).lower()

        unit_name = "G" if unit in ("г", "гр", "g") else "KG"

        return (
            to_kg(count * weight, unit),
            f"({count:g}*{weight:g}{unit_name})",
            False,
        )

    # 6. Формат 40 г x 5.
    m = WEIGHT_COUNT_RE.search(text)

    if m:
        weight = float(m.group(1))
        unit = m.group(2).lower()
        count = float(m.group(3))

        unit_name = "G" if unit in ("г", "гр", "g") else "KG"

        return (
            to_kg(weight * count, unit),
            f"({count:g}*{weight:g}{unit_name})",
            False,
        )

    # 7. Звичайна вага.
    m = WEIGHT_RE.search(text)

    if m:
        weight = float(m.group(1))
        unit = m.group(2).lower()

        return to_kg(weight, unit), "", False

    # 8. Кількість штук без вказаної ваги.
    m = PIECES_RE.search(text)

    if m:
        count = float(m.group(1))
        return None, f"({count:g}*ШТ)", False

    return None, "", False


def parse_weight(value):
    """Перетворює значення Weight на число."""

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    text = str(value).strip().replace(",", ".")

    if not text:
        return None

    try:
        return float(text)
    except (ValueError, TypeError):
        return None
