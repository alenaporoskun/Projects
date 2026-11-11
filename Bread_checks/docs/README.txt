BREAD CHECKS

Автоматизована система перевірки файлів Bread.

Керування запуском виконується через Bread_checks.ipynb.

СТРУКТУРА ПРОЄКТУ

Bread_checks/
|
|-- checks/
|   |-- flavor.py
|   |-- non_compliant_characters.py
|   |-- brand_manufacturer.py
|   |-- retailer_manufacturer.py
|   |-- extra_spaces.py
|   |-- conflicting_barcodes.py
|   |-- weight.py
|   |-- weight_utils.py
|   |-- columns_R_AJ.py
|   |-- error_statistics.py
|   |-- ERROR_PRIORITIES.py
|
|-- exceptions/
|   |-- EXCEPTIONS_Flavor_order.xlsx
|   |-- EXCEPTIONS_Non_compliant_characters.xlsx
|   |-- EXCEPTIONS_Brand_Name.xlsx
|   |-- EXCEPTIONS_Retailer_Manufacturer.xlsx
|   |-- EXCEPTIONS_Conflicting_Barcodes.xlsx
|
|-- input/              - файли для перевірки, не зберігаються в Git
|-- history/            - історія запусків та результати
|-- docs/               - документація
|-- Bread_checks.ipynb  - керування запуском
|-- run.py              - головний двигун
|-- requirements.txt    - залежності
|-- README.md
|-- .gitignore

PYTHON ТА ЗАЛЕЖНОСТІ

Проєкт використовує окреме Python-середовище .venv.

Основні бібліотеки:

pandas==2.3.1
openpyxl==3.1.5

Встановлення:

pip install -r requirements.txt

ЗАПУСК

Файл для перевірки потрібно покласти у:

input/

Підтримуються:

.xlsx - NOT_IN_LIST
.xlsm - GUIDE

Для GUIDE використовується аркуш IN_LIST.

Для NOT_IN_LIST використовується перший аркуш.

ВИБІР ФАЙЛУ

У Bread_checks.ipynb:

file_type = "NOT_IN_LIST"

Приклад:

file_type = "NOT_IN_LIST"

if file_type == "NOT_IN_LIST":
file_name = "NOT_IN_LIST_Bread_2026_09_23_OP_2.xlsx"
compare_file_name = "NOT_IN_LIST_Bread_2026_09_23.xlsx"

elif file_type == "GUIDE":
file_name = "Bread_Guide_Sku_2026_09_07_1_OP_4.xlsm"
compare_file_name = None

Для NOT_IN_LIST можна додатково вказати файл для порівняння.

ПЕРЕВІРКА ТИПУ ФАЙЛУ

NOT_IN_LIST:

* назва містить NOT_IN_LIST
* формат .xlsx

GUIDE:

* назва містить Guide
* формат .xlsm

При невідповідності запуск зупиняється.

CHECKS

У Notebook задається список:

CHECKS = [
"flavor",
"non_compliant_characters",
"brand_manufacturer",
"retailer_manufacturer",
"extra_spaces",
"columns_R_AJ",
"conflicting_barcodes",
"weight",
"error_statistics",
]

Можна запускати тільки потрібні перевірки.

ПЕРЕВІРКИ

1. FLAVOR

Перевіряє порядок значень у Flavor.

Exception:

exceptions/EXCEPTIONS_Flavor_order.xlsx

Аркуш:

ВИНЯТКИ_смаки

Регістр букв не впливає на сортування.

Результат:

history/<run>/RESULTS/Flavor_order/

2. NON-COMPLIANT CHARACTERS

Перевіряє недопустимі символи у:

Manufacturer
Brand_Name
Subbrand_Name
Flavor

Exception:

exceptions/EXCEPTIONS_Non_compliant_characters.xlsx

Аркуш:

ВИНЯТКИ_символи

Результат:

history/<run>/RESULTS/Non_compliant_characters/

3. BRAND / MANUFACTURER

Перевіряє, що один бренд не має декількох виробників.

Exception:

exceptions/EXCEPTIONS_Brand_Name.xlsx

Аркуш:

ВИНЯТКИ_бренди

Регістр букв не має значення.

Результат:

history/<run>/RESULTS/Brand_Manufacturer/

4. RETAILER / MANUFACTURER

Перевіряє відповідність виробника рітейлеру.

Exception:

exceptions/EXCEPTIONS_Retailer_Manufacturer.xlsx

Аркуш:

ВИНЯТКИ_рітейлер

Спеціальні правила:

FOZZY GROUP
Expansiya
Fora
Silpo
Thrash

Регістр букв не має значення.

Результат:

history/<run>/RESULTS/Retailer_Manufacturer/

5. EXTRA SPACES

