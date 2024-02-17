from re import fullmatch
from re import IGNORECASE

from datetime import datetime

# Регулярний вираз для перевірки email
EMAIL_REGULAR = r"[a-z][a-z0-9_.]+[@][a-z.]+[.][a-z]{2,}"


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    # реалізація класу
    def __init__(self, value: str):
        self.value = value

    # getter
    @property
    def value(self) -> str:
        return self._value

    # setter
    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value


class Phone(Field):
    def __init__(self, value: str):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value: str) -> bool:
        return len(value) == 10 and value.isdigit()
    
    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)


class Email(Field):
    def __init__(self, value: str):
        if not self.is_valid_email(value):
            raise ValueError('Invalid email format')
        super().__init__(value)

    @staticmethod
    def is_valid_email(value: str) -> bool:
        return fullmatch(EMAIL_REGULAR, value, flags = IGNORECASE) is not None
    
    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        if not self.is_valid_email(new_value):
            raise ValueError('Invalid email format')
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self._value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid birthday date format. Use YYYY-MM-DD.")

    @property
    def value(self) -> str:
        return self._value

    def formatted_value(self) -> str:
        return self._value.strftime('%Y-%m-%d') if self._value else ""


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value)

    # getter
    @property
    def value(self) -> str:
        return self._value
    
    # setter
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None
        self.notes = []

    def add_phone(self, phone: str) -> None:
        phone = Phone(phone)
        self.phones.append(phone)
        
    def add_email(self, email: str) -> None:
        email = Email(email)
        self.email = email
            
    def edit_phone(self, old_phone: str = None, new_phone: str = None) -> None:
        # Редагування телефону
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        
        if not found:
            raise ValueError(f"Phone {old_phone} not found in the record")
    
    def edit_email(self, new_email: str) -> None:
        if not Email.is_valid_email(new_email):
            raise ValueError('Invalid email format')
        self.email.value = new_email

    def remove_phone(self, number: str) -> None:
        # Видалення телефону
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)

    def find_phone(self, number: str) -> str:
        # Знаходження телефону
        for phone in self.phones:
            if phone.value.lower() == number:
                return phone
        return None
        
    def set_birthday(self, birthday: str) -> None:
        # Передача дати народження об'єкту Birthday
        try:
            birthday_obj = Birthday(birthday)
            self.birthday = birthday_obj
        except ValueError as e:
            raise ValueError(f"Invalid birthday date format. {str(e)}")

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def days_to_birthday(self) -> int:
        # Знаходження кількості днів до дня народження
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
            delta = next_birthday - today
            return f'There are {delta.days} days left before the birthday.'
        else:
            return None

    def __str__(self) -> str:
        contact_info = f"Contact name: {self.name.value}"
        if self.phones:
            contact_info += f", phones: {'; '.join(p.value for p in self.phones)}"
        if self.email is not None:
            contact_info += f", email: {self.email.value}"
        if self.birthday:
            contact_info += f", birthday: {self.birthday.strftime('%Y-%m-%d')}"
        if self.address:
            contact_info += f", address: {self.address.value}"
        if self.notes:
            contact_info += f" \nNotes: \n "
            for i, note in enumerate(self.notes, start=1):
                contact_info += f"{i}.{note}\n"
        return contact_info