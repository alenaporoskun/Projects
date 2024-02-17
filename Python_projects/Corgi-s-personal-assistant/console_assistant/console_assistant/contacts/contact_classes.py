from datetime import datetime
from datetime import date
from datetime import timedelta

from console_assistant.contacts.book_classses import AddressBook
from console_assistant.contacts.fields import Record
from console_assistant.output.print_table import PrintTable


class AddContact:
    @staticmethod
    def handle(address_book) -> None:
        # Функція для додавання контакту в адресну книгу

        name_contact = input('Enter name of contact: ')
        if name_contact in address_book.data:
            print('Such a contact already exists.')
            return
        elif name_contact == "":
            print('Name cannot be empty.')
            return

        # Створюється новий запис (контакт) з ім'ям name
        record = Record(name_contact)

        # Додається створений запис в адресну книгу
        address_book.add_record(record)

        # Користувачу пропонується ввести телефон для контакту
        phone = input(f'Enter the phone of contact {name_contact} (10 digits) (c - close): ')

        # Ввод телефонів для контакту, можливо введення 'c' для закриття
        phones = []
        while phone != 'c':
            try:
                # Додає телефон до запису контакту
                if not phone in phones:
                    record.add_phone(phone)
                    phones.append(phone)
                else:
                    print('The phone is already in the phone list.')
                phone = input(f'Enter the phone of contact {name_contact} (10 digits) (c - close): ')
            except ValueError:
                # Обробка виключення, якщо введено некоректний телефон
                phone = input(f'Enter the phone (10 digits) (c - close): ')

        # Користувачу пропонується ввести день народження для контакту
        birthday = input(f'Enter the birthday of contact {name_contact} (Year-month-day) (c - close): ')

        # Ввод дня народження для контакту, можливо введення 'c' для закриття
        while birthday != 'c':
            try:
                # Встановлює день народження для запису контакту
                record.set_birthday(birthday)
                break
            except ValueError:
                # Обробка виключення, якщо введено некоректний формат дня народження
                birthday = input(f'Enter the birthday (Year-month-day) (c - close): ')

        # Користувачу пропонується ввести електронну пошту для контакту
        email = input(f'Enter the email address (c - close): ')

        # Ввод електронної пошти для контакту, можливо введення 'c' для закриття
        while email != 'c':
            try:
                # Додає електронну пошту до запису контакту
                record.add_email(email)
                break
            except ValueError:
                # Обробка виключення, якщо введено некоректний формат електронної пошти
                email = input('Enter a valid email (c - close): ')

        # Користувачу пропонується ввести адресу для контакту
        address = input(f'Enter the address of contact {name_contact} (c - close): ')

        # Якщо адреса не 'c', встановлює адресу для запису контакту
        if address != 'c':
            record.set_address(address)


class EditContact:
    @staticmethod
    def handle(address_book) -> None:


        contact_name = input('Write the name of contact in which you want to'\
                            ' change something: ')

        if contact_name in address_book.data:
            contact_edit = address_book.data[contact_name]
            print(f'Contact found')

            while True:
                edit = input('Enter what you want to edit(n - name, p - phone, ' \
                            'b - birthday, a - address, e - email) (c - close): ')

                if edit.lower() == 'c':
                    break 

                elif edit == 'n':
                    new_name = input('Enter the new name (c - close): ')
                    if new_name.lower() != 'c':
                        # Перевіряємо, чи нове ім’я вже існує в адресній книзі
                        if new_name in address_book.data:
                            print('A contact with that name already exists.')
                        elif new_name == "":
                            print('New name cannot be empty. Contact name not updated.')
                        else:
                            # Оновлюємо ім’я контакту в адресній книзі
                            address_book.update_contact_name(contact_name, new_name,
                                                        address_book.notes_manager)
                            print(f'Contact name update to {new_name}.')
                            contact_name = new_name
                    else:
                        print('Name not changed')

                elif edit == 'p':
                    new_phone = input("Enter new phone number (10 digits) (c - close): ")
                    while new_phone != 'c':
                        try:
                            if not (len(new_phone) == 10 and new_phone.isdigit()):
                                raise ValueError
                            len_phones = len(contact_edit.phones)
                            if  len_phones == 0:
                                contact_edit.add_phone(new_phone)
                            elif len_phones == 1:
                                while True:
                                    choice = input('Enter what you want (c - correct phone ' \
                                                f'{contact_edit.phones[0].value}, a - add a new phone): ')
                                    if choice == 'c':
                                        contact_edit.edit_phone(contact_edit.phones[0].value,
                                                                new_phone)
                                        break
                                    elif choice == 'a':
                                        contact_edit.add_phone(new_phone)
                                        break
                            else:
                                question_text = 'What phone number will we correct: '
                                for i in range(len_phones):
                                    question_text += str(i + 1) + ' - ' + contact_edit.phones[i].value + ', '
                                question_text += str(len_phones + 1) + ' - add a new phone: '
                                while True:
                                    number = input(question_text)
                                    if number.isdigit():
                                        number = int(number)
                                        if number > 0 and number < len_phones + 2:
                                            break
                                        else:
                                            print('Incorrect number.')
                                    else:
                                        print('Only numbers are required.')
                                if number > 0 and number <= len_phones:
                                    contact_edit.edit_phone(contact_edit.phones[number - 1].value, new_phone)
                                else:
                                    contact_edit.add_phone(new_phone)
                            new_phone = input("Enter new phone number (c - close): ")
                        except ValueError:
                            new_phone = input('Enter the valid phone (10 digits) (c - close): ')
                elif edit == 'b':
                    new_birthday = input('Enter new birthday (Year-month-day) (c - close): ')
                    while new_birthday != 'c':
                        try:
                            contact_edit.set_birthday(new_birthday)
                            break
                        except ValueError:
                            new_birthday = input('Enter the birthday (Year-month-day) (c - close): ')
                elif edit == 'a':
                    new_address = input('Enter new address (c - close): ')
                    if new_address != 'c':
                        contact_edit.set_address(new_address)
                elif edit == 'e':
                    new_email = input('Enter new email (c - close): ')
                    while new_email != 'c':
                        try:
                            if contact_edit.email:
                                contact_edit.edit_email(new_email)
                            else:
                                contact_edit.add_email(new_email)
                            break
                        except ValueError:
                            new_email = input('Enter a valid email (c - close): ')
                else:
                    print('Invalid comand.')
        else:
            print(f'Contact {contact_name} not found.')


