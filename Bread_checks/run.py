
# 🚀 RUN — запуск перевірок
# Версія: 29.10.2026
# Виправлено: закриття Excel-файлів і підрахунок Weight

from pathlib import Path
from datetime import datetime
import io
import gc
from contextlib import redirect_stdout

import pandas as pd

from checks.flavor import check_flavor
from checks.non_compliant_characters import check_non_compliant_characters
from checks.brand_manufacturer import check_brand_manufacturer
from checks.retailer_manufacturer import check_retailer_manufacturer
from checks.extra_spaces import check_extra_spaces
from checks.conflicting_barcodes import check_conflicting_barcodes
from checks.weight import check_weight
from checks.columns_nil import check_columns_nil
from checks.error_statistics import create_error_statistics
from checks.validate_columns import validate_columns


CHECK_FUNCTIONS = {
    "flavor": check_flavor,
    "non_compliant_characters": check_non_compliant_characters,
    "brand_manufacturer": check_brand_manufacturer,
    "retailer_manufacturer": check_retailer_manufacturer,
    "extra_spaces": check_extra_spaces,
    "conflicting_barcodes": check_conflicting_barcodes,
    "weight": check_weight,
    "columns_nil": check_columns_nil,
}


def get_critical_weight_count(results_dir):
    """
    Підраховує CRITICAL тільки в найновішому звіті Weight,
    щоб не рахувати старі звіти повторно.
    """

    weight_dir = Path(results_dir) / "Weight"

    if not weight_dir.exists():
        return 0

    files = list(weight_dir.glob("*.xlsx"))

    if not files:
        return 0

    latest_file = max(
        files,
        key=lambda file: file.stat().st_mtime
    )

    try:
        with pd.ExcelFile(latest_file) as excel_file:
            df_weight = pd.read_excel(excel_file)

        if "PRIORITY" not in df_weight.columns:
            return 0

        count = (
            df_weight["PRIORITY"]
            .astype(str)
            .str.strip()
            .eq("CRITICAL")
            .sum()
        )

        return int(count)

    except Exception as exc:
        print(
            f"⚠️ Не вдалося прочитати звіт Weight "
            f"{latest_file.name}: {exc}"
        )
        return 0


