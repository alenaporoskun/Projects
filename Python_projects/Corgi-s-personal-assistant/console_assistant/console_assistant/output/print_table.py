from rich.console import Console
from rich.table import Table

from console_assistant.helpers.interface import Interface
from console_assistant.contacts.fields import Birthday


class PrintTable(Interface):
    @staticmethod
    def handle_console(address_book, text_title: str) -> None:
        # Виведення у вигляді таблиці

        # Перевірка на порожню книгу
        if not address_book.data:
            print("The book of gift recipients is empty.")
            return 

        # Створення об'єкту Console
        console = Console()

        # Створення таблиці
        table = Table(title = text_title, show_header=True, header_style="bold magenta")
        table.title_align = "center"
        table.title_style = "bold yellow"

        # Додавання стовпців до таблиці
        table.add_column("Contact name", style="magenta", width=20, justify="center")
        table.add_column("Phones", style="cyan", width=40, justify="center")
        table.add_column("Birthday", style="green", width=20, justify="center")
        table.add_column("Address", style="yellow", width=40, justify="center")
        table.add_column("Email", style="red", width=40, justify="center")

        # Додавання даних до таблиці
        for name, record in address_book.data.items():
            table.add_row(
                str(record.name.value),
                "; ".join(str(phone) for phone in record.phones),
                record.birthday.formatted_value() if isinstance(record.birthday, Birthday) else "",
                str(record.address.value) if record.address else "",
                str(record.email.value) if record.email else "",
            )

        # Виведення таблиці
        console.print(table)
        print()
