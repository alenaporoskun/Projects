# 📏 EXTRA SPACES — перевірка зайвих пробілів ==================
# Версія: 20.10.2026
# Опис: перевірка зайвих пробілів у визначених полях


import pandas as pd
from pathlib import Path
from datetime import datetime


def check_extra_spaces(df, file_type, exceptions_dir, results_dir):
    columns_to_check = [
        "Manufacturer",
        "Brand",
        "Category",
        "Class_1",
        "Class_2",
        "Class_3",
        "Class_4",
        "Subbrand",
        "Flavor",
        "Pack_Set"
    ]

    results = []

    for column in columns_to_check:
        mask = df[column].apply(
            lambda x: isinstance(x, str) and (
                x != x.strip() or "  " in x
            )
        )

        for _, row in df.loc[mask, ["ID_SKU"]].iterrows():
            results.append({
                "ID_SKU": row["ID_SKU"],
                "COLUMN": column
            })

    if results:
        output_dir = results_dir / "Extra_spaces"
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_dir / (
            f"Extra_spaces_{file_type}_{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ EXTRA SPACES: знайдено {len(results)} помилок"
        )
        print(
            f"📁 Результат: "
            f"{output_file.relative_to(Path(__file__).parents[1])}"
        )

    else:
        print(
            "✅ EXTRA SPACES: зайвих пробілів не знайдено"
        )