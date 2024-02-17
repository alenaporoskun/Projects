# HW_1

## Завдання 2

Ваш попередній додаток зараз працює в консольному режимі та взаємодіє з користувачем у вигляді команд в консолі. Додаток треба розвивати і найчастіше змінюваною частиною додатку зазвичай є інтерфейс користувача (поки що це консоль). Модифікуйте код вашого додатку, щоб подання інформації користувачу (виведення карток з контактами користувача, нотатками, сторінка з інформацією про доступні команди) було легко змінити. Для цього треба описати абстрактний базовий клас для користувальницьких уявлень та конкретні реалізації, які успадковують базовий клас та реалізують консольний інтерфейс.

## Назва проєкту: Mr.Corgi’s personal assistant

* Був зроблений повний рефакторинг коду проєкту. 

* Був змінений скрипт персонального помічника. 

* Для цього було створено структуру файлів та папок:

├── HW_1 
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


Був розроблений персональний помічник для містера Коргі. Містер Коргі - помічник Санта Клауса.   
Бо містер Коргі потребує програму, що допоможе з його обов’язками.  
Містер Коргі:   
- Відповідає за книгу отримувачів подарунків:
1. додає, 
2. редагує, 
3. видаляє, 
4. шукає людей в ній.
- Зберігає та слідкує за списком побажань отримувачів подарунків.
- Може сказати у кого з них день народження через декілька днів.
- Сортує файли.
  
Всі команди нашого особистого асистента для пана Коргі:  
  
- add-contact              - додати контакт 
- edit-contact             - відредагувати інформацію про контакт
- delete-contact           - видалити контакт
- delete-phone             - видалити телефон з деякого контакту
- show-contacts            - показати всі контакти в адресній книзі
- upcoming-birthdays       - показати список контактів, у яких день народження через певну кількість днів від поточної дати
- search-contact           - пошук контактів в адресній книзі
- add-note                 - додати нотатку з автором, якщо він є в контактній книзі
- show-notes               - показати всі нотатки з авторами та тегами
- search-notes             - пошук нотатки за словом або автором
- edit-note                - редагувати нотатку 
- delete-note              - видалити нотатку
- sort-files               - сортувати файли по папкам 
- exit                     - вийти з Помічника