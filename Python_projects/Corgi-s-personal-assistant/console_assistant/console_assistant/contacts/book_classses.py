from os import path
from os import makedirs

from collections import UserDict
from pickle import load, dump

from .fields import Record
from console_assistant.output.print_table import PrintTable
from .note_classes import NoteManager

# Отримуємо повний шлях до поточного робочого каталогу,
# де розташований цей скрипт
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Виходимо на один рівень вище від поточного каталогу
PARENT_DIRECTORY = path.join(CURRENT_DIRECTORY, path.pardir)

# Побудуємо абсолютний шлях до файлу address_book.pkl у підкаталозі 'data'
FILENAME_ADDRESS_BOOK = path.join(PARENT_DIRECTORY, 'data', 'address_book.pkl')

# Побудуємо абсолютний шлях до файлу notes.pkl у підкаталозі 'data'
FILENAME_NOTES = path.join(PARENT_DIRECTORY, 'data', 'notes.pkl')


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notes_manager = NoteManager()

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def add_note(self, text: str) -> None:
        self.notes_manager.add_note(text)

    def print_notes(self) -> None:
        self.notes_manager.print_notes()

    def find(self, name: str) -> str:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def update_contact_name(self, old_name: str, new_name: str,
                                  notes_manager: NoteManager) -> None:
        # Оновлення імені контакту

        # Перевірка, чи ім'я контакту існує в адресній книзі
        if old_name in self.data:
            # Вилучення запису за старим ім'ям
            record = self.data.pop(old_name)
            # Оновлення імені в самому об'єкті запису
            record.name.value = new_name
            # Додавання оновленого запису з новим іменем до адресної книги
            self.data[new_name] = record

            # Оновлення імені в нотатках
            notes_manager.update_notes_author(old_name, new_name, FILENAME_NOTES)
            
    def __iter__(self):
        return AddressBookIterator(self, items_per_page = 5)
    # items_per_page - кількість записів на сторінці

    def search_contact(self) -> None:
        # пошук контактів серед контактів книги
        search_query = input("Enter search term: ")
        results, suggestions = self.search(search_query)

        if results:
            new_book = AddressBook()
            for record in set(results):
                new_book.add_record(record)
            PrintTable.handle_console(new_book, "Search results")
        elif suggestions:
            print(f"Possible suggestions: {', '.join(suggestions)}")
        else:
            print(f"Contact '{search_query}' not found. Phone number, address, and email were also not found.")

    def search(self, query: str) -> (list, list):
        results = []
        suggestions = []

        try:
            int(query[0])
        except ValueError:
            query_lower = query.lower()
            for name, record in self.data.items():
                # Пошук за ім'ям, адресою та електронною поштою
                if (
                    query_lower in name.lower()
                    or (record.email and query_lower in record.email.value.lower())
                    or (record.address and query_lower in record.address.value.lower())
                ):
                    results.append(record)
                elif name.lower().startswith(query_lower):
                    # Додавання рекомендації, якщо збігається початок імені
                    suggestions.append(name)
            # Пошук за номером телефону
            for record in self.data.values():
                for phone in record.phones:
                    if query_lower in phone.value.lower():
                        results.append(record)

        else:
            # Пошук за номером телефону
            for name, record in self.data.items():
                for phone in record.phones:
                    if query.lower() in phone.value.lower():
                        results.append(record)

        return results, suggestions


class AddressBookIterator:
    def __init__(self, address_book: AddressBook, items_per_page: int):
        self.address_book = address_book
        self.items_per_page = items_per_page
        # Визначається поточна сторінка, починаючи з нуля (перша сторінка)
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self) -> list[Record]:
        # Метод обчислює індекс початку (start) і кінця (end) діапазону
        # записів, які повинні бути виведені на поточній сторінці. 
        # Наприклад, якщо items_per_page дорівнює 5, то на першій сторінці
        # будуть виводитися записи з індексами 0 до 4, 
        # на другій сторінці - з 5 до 9, і так далі.
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        records = list(self.address_book.data.values())[start:end]

        if not records:
            raise StopIteration

        self.current_page += 1
        return records


class LoadBook:
    @staticmethod
    def handle() -> AddressBook:
        # Завантаження адресної книги з файлу
        try:
            with open(FILENAME_ADDRESS_BOOK, 'rb') as file: 
                return load(file)
        except FileNotFoundError:
            return AddressBook()


class SaveBook:
    @staticmethod
    def handle(address_book: AddressBook) -> None:
        makedirs(path.dirname(FILENAME_ADDRESS_BOOK), exist_ok=True)
        # Збереження адресної книги у файл
        with open(FILENAME_ADDRESS_BOOK, 'wb') as file:
            dump(address_book, file)