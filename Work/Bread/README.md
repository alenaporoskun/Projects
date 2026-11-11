# Bread Checks — Системний пайплайн перевірки та імпорту каталогу

Даний проєкт призначений для автоматизованого зчитування, валідації та завантаження реєстрів/каталогів у базу даних MS SQL Server.

---

## 🛠 Вимоги до середовища

* **Python:** 3.10+ (рекомендовано 3.12 / 3.13)
* **Системні драйвери:** [ODBC Driver 17 or 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) (необхідний для роботи `pyodbc`).

---

## 🚀 Встановлення та розгортання

1. **Клонування репозиторію:**
   ```bash
   git clone <repository_url>
   cd Bread_checks
   ```

2. **Створення та активація віртуального середовища:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Встановлення залежностей:**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ⚙️ Стек технологій та бібліотеки

Проєкт використовує такі ключові модулі:

* **`pandas` & `numpy`** — аналіз, перетворення та очищення даних.
* **`python-calamine`** — ультрашвидкий двигун (engine) для читання великих файлів Excel (`engine='calamine'`).
* **`openpyxl`** — резервний двигун для зчитування та збереження XLSX-структур.
* **`SQLAlchemy` & `pyodbc`** — створення з'єднання з MS SQL Server та виконання SQL-запитів/процедур.
* **`jupyter`** — середовище виконання ноутбуків для інтерактивного аналізу (`Bread_checks.ipynb`).

---

## 📓 Роботаз Jupyter Notebook

Після створення ядра відкрийте `Bread_checks.ipynb` та оберіть ядро **Python (Bread Checks)**.

---

## 🔍 Основний процес валідації

1. **Завантаження:** Читання вхідних даних Excel за допомогою `pandas` та `python-calamine`.
2. **Перевірка:** Валідація типів даних, обов'язкових полів та відсутності дублікатів.
3. **Імпорт:** Запис валідованих даних у таблиці SQL Server через `SQLAlchemy`.