class DeleteContact:
    @staticmethod
    def handle(address_book) -> None:
        # Видалення контакту з книги контактів
        contact_name = input('Enter the name of contact you want to delete: ')
        if contact_name in address_book.data:
            question = input('Are you sure you want to delete this contact' \
                            f' {contact_name}? (yes or no): ')
            if question == 'yes':
                del address_book.data[contact_name]
                print('Contact deleted')
            else:
                print('Deletion canceled')
        else:
            print(f'Contact with the name {contact_name} not found.')


class DeletePhone:
    @staticmethod
    def handle(address_book) ->None:
        # Видалення телефону якогось контакту
        contact_name = input('Enter the name of contact: ')
        if contact_name in address_book.data:
            contact_edit = address_book.data[contact_name]
            if len(contact_edit.phones) > 0:
                while len(contact_edit.phones) > 0:
                    phones = []
                    for i in range(len(contact_edit.phones)):
                        phones.append(contact_edit.phones[i].value)
                    del_phone = input('Enter phone number to delete (c - close): ')
                    if del_phone == 'c':
                        break
                    if del_phone in phones:
                        contact_edit.remove_phone(del_phone)
                        print('Phone number deleted.')
                    else:
                        print('Phone number not found.')
            else:
                print('There are no phone numbers to delete.')            
        else:
            print(f'Contact with the name {contact_name} not found.')


class UpcomingBirthdays:
    @staticmethod
    def handle(address_book) -> None:
        # Команда для виведення наближених днів народження
        days_count = input('Введіть кількість днів для перевірки найближчих днів народження: ')
        try:
            days_count = int(days_count)
            if days_count < 0:
                raise ValueError("Будь ласка, введіть не від'ємне число днів.")
        except ValueError:
            print("Невірний ввід. Будь ласка, введіть не від'ємне ціле число.")

        upcoming_birthdays = UpcomingBirthdays.get_upcoming_birthdays(address_book, days_count)
        if upcoming_birthdays:
            new_book = AddressBook()
            for contact in upcoming_birthdays:
                new_book.add_record(contact)
            PrintTable.handle_console(new_book, f'Найближчі дні народження протягом наступних {days_count} днів')
        else:
            print(f'Немає найближчих днів народження протягом наступних {days_count} днів.')

    @staticmethod
    def get_upcoming_birthdays(address_book: AddressBook, days_count: int) -> list:
        upcoming_birthdays = []    
        today = datetime.today().date()  # Використовуємо тільки дату          

        for record in address_book.data.values():
            if record.birthday and isinstance(record.birthday.value, date):
                next_birthday = datetime(today.year, record.birthday.value.month, record.birthday.value.day).date()

                # Перевірка, чи день народження вже минув у поточному році
                if today > next_birthday:
                    next_birthday = datetime(today.year + 1, record.birthday.value.month, record.birthday.value.day).date()
                else:
                    # Обчислення різниці в часі між сьогоднішньою датою і наступним днем народження
                    delta = next_birthday - today + timedelta(days=1)
                
                # Обчислення різниці в часі між сьогоднішньою датою і наступним днем народження
                delta = next_birthday - today
                
                # Перевірка, чи день народження відбудеться або вже відбувся впродовж зазначеної кількості днів
                if 0 <= delta.days <= days_count:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays