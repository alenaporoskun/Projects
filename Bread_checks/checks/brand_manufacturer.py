# 🏷️ BRAND / MANUFACTURER — перевірка брендів та виробників ==========================
# Версія: 20.10.2026
# Опис: перевірка відповідності Brand та Manufacturer

import pandas as pd
from pathlib import Path
from datetime import datetime

def check_brand_manufacturer(df, file_type, exceptions_dir, results_dir):

    exceptions_file = exceptions_dir / "EXCEPTIONS_Brand.xlsx"

    if not exceptions_file.exists():
        raise FileNotFoundError(
            f"❌ Не знайдено: {exceptions_file}"
        )

    def normalize(value):
        return str(value).strip().lower()

    excluded_brands = {
        normalize(value)
        for value in pd.read_excel(
            exceptions_file,
            sheet_name="ВИНЯТКИ_бренди",
            dtype=str
        )["Brand"]
        .dropna()
    }

    results = []

    grouped = (
        df[
            df["Brand"].notna()
            & df["Manufacturer"].notna()
        ]
        .groupby("Brand")["Manufacturer"]
        .agg(
            lambda x: {
                normalize(value)
                for value in x
            }
        )
    )

    for brand, manufacturers in grouped.items():

        brand = str(brand).strip()

        # ⛔ Бренди з винятків не перевіряємо
        if normalize(brand) in excluded_brands:
            continue

        if len(manufacturers) > 1:

            original_manufacturers = []

            for value in df.loc[
                df["Brand"].astype(str).str.strip() == brand,
                "Manufacturer"
            ]:
                value = str(value).strip()

                if normalize(value) not in [
                    normalize(v)
                    for v in original_manufacturers
                ]:
                    original_manufacturers.append(value)

            results.append({
                "Brand": brand,
                "Manufacturers": "; ".join(
                    sorted(original_manufacturers)
                )
            })

    if results:
        output_dir = results_dir / "Brand_manufacturer"
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_dir / (
            f"Brand_manufacturer_{file_type}_"
            f"{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ BRAND / MANUFACTURER: "
            f"знайдено {len(results)} невідповідностей"
        )
        print(
            f"📁 Результат: "
            f"{output_file.relative_to(Path(__file__).parents[1])}"
        )

    else:
        print(
            "✅ BRAND / MANUFACTURER: "
            "у кожного бренда один виробник"
        )