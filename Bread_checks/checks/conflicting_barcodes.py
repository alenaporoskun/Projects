# 🔢 CONFLICTING BARCODES — перевірка конфліктів по штрихкоду =====
# Версія: 20.10.2026
# Опис: перевірка конфліктів даних для однакових штрихкодів

import pandas as pd
from pathlib import Path
from datetime import datetime

def check_conflicting_barcodes(df, file_type, exceptions_dir, results_dir):
    exceptions_file = exceptions_dir / "EXCEPTIONS_Conflicting_Barcodes.xlsx"

    if not exceptions_file.exists():
        raise FileNotFoundError(f"❌ Не знайдено: {exceptions_file}")

    excluded_barcodes = set(
        pd.read_excel(
            exceptions_file,
            sheet_name="ВИНЯТКИ_штрихкоди",
            dtype=str
        )["Barcode"].dropna().str.strip()
    )

    columns_to_check = [
        "Manufacturer", "Brand", "Category",
        "Class_1", "Class_2", "Class_3", "Class_4",
        "Subbrand", "Flavor", "Weight", "Pack_Set"
    ]

    df_barcode = df.assign(
        Barcode=df["ID_SKU"].str.extract(r"\b(\d{13})\b")[0]
    ).dropna(subset=["Barcode"])

    results = []

    for barcode, group in df_barcode.groupby("Barcode"):
        if barcode in excluded_barcodes:
            continue

        categories = group["Category"].fillna("").str.strip().str.lower()

        if (categories == "non").all():
            continue

        different = [
            column for column in columns_to_check
            if group[column].fillna("").str.strip().str.lower().nunique() > 1
        ]

        if different:
            results.append({
                "BAR_CODE": barcode,
                "DIFFERENT_COLUMNS": "; ".join(different)
            })

    if results:
        output_dir = results_dir / "Conflicting_Barcodes"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / (
            f"Conflicting_Barcodes_{file_type}_"
            f"{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(output_file, index=False)

        print(f"⚠️ CONFLICTING BARCODES: знайдено {len(results)} конфліктів")
        print(f"📁 Результат: {output_file.relative_to(Path(__file__).parents[1])}")

    else:
        print("✅ CONFLICTING BARCODES: конфліктів за штрихкодами не знайдено")