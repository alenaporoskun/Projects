# Перевірка наявності необхідних колонок

REQUIRED_COLUMNS = {
    "flavor": {"Flavor"},
    "non_compliant_characters": {
        "Manufacturer",
        "Brand",
        "Subbrand",
        "Flavor",
    },
    "brand_manufacturer": {"Brand", "Manufacturer"},
    "retailer_manufacturer": {
    "Retail_Net",
    "Manufacturer",
    "ID_SKU",
    },
    "extra_spaces": {
        "Manufacturer",
        "Brand",
        "Category",
        "Class_1",
        "Class_2",
        "Class_3",
        "Class_4",
        "Subbrand",
        "Flavor",
        "Pack_Set",
    },
    "conflicting_barcodes": {
        "ID_SKU",
        "Manufacturer",
        "Brand",
        "Category",
        "Class_1",
        "Class_2",
        "Class_3",
        "Class_4",
        "Subbrand",
        "Flavor",
        "Weight",
        "Pack_Set",
    },
    "weight": {"Weight", "Pack_Set"},
}


def validate_columns(df, checks):
    available = {str(column).strip() for column in df.columns}

    print("🔎 Перевірка колонок")

    missing_by_check = {}

    for check in checks:
        required = REQUIRED_COLUMNS.get(check)

        if required is None:
            continue

        missing = sorted(required - available)

        if missing:
            missing_by_check[check] = missing

    if missing_by_check:
        print("❌ Відсутні необхідні колонки:")

        for check, missing in missing_by_check.items():
            print(f"   • {check}: {', '.join(missing)}")

        print(f"📋 Знайдені колонки: {', '.join(map(str, df.columns))}")
        return False

    print("✅ Усі необхідні колонки наявні")
    return True