from rich.console import Console
from rich.table import Table

from pickle import dump
from pickle import load

from os import path

from console_assistant.helpers.interface import Interface

# Отримуємо повний шлях до поточного робочого каталогу,
# де розташований цей скрипт
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Виходимо на один рівень вище від поточного каталогу
PARENT_DIRECTORY = path.join(CURRENT_DIRECTORY, path.pardir)

# Побудуємо абсолютний шлях до файлу notes.pkl у підкаталозі 'data'
FILENAME_NOTES = path.join(PARENT_DIRECTORY, 'data', 'notes.pkl')

class Notes:
    def __init__(self, text: str, author: str, tags: list = None):
        self.text = text
        self.author = author
        self.tags = tags if tags is not None else []

    def __str__(self) -> str:
        tags_str = ', '.join(self.tags) if hasattr(self, 'tags') else ''
        return f"{self.text} (by {self.author}, Tags: {tags_str})"
    

class NotePrinter(Interface):
    @staticmethod
    def handle_console(notes) -> None:
        if notes:
            console = Console()
            table = Table(title="Wish list", show_header=True, header_style="bold magenta")
            table.title_align = "center"
            table.title_style = "bold yellow"
            table.add_column("Index", style="cyan", width=5, justify="center")
            table.add_column("Note", style="green")
            table.add_column("Author", style="blue")
            table.add_column("Tags", style="magenta")

            for i, note in enumerate(notes, start=1):
                # Перевірка, чи note має атрибут tags перед його використанням
                tags_str = ', '.join(note.tags) if hasattr(note, 'tags') else ''
                table.add_row(str(i), note.text, note.author, tags_str)

            console.print(table)
        else:
            print("No notes available.")


class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note_with_tags(self, author: str, text: str, tags: list) -> None:
        note = Notes(text, author, tags)
        self.notes.append(note)

    def print_notes(self) -> None:
        NotePrinter.handle_console(self.notes)

    def save_notes(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            dump(self.notes, file)

    def load_notes(self, filename: str) -> list:
        try:
            with open(filename, 'rb') as file:
                self.notes = load(file)
        except FileNotFoundError:
            self.notes = []

    def edit_note(self, index: int, new_text: str = None,
                        new_tags: list = None) -> None:
        # Редагує нотатку з вказаним індексом.
        # index: Індекс нотатки для редагування
        # new_text: Новий текст нотатки
        # new_tags: Нові теги нотатки
        
        if 1 <= index <= len(self.notes):
            note = self.notes[index - 1]
            note.text = new_text
            note.tags = new_tags
            print(f"Note {index} edited successfully.")
        else:
            print("Invalid note index.")

    def delete_note(self, index: int) -> None:
        if 1 <= index <= len(self.notes):
            deleted_note = self.notes.pop(index - 1)
            print(f"Note {index} deleted: {deleted_note}")
        else:
            print("Invalid note index.")

    def update_notes_author(self, old_author: str, new_author: str,
                                  filename: str):
        for note in self.notes:
            if note.author == old_author:
                note.author = new_author

        # Збереження оновленного нотатка у файл
        self.save_notes(filename)


class AddNote:
    @staticmethod
    def handle(address_book) -> None:
        # Додавання нотатки
        author = input('Enter an author of note (c - close): ')

        # Перевірка, чи користувач вибрав опцію закриття
        if author.lower() == 'c':
            return

        # Перевірка, чи автор існує в телефонній книзі
        if author not in address_book.data:
            print('The author is not found in the book of gift recipients.')
            return

        # Введення тексту нотатки та тегів
        while True:
            note_text = input('Enter your note (c - close): ')
            if note_text.lower() == 'c':
                break

            tags_input = input('Enter tags (comma-separated): ')
            tags = [tag.strip() for tag in tags_input.split(',')]
            
            # Додавання нотатки та тегів до менеджера нотаток
            address_book.notes_manager.add_note_with_tags(author, note_text, tags)
            print('Note added successfully!')

        # Збереження нотаток у файл
        address_book.notes_manager.save_notes(FILENAME_NOTES)


class ShowNotes:
    @staticmethod
    def handle(address_book) -> None:
        # Функція для відображення нотаток з файла

        # Завантажує нотатки з файлу в об'єкт notes_manager
        address_book.notes_manager.load_notes(FILENAME_NOTES)

        # Виводить всі нотатки за допомогою методу print_notes
        address_book.notes_manager.print_notes()


class SearchNotes:
    @staticmethod
    def handle(address_book) -> None:
        # Пошук нотатки за словами або автором
        search_term = input(
            'Enter search term (leave blank to show all notes): ').lower()

        # Завантаження нотатки з файлу в об'єкт notes_manager
        address_book.notes_manager.load_notes(FILENAME_NOTES)

        # Фільтрування нотаток за словом або автором
        filtered_notes = [note for note in address_book.notes_manager.notes if search_term in note.text.lower() 
                        or search_term in note.author.lower()]

        # Виведення знайдених нотаток
        if filtered_notes:
            console = Console()
            table = Table(title='Search results', show_header=True,
                        header_style='bold magenta')
            table.title_align = 'center'
            table.title_style = 'bold yellow'
            table.add_column('Index', style='cyan', width=5, justify='center')
            table.add_column('Note', style='green')
            table.add_column('Author', style='blue')

            for i, note in enumerate(filtered_notes, start=1):
                table.add_row(str(i), note.text, note.author)

            console.print(table)
        else:
            print(f"No notes found for the search term '{search_term}'.")


class EditNote:
    @staticmethod
    def handle(address_book) -> None:
        address_book.notes_manager.load_notes(FILENAME_NOTES)
        address_book.notes_manager.print_notes()
            
        try:
            index_to_edit = int(input('Enter the index of the note to edit (0 - cancel): '))
            if index_to_edit == 0:
                return  # Редагування скасовано
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return
            
        if 1 <= index_to_edit <= len(address_book.notes_manager.notes):
            new_text = input('Enter the new text for the note: ')
            new_tags_input = input("Enter new tags (comma-separated): ")
            new_tags = [tag.strip() for tag in new_tags_input.split(',')]
            address_book.notes_manager.edit_note(index_to_edit, new_text, new_tags)
            address_book.notes_manager.save_notes(FILENAME_NOTES)
                
        else:
            print("Invalid note index.")
    

class DeleteNote:
    @staticmethod    
    def handle(address_book) -> None:
        address_book.notes_manager.load_notes(FILENAME_NOTES)
        address_book.notes_manager.print_notes()
        index_to_delete = int(input('Enter the index of the note to delete (0 - cancel): '))

        if index_to_delete == 0:
            return  # Скасувати видалення
        
        address_book.notes_manager.delete_note(index_to_delete)
        address_book.notes_manager.save_notes(FILENAME_NOTES)
        print('Note deleted successfully!')