def run_checks(file_name, checks, compare_file_name=None):
    BASE_DIR = Path(__file__).resolve().parent

    INPUT_DIR = BASE_DIR / "input"
    EXCEPTIONS_DIR = BASE_DIR / "exceptions"
    HISTORY_DIR = BASE_DIR / "history"

    for folder in (INPUT_DIR, EXCEPTIONS_DIR, HISTORY_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    file_path = INPUT_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"❌ Не знайдено файл: {file_path}"
        )

    compare_file_path = None

    if compare_file_name:
        compare_file_path = INPUT_DIR / compare_file_name

        if not compare_file_path.exists():
            raise FileNotFoundError(
                f"❌ Не знайдено файл для порівняння: "
                f"{compare_file_path}"
            )

    # 📋 Визначаємо тип файлу.
    # Контекстний менеджер гарантує закриття Excel-файлу.
    with pd.ExcelFile(file_path) as excel_file:
        sheet_names = excel_file.sheet_names

    if "IN_LIST" in sheet_names and "NOT_IN_LIST" not in sheet_names:
        file_type = "GUIDE"
        sheet_name = "IN_LIST"

    elif "NOT_IN_LIST" in sheet_names and "IN_LIST" not in sheet_names:
        file_type = "NOT_IN_LIST"
        sheet_name = "NOT_IN_LIST"

    else:
        raise ValueError(
            f"❌ Не вдалося однозначно визначити тип файлу: "
            f"{file_name}. "
            f"Знайдені аркуші: {sheet_names}. "
            "Очікується лише один аркуш: IN_LIST або NOT_IN_LIST."
        )

    run_type = "Guide" if file_type == "GUIDE" else "Not-in-list"

    run_name = f"{datetime.now():%Y-%m-%d_%H-%M}_{run_type}"

    RUN_DIR = HISTORY_DIR / run_name
    RESULTS_DIR = RUN_DIR / "RESULTS"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 📖 Читаємо вхідний файл.
    # pd.read_excel зазвичай сам закриває внутрішній файл.
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        dtype=str,
    )

    checks_to_run = [
        check for check in checks
        if check in CHECK_FUNCTIONS
    ]

    if not validate_columns(df, checks_to_run):
        del df
        gc.collect()

        raise ValueError(
            "❌ Запуск зупинено: структура Excel-файлу "
            "не відповідає вимогам."
        )

    print(f"🚀 Новий запуск: {run_name}")
    print(f"📂 Файл: {file_name}")
    print(f"📋 Тип файлу: {file_type}")
    print(f"📊 Рядків: {len(df):,}")

    if compare_file_path:
        print(f"🔎 Порівняння: {compare_file_name}")

    final_output = [
        f"🚀 Новий запуск: {run_name}",
        f"📂 Файл: {file_name}",
        f"📋 Тип файлу: {file_type}",
        f"📊 Рядків: {len(df):,}",
    ]

    if compare_file_path:
        final_output.append(
            f"🔎 Порівняння: {compare_file_name}"
        )

    # 🔎 Запускаємо перевірки по черзі.
    for check in checks:
        if check == "error_statistics":
            continue

        if check not in CHECK_FUNCTIONS:
            print(f"⚠️ Невідома перевірка: {check}")
            continue

        buffer = io.StringIO()

        with redirect_stdout(buffer):
            if check == "columns_nil":
                CHECK_FUNCTIONS[check](
                    df,
                    file_type,
                    EXCEPTIONS_DIR,
                    RESULTS_DIR,
                    compare_file_path,
                )
            else:
                CHECK_FUNCTIONS[check](
                    df,
                    file_type,
                    EXCEPTIONS_DIR,
                    RESULTS_DIR,
                )

        output = buffer.getvalue().strip()
        del buffer

        if output:
            print(output)

            for line in output.splitlines():
                if line.startswith((
                    "✅",
                    "⚠️",
                    "❌",
                    "⏭️",
                    "📁 Результат:",
                )):
                    final_output.append(line)

        del output

    # 📊 Статистика помилок.
    if "error_statistics" in checks:
        buffer = io.StringIO()

        with redirect_stdout(buffer):
            create_error_statistics(RESULTS_DIR)

        output = buffer.getvalue().strip()
        del buffer

        if output:
            print(output)

            for line in output.splitlines():
                if line.startswith((
                    "📊 ERROR STATISTICS:",
                    "📁 Результат:",
                )):
                    final_output.append(line)

        del output

    # ⚖️ Критичні помилки Weight.
    critical_weight = get_critical_weight_count(RESULTS_DIR)

    if critical_weight:
        message = (
            f"🔴 CRITICAL: {critical_weight} помилок у Weight"
        )

        print(message)
        final_output.append(message)

    # 📄 Зберігаємо фінальний вивід.
    final_output_file = RUN_DIR / "FINAL_OUTPUT.txt"

    final_output_file.write_text(
        "\n".join(final_output),
        encoding="utf-8",
    )

    print(
        f"📄 Фінальний вивід: "
        f"{final_output_file.relative_to(BASE_DIR)}"
    )

    # 🗑️ Видаляємо RESULTS, якщо вони порожні.
    if RESULTS_DIR.exists() and not any(
        path.is_file() for path in RESULTS_DIR.rglob("*")
    ):
        import shutil

        shutil.rmtree(RESULTS_DIR)

        print(f"🗑️ Видалено порожню папку: {RESULTS_DIR}")

    # 🧹 Звільняємо посилання на DataFrame та збираємо сміття.
    del df
    gc.collect()