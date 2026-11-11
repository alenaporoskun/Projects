# 🏪 RETAILER / MANUFACTURER — перевірка відповідності виробника рітейлеру ===
# Версія: 25.09.2026 20:50
# Опис: перевірка відповідності Retail_Net та Manufacturer з винятками

import pandas as pd
from pathlib import Path
from datetime import datetime


def check_retailer_manufacturer(
    df,
    file_type,
    exceptions_dir,
    results_dir
):
    # 📋 Файл винятків
    exceptions_file = (
        exceptions_dir
        / "EXCEPTIONS_Retailer_Manufacturer.xlsx"
    )

    if not exceptions_file.exists():
        raise FileNotFoundError(
            f"❌ Не знайдено: {exceptions_file}"
        )

    # 📖 Завантажуємо винятки
    exceptions_df = pd.read_excel(
        exceptions_file,
        sheet_name="ВИНЯТКИ_рітейлер",
        dtype=str
    ).fillna("")

    # 🔍 Формуємо набір винятків
    excluded_pairs = {
        (
            str(row["Manufacturer"]).strip().lower(),
            str(row["ID_SKU"]).strip().lower(),
            str(row["Retail_Net"]).strip().lower()
        )
        for _, row in exceptions_df.iterrows()
    }

    retailers = [
        "ATB",
        "Auchan",
        "EKO-Market",
        "Expansiya",
        "Fora",
        "METRO",
        "Novus",
        "Silpo",
        "Thrash",
        "Varus",
        "Velyka Kyshenya",
        "Kopiyka",
        "Tavriya"
    ]

    fozzy_retailers = {
        "expansiya",
        "fora",
        "silpo",
        "thrash"
    }

    def normalize(value):
        return str(value).strip().lower()

    results = []

    for _, row in df.iterrows():

        id_sku = normalize(row["ID_SKU"])
        retailer = normalize(row["Retail_Net"])
        manufacturer = normalize(row["Manufacturer"])

        # ⛔ Виняток
        if (
            manufacturer,
            id_sku,
            retailer
        ) in excluded_pairs:
            continue

        # 🏪 FOZZY GROUP
        if manufacturer == "fozzy group":

            if retailer not in fozzy_retailers:
                results.append({
                    "ID_SKU": row["ID_SKU"],
                    "Retail_Net": row["Retail_Net"],
                    "Manufacturer": row["Manufacturer"]
                })

            continue

        # 🔍 Інші рітейлери
        for other_retailer in retailers:

            other_retailer = normalize(
                other_retailer
            )

            if (
                other_retailer != retailer
                and other_retailer in manufacturer
            ):
                results.append({
                    "ID_SKU": row["ID_SKU"],
                    "Retail_Net": row["Retail_Net"],
                    "Manufacturer": row["Manufacturer"]
                })

                break

    # 📊 Результат
    if results:

        output_dir = (
            results_dir
            / "Retailer_Manufacturer"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_dir / (
            f"Retailer_Manufacturer_{file_type}_"
            f"{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ RETAILER / MANUFACTURER: "
            f"знайдено {len(results)} помилок"
        )

        print(
            f"📁 Результат: "
            f"{output_file.relative_to(Path(__file__).parents[1])}"
        )

    else:

        print(
            "✅ RETAILER / MANUFACTURER: "
            "невідповідностей не знайдено"
        )