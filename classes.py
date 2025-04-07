from datetime import datetime, timedelta, date

from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)
        if  not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)
        try:
            self.value = self.string_to_date(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def string_to_date(self, value: str) -> date:
        """Перетворює дату у форматі 'DD.MM.YYYY' у об'єкт datetime.date."""
        return datetime.strptime(value, "%d.%m.%Y").date()

    def date_to_string(date_obj: date) -> str:
        """Перетворює дату у форматі datetime.date в рядок 'DD.MM.YYYY'."""
        return date_obj.strftime("%d.%m.%Y")

    def find_next_weekday(start_date: date, weekday: int) -> date:
        """Знаходить наступний вказаний день тижня."""
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(birthday: date) -> date:
        """Якщо день народження випадає на вихідний, переносимо на понеділок."""
        if birthday.weekday() >= 5:
            return Birthday.find_next_weekday(birthday, 0)  # Понеділок
        return birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, phone, new_phone):
        if self.find_phone(phone):
            self.add_phone(new_phone)
            self.remove_phone(phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item

    def __str__(self):
        if self.birthday is None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {Birthday.date_to_string(self.birthday.value)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        self.data.pop(name)

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = date.today()
        days = 7
        for name in self.data:
            birthday_this_year = self.data[name].birthday.value.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = Birthday.adjust_for_weekend(birthday_this_year)
                congratulation_date_str = Birthday.date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": name, "birthday": congratulation_date_str})
        return upcoming_birthdays
    
    def __str__(self):
        return '\n'.join(f'{self.data[item]}' for item in self.data)
    
