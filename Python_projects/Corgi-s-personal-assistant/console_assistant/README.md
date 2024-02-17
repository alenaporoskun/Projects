## Project name: Mr.Corgi's personal assistant

* A complete refactoring of the project code was done. 

* The personal assistant script was changed. 

* A file and folder structure was created for this purpose:

├── console_assistant  
│    ├── contacts  
│    │   ├── __init__.py  
│    │   ├── book_classes.py  
│    │   ├── contact_classes.py  
│    │   ├── fields.py  
│    │   ├── note_classes.py  
│    ├── data  
│    │   ├── address_book.pkl  
│    │   ├──notes.pkl  
│    ├── helpers  
│    │   ├── __init__.py  
│    │   ├── file_sorter.py  
│    │   ├── help.py  
│    │   ├── interface.py  
│    ├── output  
│    │   ├── __init__.py  
│    │   ├── print_table.py    
│    │  
│    └── __init__.py  
│    └── main.py  
│    └── README.md    
│    └── README_ua.md    


A personal assistant for Mr Corgi was developed. Mr Corgi is Santa Claus's assistant.   
Because Mr Corgi needs an app to help him with his duties.  
Mr Corgi:   
- Responsible for the book of gift recipients:
1. adds, 
2. edits, 
3. deletes, 
4. searches for people in it.
- Saves and monitors the list of gift recipients' wishes.
- It can tell which of them has a birthday in a few days.
- Sort files.
  
All commands of our personal assistant for Mr Corgi:  
  
- add-contact        - add a contact 
- edit-contact       - edit contact information
- delete-contact     - delete a contact
- delete-phone       - delete a phone number from a specific contact
- show-contacts      - show all contacts in the address book
- upcoming-birthdays - show a list of contacts whose birthday is in a certain number of days from the current date
- search-contact     - search for contacts in the address book
- add-note           - add a note with the author if it is in the contact book
- show-notes         - show all notes with authors and tags
- search-notes       - search for a note by word or author
- edit-note          - edit a note 
- delete-note        - delete a note
- sort-files         - sort files by folder 
- exit               - exit the Assistant