Перевіряє зайві пробіли у:

Manufacturer
Brand_Name
Category
Class_1
Class_2
Class_3
Class_4
Subbrand_Name
Flavor
Package_Count

Перевіряються:

* пробіли на початку;
* пробіли в кінці;
* подвійні пробіли.

Результат:

history/<run>/RESULTS/Extra_spaces/

6. CONFLICTING BARCODES

Перевіряє конфлікти записів з однаковим Barcode.

Порівнюються:

Manufacturer
Brand_Name
Category
Class_1
Class_2
Class_3
Class_4
Subbrand_Name
Flavor
Weight
Package_Count

Exception:

exceptions/EXCEPTIONS_Conflicting_Barcodes.xlsx

Аркуш:

ВИНЯТКИ_штрихкоди

Регістр букв не має значення.

Результат:

history/<run>/RESULTS/Conflicting_Barcodes/

Barcode у файлі винятків рекомендується зберігати як Text, щоб 13-значні штрихкоди не змінювалися.

7. WEIGHT

Перевіряє Weight та пов'язані значення.

Запускається, якщо "weight" є у CHECKS.

Пріоритети з:

checks/ERROR_PRIORITIES.py

CRITICAL:

EMPTY_WEIGHT
WEIGHT_NOT_NUMBER
WEIGHT_OUT_OF_RANGE
WEIGHT_MISMATCH
PACKAGE_COUNT_MISMATCH

WARNING:

ID_SKU+ARTICLE_WEIGHT_DIFFERENT
ID_SKU+ARTICLE_PACKAGE_COUNT_DIFFERENT

INFO:

NO_WEIGHT_FOUND
WEIGHT_UNIT_IN_NAME

Результат:

history/<run>/RESULTS/Weight/

8. COLUMNS R:AJ

Працює тільки для NOT_IN_LIST.

Порівнює два NOT_IN_LIST.

Ключ:

R + S

Порівнюються:

T:AJ

Перевіряються:

* дублікати ключів;
* відсутні ключі;
* невідповідності T:AJ.

Регістр букв має значення.

Результат:

history/<run>/RESULTS/Columns_R_AJ/

9. ERROR STATISTICS

Формує загальну статистику помилок за результатами перевірок.

Запускається через:

"error_statistics"

Результат:

history/<run>/RESULTS/Error_statistics_YYYY.MM.DD.xlsx

HISTORY

Кожен запуск створює:

history/YYYY-MM-DD_HH-MM_Type/

Приклад:

history/
|
|-- 2026-09-26_00-16_Guide/
|   |-- RESULTS/
|   |-- FINAL_OUTPUT.txt
|
|-- 2026-09-26_00-04_Not-in-list/
|-- RESULTS/
|-- FINAL_OUTPUT.txt

RESULTS/ містить результати запущених перевірок.

FINAL_OUTPUT.txt містить:

* файл;
* тип файлу;
* кількість рядків;
* файл порівняння;
* статуси перевірок;
* шляхи до результатів;
* критичні помилки Weight.

EXCEPTIONS

Постійні файли винятків зберігаються тільки в:

exceptions/

Копії винятків у history/ не створюються.

INPUT

Робочі файли зберігаються в:

input/

Папка input/ виключена з Git.

ПРИНЦИП РОБОТИ

Bread_checks.ipynb
|
v
run.py
|
|-- flavor.py
|-- non_compliant_characters.py
|-- brand_manufacturer.py
|-- retailer_manufacturer.py
|-- extra_spaces.py
|-- columns_R_AJ.py
|-- conflicting_barcodes.py
|-- weight.py
|-- error_statistics.py
|
v
history/<run>/
|
|-- RESULTS/
|-- FINAL_OUTPUT.txt

ВІДПОВІДАЛЬНІСТЬ ФАЙЛІВ

Bread_checks.ipynb

Вибір файлу, типу, файлу порівняння та перевірок.

run.py

Завантаження файлу, запуск перевірок, створення History та FINAL_OUTPUT.txt.

checks/*.py

Логіка окремих перевірок.

exceptions/

Постійні винятки.

history/

Історія запусків і результати.

docs/

Документація.

requirements.txt

Версії Python-залежностей.

ДОДАВАННЯ НОВОЇ ПЕРЕВІРКИ

1. Створити .py у checks/.
2. Додати функцію.
3. Підключити її в run.py.
4. Додати до CHECK_FUNCTIONS.
5. Додати назву до CHECKS.
6. Визначити результат.
7. За потреби створити exception-файл.
8. Описати перевірку в README.md.

ОСНОВНИЙ ПРИНЦИП

одна перевірка
|
один .py файл
|
своя логіка
|
свої винятки
|
свій результат

Кожну перевірку можна змінювати або запускати незалежно від інших.
