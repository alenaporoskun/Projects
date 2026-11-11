# ⚖️ WEIGHT CHECK — перевірка Weight та Pack_Set

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from checks.weight_utils import extract, parse_weight
from checks.ERROR_PRIORITIES import ERROR_PRIORITIES


OUTPUT_COLUMNS = [
    "ID_SKU",
    "ARTICLE_NAME_WEB",
    "Weight",
    "Expected_Weight",
    "Pack_Set",
    "Expected_Pack_Set",
    "ERRORS",
    "PRIORITY",
]

MIN_WEIGHT = 0.0035
MAX_WEIGHT = 1000
WEIGHT_TOLERANCE = 0.001


def load_weight_exceptions(exceptions_dir):
    """Завантажує ID_SKU, які потрібно пропускати."""

    path = Path(exceptions_dir) / "EXCEPTIONS_Weight.xlsx"

    if not path.exists():
        return set()

    exceptions_df = pd.read_excel(path, dtype={"ID_SKU": str})

    if "ID_SKU" not in exceptions_df.columns:
        print(
            "⚠️ WEIGHT: у EXCEPTIONS_Weight.xlsx "
            "відсутня колонка ID_SKU"
        )
        return set()

    return set(
        exceptions_df["ID_SKU"]
        .dropna()
        .astype(str)
        .str.strip()
    )


def is_empty(value):
    """Перевіряє, чи значення порожнє."""

    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass

    return str(value).strip() == ""


def normalize_text(value):
    if is_empty(value):
        return ""
    return str(value).strip()


def normalize_pack(value):
    """Нормалізує Pack_Set."""

    if is_empty(value):
        return ""

    return (
        str(value)
        .strip()
        .upper()
        .replace(" ", "")
        .replace("Х", "*")
        .replace("X", "*")
        .replace("×", "*")
    )


def get_pack_count(value):
    """Отримує кількість з формату на кшталт (6*50G) або (6*ШТ)."""

    pack = normalize_pack(value)

    match = re.fullmatch(
        r"\(?(\d+(?:\.\d+)?)\*.+\)?",
        pack,
    )

    return float(match.group(1)) if match else None


def is_count_only_pack(value):
    """Перевіряє формат кількості без ваги."""

    return bool(
        re.fullmatch(
            r"\(?\d+(?:\.\d+)?\*ШТ\)?",
            normalize_pack(value),
        )
    )


def packs_match(expected_pack, actual_pack):
    """Порівнює очікувану та фактичну упаковку."""

    expected = normalize_pack(expected_pack)
    actual = normalize_pack(actual_pack)

    if not expected or not actual:
        return False

    if is_count_only_pack(expected):
        expected_count = get_pack_count(expected)
        actual_count = get_pack_count(actual)

        return (
            expected_count is not None
            and actual_count is not None
            and expected_count == actual_count
        )

    return expected == actual


def get_priority(errors):
    """Визначає найвищий пріоритет помилок."""

    priority_order = {
        "CRITICAL": 3,
        "WARNING": 2,
        "INFO": 1,
    }

    priorities = []

    for error in errors:
        if error not in ERROR_PRIORITIES:
            raise KeyError(
                f"Помилка '{error}' відсутня в ERROR_PRIORITIES"
            )

        priorities.append(ERROR_PRIORITIES[error])

    return max(
        priorities,
        key=lambda priority: priority_order.get(priority, 0),
        default="",
    )


