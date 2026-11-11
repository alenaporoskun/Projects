# 🔤 NON-COMPLIANT CHARACTERS — перевірка на непідходящі символи
# Версія: 20.10.2026
# Опис: перевірка на непідходящі символи у визначених полях
# Винятки: порівняння значень без урахування регістру

import pandas as pd
from pathlib import Path
from datetime import datetime


def check_non_compliant_characters(df, file_type, exceptions_dir, results_dir):
    exceptions_file = exceptions_dir / "EXCEPTIONS_Non_compliant_characters.xlsx"

    if not exceptions_file.exists():
        raise FileNotFoundError(f"❌ Не знайдено: {exceptions_file}")

    # Завантаження винятків
    exceptions_df = pd.read_excel(
        exceptions_file,
        sheet_name="ВИНЯТКИ_символи",
        dtype=str
    ).fillna("")

    # Нормалізація: рядок, видалення пробілів по краях,
    # порівняння без урахування регістру
    def normalize(value):
        if pd.isna(value):
            return ""
        return str(value).strip().casefold()

    # Перевірка необхідних колонок у файлі винятків
    required_exception_columns = {"Column", "Value"}
    missing_exception_columns = (
        required_exception_columns - set(exceptions_df.columns)
    )

    if missing_exception_columns:
        raise ValueError(
            "❌ У файлі винятків відсутні колонки: "
            + ", ".join(sorted(missing_exception_columns))
        )

    # Створення набору винятків (Column, Value)
    excluded_values = {
        (normalize(row["Column"]), normalize(row["Value"]))
        for _, row in exceptions_df.iterrows()
        if normalize(row["Column"]) and normalize(row["Value"])
    }

    columns_to_check = [
        "Manufacturer",
        "Brand",
        "Subbrand",
        "Flavor"
    ]

    # Дозволені символи
    allowed_symbols = set(" ,.!?:;-<>&'()/№_")

    def has_non_compliant_chars(value):
        if not isinstance(value, str):
            return False

        for char in value:
            if (
                char in allowed_symbols
                or char.isdigit()
                or "A" <= char <= "Z"
                or "a" <= char <= "z"
                or "А" <= char <= "я"
                or char in "ЇїЄєІіҐґ"
            ):
                continue

            return True

        return False

    # Перевірка наявності необхідних колонок в основному DataFrame
    required_df_columns = {"ID_SKU", *columns_to_check}
    missing_df_columns = required_df_columns - set(df.columns)

    if missing_df_columns:
        raise ValueError(
            "❌ В основному DataFrame відсутні колонки: "
            + ", ".join(sorted(missing_df_columns))
        )

    results = []

    # Перевірка даних
    for column in columns_to_check:
        for _, row in df.iterrows():
            value = row[column]

            # Перевіряємо виняток за колонкою та повним значенням
            exception_key = (normalize(column), normalize(value))

            if exception_key in excluded_values:
                continue

            if has_non_compliant_chars(value):
                results.append({
                    "ID_SKU": row["ID_SKU"],
                    "COLUMN": column,
                    "VALUE": value
                })

    # Формування звіту
    if results:
        output_dir = results_dir / "Non_compliant_characters"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / (
            f"Non_compliant_characters_{file_type}_"
            f"{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ NON-COMPLIANT CHARACTERS: "
            f"знайдено {len(results)} помилок"
        )

        try:
            project_dir = Path(__file__).resolve().parents[1]
            print(
                f"📁 Результат: "
                f"{output_file.resolve().relative_to(project_dir)}"
            )
        except (NameError, ValueError):
            print(f"📁 Результат: {output_file.resolve()}")

    else:
        print(
            "✅ NON-COMPLIANT CHARACTERS: "
            "непідходящих символів не знайдено"
        )
