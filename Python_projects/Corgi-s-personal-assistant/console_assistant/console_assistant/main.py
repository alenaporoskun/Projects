from os import path
from os import makedirs

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from .helpers.help import Help
from .contacts.book_classses import PrintTable, LoadBook, SaveBook
from .contacts.contact_classes import AddContact, EditContact, DeleteContact
from .contacts.contact_classes import DeletePhone, UpcomingBirthdays
from .contacts.note_classes import AddNote, ShowNotes, SearchNotes
from .contacts.note_classes import EditNote, DeleteNote
from .helpers.file_sorter import SortFiles

# Отримуємо повний шлях до поточного робочого каталогу,
# де розташований цей скрипт
CURRENT_DIRECTORY = path.dirname(path.realpath(__file__))

# Побудуємо абсолютний шлях до файлу notes.pkl у підкаталозі 'data'
FILENAME_NOTES = path.join(CURRENT_DIRECTORY, 'data', 'notes.pkl')


def main() -> None:
    # Створення папки 'data'
    data_folder_path = path.join(CURRENT_DIRECTORY, 'data')
    makedirs(data_folder_path, exist_ok=True)

    # Завантаження адресної книги або створення нової
    #book = load_book()
    book = LoadBook.handle()

    print("Hi! I am Mr.Corgi's Personal Assistant. How can I help you?")

    # Список доступних команд
    commands = ['help', 'add-contact', 'show-contacts', 'edit-contact',
                'delete-contact', 'delete-phone', 'upcoming-birthdays', 
                'add-note', 'show-notes', 'search-contact', 'search-notes',
                'edit-note', 'delete-note', 'sort-files', 'exit']

    # Створення об'єкту WordCompleter, який використовується
    # для автодоповнення команд
    completer = WordCompleter(commands, ignore_case=True)

    # Запит на введення команди від користувача з можливістю автодоповнення
    command = prompt('Write a command (help - all commands): ',
                      completer=completer)

    choice = {
        'add-contact':        AddContact,
        'edit-contact':       EditContact,
        'delete-contact':     DeleteContact,
        'delete-phone':       DeletePhone,
        'upcoming-birthdays': UpcomingBirthdays,
        'add-note':           AddNote,
        'show-notes':         ShowNotes,
        'search-notes':       SearchNotes, 
        'edit-note':          EditNote,
        'delete-note':        DeleteNote
    }

    choice2 = {
        'help':           lambda: Help().handle_console(),
        'show-contacts':  lambda: PrintTable.handle_console(book, "Book of gift recipients"),
        'search-contact': lambda: book.search_contact(),
        'sort-files':     lambda: SortFiles.handle()
    }

    while command != 'exit':
        if command in choice.keys():
            choice[command].handle(book)
        elif command in choice2.keys():
            choice2[command]()
        else:
            print("The command was not found. Please enter another command.")

        command = prompt('Write a command (help - all commands): ',
                      completer=completer)

        # Збереження книги
        SaveBook.handle(book)

if __name__ == "__main__":
    main()