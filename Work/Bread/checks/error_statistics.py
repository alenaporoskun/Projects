# 📊 ERROR STATISTICS — статистика помилок
# Опис: формування загальної статистики помилок

from pathlib import Path
from datetime import datetime

import pandas as pd


def create_error_statistics(results_dir):
    results_dir = Path(results_dir)

    statistics = []

    for file in results_dir.rglob("*.xlsx"):
        # Не читаємо власний звіт статистики
        if file.name.startswith("Error_statistics_"):
            continue

        try:
            with pd.ExcelFile(file) as excel_file:
                df = pd.read_excel(excel_file)
        except Exception as exc:
            print(f"⚠️ Не вдалося прочитати {file.name}: {exc}")
            continue

        check_name = file.parent.name

        # --------------------------------------------------
        # WEIGHT — коди помилок з колонки ERRORS
        # --------------------------------------------------
        if "ERRORS" in df.columns:
            errors = (
                df["ERRORS"]
                .dropna()
                .astype(str)
                .str.split(";")
                .explode()
                .str.strip()
            )

            errors = errors[
                errors.ne("")
                & errors.str.lower().ne("nan")
            ]

            for error, count in errors.value_counts().items():
                statistics.append({
                    "CHECK": check_name,
                    "ERROR": error,
                    "COUNT": int(count),
                })

        # --------------------------------------------------
        # Інші перевірки — коди помилок з колонки ERROR
        # --------------------------------------------------
        elif "ERROR" in df.columns:
            errors = (
                df["ERROR"]
                .dropna()
                .astype(str)
                .str.split(";")
                .explode()
                .str.strip()
            )

            errors = errors[
                errors.ne("")
                & errors.str.lower().ne("nan")
            ]

            for error, count in errors.value_counts().items():
                statistics.append({
                    "CHECK": check_name,
                    "ERROR": error,
                    "COUNT": int(count),
                })

        # --------------------------------------------------
        # CONFLICTING BARCODES — кожен рядок є конфліктом
        # --------------------------------------------------
        elif (
            "BAR_CODE" in df.columns
            and "DIFFERENT_COLUMNS" in df.columns
        ):
            count = len(df)

            if count:
                statistics.append({
                    "CHECK": check_name,
                    "ERROR": "CONFLICTING_BARCODE",
                    "COUNT": count,
                })

        # Звіт без підтримуваного формату не рахуємо
        else:
            print(
                f"ℹ️ Пропущено {file.name}: "
                "не знайдено підтримуваних колонок помилок"
            )

    # ------------------------------------------------------
    # Якщо помилок не знайдено
    # ------------------------------------------------------
    if not statistics:
        print("✅ ERROR STATISTICS: помилок не знайдено")
        return

    statistics_df = pd.DataFrame(statistics)

    summary = (
        statistics_df
        .groupby("ERROR", as_index=False)["COUNT"]
        .sum()
        .sort_values("COUNT", ascending=False)
    )

    output_file = (
        results_dir
        / f"Error_statistics_{datetime.now():%Y.%m.%d}.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:
        statistics_df.to_excel(
            writer,
            sheet_name="BY_CHECK",
            index=False,
        )

        summary.to_excel(
            writer,
            sheet_name="SUMMARY",
            index=False,
        )

    print("📊 ERROR STATISTICS: статистику сформовано")
    print(f"📁 Результат: {output_file}")
