from .interface import Interface

class Help(Interface):
    @staticmethod
    def handle_console() -> None:
        # Друк команд
        print('''All commands:
        - add-contact         - add contact
        - edit-contact        - edit contact information
        - delete-contact      - delete contact
        - delete-phone        - delete phone from some contact
        - show-contacts       - display all contacts in the book
        - search-contact      - search for contacts in the book 
        - upcoming-birthdays  - display a list of contacts whose birthday is a specified number of days from the current date
        - add-note            - add note with author if he/she is in the book
        - show-notes          - show all notes with authors and tags
        - search-notes        - search for a note by word or author
        - edit-note           - editing a note
        - delete-note         - delete note
        - sort-files          - sort files in a directory
        - exit                - exit the Assistant
        ''')