def check_weight(df, file_type, exceptions_dir, results_dir):
    """Перевіряє вагу та Pack_Set і зберігає критичні помилки."""

    exceptions = load_weight_exceptions(exceptions_dir)
    results = []

    for _, row in df.iterrows():
        sku = normalize_text(row.get("ID_SKU", ""))
        article_name = row.get("ARTICLE_NAME_WEB", "")
        category = row.get("Category", "")
        class_1 = row.get("Class_1", "")

        # Пропускаємо винятки.
        if sku in exceptions:
            continue

        # Пропускаємо Category = NON.
        if (
            not is_empty(category)
            and str(category).strip().lower() == "non"
        ):
            continue

        # Пропускаємо записи без Class_1.
        if is_empty(class_1):
            continue

        raw_weight = row.get("Weight")
        raw_pack = row.get("Pack_Set")

        actual_weight = parse_weight(raw_weight)
        actual_pack = normalize_pack(raw_pack)

        # Визначаємо очікувану вагу й упаковку з ID_SKU та назви.
        sku_weight, sku_pack, sku_unit_error = extract(sku)
        name_weight, name_pack, name_unit_error = extract(article_name)

        if (
            sku_weight is None
            and name_weight is None
            and not sku_pack
            and not name_pack
        ):
            continue

        expected_weight = (
            sku_weight if sku_weight is not None else name_weight
        )
        expected_pack = sku_pack or name_pack

        if sku_weight is not None or sku_pack:
            unit_error = sku_unit_error
        else:
            unit_error = name_unit_error

        errors = []

        # Перевірка порожньої або нечислової ваги.
        if is_empty(raw_weight):
            errors.append("EMPTY_WEIGHT")
        elif actual_weight is None:
            errors.append("WEIGHT_NOT_NUMBER")

        # Перевірка діапазону.
        if (
            actual_weight is not None
            and not MIN_WEIGHT <= actual_weight <= MAX_WEIGHT
        ):
            errors.append("WEIGHT_OUT_OF_RANGE")

        # Порівняння ваги в ID_SKU та назві.
        weights_different = (
            sku_weight is not None
            and name_weight is not None
            and abs(sku_weight - name_weight) > WEIGHT_TOLERANCE
        )

        if weights_different:
            errors.append("ID_SKU+ARTICLE_WEIGHT_DIFFERENT")

        # Порівняння упаковки в ID_SKU та назві.
        packages_different = (
            bool(sku_pack)
            and bool(name_pack)
            and not packs_match(sku_pack, name_pack)
        )

        if packages_different:
            errors.append("ID_SKU+ARTICLE_PACKAGE_COUNT_DIFFERENT")

        # Помилка одиниць ваги.
        if unit_error:
            errors.append("WEIGHT_UNIT_IN_NAME")

        # Порівняння фактичної ваги з очікуваною.
        if (
            expected_weight is not None
            and actual_weight is not None
            and not weights_different
            and not unit_error
            and abs(expected_weight - actual_weight) > WEIGHT_TOLERANCE
        ):
            errors.append("WEIGHT_MISMATCH")

        # Порівняння Pack_Set.
        if (
            expected_pack
            and not packages_different
            and not packs_match(expected_pack, actual_pack)
        ):
            errors.append("PACK_SET_MISMATCH")

        # Видаляємо дублікати помилок.
        errors = list(dict.fromkeys(errors))

        if not errors:
            continue

        priority = get_priority(errors)

        # У звіт потрапляють тільки CRITICAL.
        if priority != "CRITICAL":
            continue

        results.append(
            {
                "ID_SKU": sku,
                "ARTICLE_NAME_WEB": article_name,
                "Weight": raw_weight,
                "Expected_Weight": expected_weight,
                "Pack_Set": actual_pack,
                "Expected_Pack_Set": expected_pack,
                "ERRORS": "; ".join(errors),
                "PRIORITY": priority,
            }
        )

    result_df = pd.DataFrame(results, columns=OUTPUT_COLUMNS)

    if result_df.empty:
        print("✅ WEIGHT: критичних помилок не знайдено")
        return result_df

    output_dir = Path(results_dir) / "Weight"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y.%m.%d_%H-%M-%S")
    output_file = (
        output_dir / f"Weight_{file_type}_{timestamp}.xlsx"
    )

    result_df.to_excel(output_file, index=False)

    print(f"⚖️ WEIGHT: знайдено {len(result_df):,} критичних помилок")
    print(f"📁 Результат: {output_file}")

    return result_df
