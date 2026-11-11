# 🍓 FLAVOR — перевірка порядку смаків ==========================
# Версія: 25.09.2026 19:04
# Опис: перевірка порядку смаків

import pandas as pd
from pathlib import Path
from datetime import datetime


def check_flavor(df, file_type, exceptions_dir, results_dir):
    exceptions_file = exceptions_dir / "EXCEPTIONS_Flavor_order.xlsx"

    if not exceptions_file.exists():
        raise FileNotFoundError(f"❌ Не знайдено: {exceptions_file}")

    excluded_flavors = set(
        pd.read_excel(
            exceptions_file,
            sheet_name="ВИНЯТКИ_смаки",
            dtype=str
        )["Flavor"]
        .dropna()
        .str.strip()
    )

    UA_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

    def flavor_key(text):
        return [
            UA_ALPHABET.index(char)
            for char in text.lower()
            if char in UA_ALPHABET
        ]

    results = []

    for flavor in df["Flavor"].dropna().astype(str).str.strip().unique():
        if flavor in excluded_flavors:
            continue

        parts = flavor.split("_")
        correct_flavor = "_".join(
            sorted(parts, key=flavor_key)
        )

        if flavor != correct_flavor:
            results.append({
                "CURRENT_FLAVOR": flavor,
                "CORRECT_FLAVOR": correct_flavor
            })

    if results:
        output_dir = results_dir / "Flavor_order"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / (
            f"Flavor_order_{file_type}_{datetime.now():%Y.%m.%d}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ FLAVOR: знайдено {len(results)} помилок у порядку смаків"
        )
        print(
            f"📁 Результат: "
            f"{output_file.relative_to(Path(__file__).parents[1])}"
        )

    else:
        print("✅ FLAVOR: порядок смаків правильний")