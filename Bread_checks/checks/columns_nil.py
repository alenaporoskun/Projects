# 🔍 COLUMNS NIL — порівняння двох файлів NOT_IN_LIST
# Версія: 20.10.2026
# Ключ: O + P
# Порівняння: O:AG включно

import pandas as pd
from pathlib import Path
from datetime import datetime


def check_columns_nil(
    df,
    file_type,
    exceptions_dir,
    results_dir,
    compare_file_path=None
):
    # Перевіряємо тип основного файлу
    if file_type != "NOT_IN_LIST":
        print("⏭️ COLUMNS NIL: пропущено — файл не NOT_IN_LIST")
        return

    # Перевіряємо наявність файлу для порівняння
    if compare_file_path is None:
        print("⏭️ COLUMNS NIL: файл для порівняння не заданий")
        return

    compare_file_path = Path(compare_file_path)

    if not compare_file_path.exists():
        raise FileNotFoundError(
            f"❌ Файл для порівняння не знайдено: {compare_file_path}"
        )

    # Читаємо файл для порівняння
    compare_df = pd.read_excel(
        compare_file_path,
        sheet_name="NOT_IN_LIST",
        dtype=str
    ).fillna("")

    df = df.copy().fillna("")

    # Перевіряємо, що обидва файли містять колонки до AG
    if len(df.columns) < 33 or len(compare_df.columns) < 33:
        raise ValueError(
            "❌ Обидва файли повинні містити колонки щонайменше до AG"
        )

    # 🔑 Формуємо ключ O + P
    df["_KEY"] = (
        df.iloc[:, 14].astype(str).str.strip()
        + "||"
        + df.iloc[:, 15].astype(str).str.strip()
    )

    compare_df["_KEY"] = (
        compare_df.iloc[:, 14].astype(str).str.strip()
        + "||"
        + compare_df.iloc[:, 15].astype(str).str.strip()
    )

    results = []

    # ⚠️ Знаходимо дублікати ключів
    for data, error in [
        (df, "DUPLICATE_KEY_IN_MAIN_FILE"),
        (compare_df, "DUPLICATE_KEY_IN_COMPARE_FILE")
    ]:
        duplicates = data[data["_KEY"].duplicated(keep=False)]

        for _, row in duplicates.iterrows():
            results.append({
                "ERROR": error,
                "COLUMN_O": row.iloc[14],
                "COLUMN_P": row.iloc[15],
                "COLUMN": "",
                "FILE_VALUE": "",
                "COMPARE_VALUE": ""
            })

    # Дублікати виключаємо з подальшого порівняння
    main = (
        df[~df["_KEY"].duplicated(keep=False)]
        .set_index("_KEY")
    )

    compare = (
        compare_df[~compare_df["_KEY"].duplicated(keep=False)]
        .set_index("_KEY")
    )

    # ❌ Ключі, яких немає у файлі порівняння
    for key in main.index.difference(compare.index):
        row = main.loc[key]

        results.append({
            "ERROR": "KEY_NOT_FOUND_IN_COMPARE_FILE",
            "COLUMN_O": row.iloc[14],
            "COLUMN_P": row.iloc[15],
            "COLUMN": "",
            "FILE_VALUE": "",
            "COMPARE_VALUE": ""
        })

    # ❌ Ключі, яких немає в основному файлі
    for key in compare.index.difference(main.index):
        row = compare.loc[key]

        results.append({
            "ERROR": "KEY_NOT_FOUND_IN_MAIN_FILE",
            "COLUMN_O": row.iloc[14],
            "COLUMN_P": row.iloc[15],
            "COLUMN": "",
            "FILE_VALUE": "",
            "COMPARE_VALUE": ""
        })

    # 🔄 Порівнюємо колонки O:AG включно
    # Excel: O = 15, AG = 33
    # Python iloc: O = 14, AG = 32
    columns = [
        "O", "P", "Q", "R", "S", "T", "U", "V", "W",
        "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG"
    ]

    indexes = range(14, 33)

    # Порівнюємо лише унікальні ключі, присутні в обох файлах
    for key in main.index.intersection(compare.index):
        row1 = main.loc[key]
        row2 = compare.loc[key]

        for column, index in zip(columns, indexes):
            value1 = str(row1.iloc[index]).strip()
            value2 = str(row2.iloc[index]).strip()

            if value1 != value2:
                results.append({
                    "ERROR": "VALUE_MISMATCH",
                    "COLUMN_O": row1.iloc[14],
                    "COLUMN_P": row1.iloc[15],
                    "COLUMN": column,
                    "FILE_VALUE": value1,
                    "COMPARE_VALUE": value2
                })

    # 📁 Зберігаємо результати
    if results:
        output_dir = Path(results_dir) / "Columns_NIL"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / (
            f"Columns_NIL_{file_type}_{datetime.now():%Y.%m.%d_%H-%M-%S}.xlsx"
        )

        pd.DataFrame(results).to_excel(
            output_file,
            index=False
        )

        print(
            f"⚠️ COLUMNS NIL: знайдено {len(results)} невідповідностей"
        )
        print(f"📁 Результат: {output_file}")

    else:
        print("✅ COLUMNS NIL: розбіжностей не знайдено")