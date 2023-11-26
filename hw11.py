from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        # Додайте перевірку на коректність введення номера телефону
        if not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Некоректний номер телефону")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        # Додайте перевірку на коректність введення дня народження
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Некоректний формат дня народження")
        self._value = new_value

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, 
                                     datetime.strptime(self.birthday.value, '%Y-%m-%d').month,
                                     datetime.strptime(self.birthday.value, '%Y-%m-%d').day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, 
                                         datetime.strptime(self.birthday.value, '%Y-%m-%d').month,
                                         datetime.strptime(self.birthday.value, '%Y-%m-%d').day)
            days_left = (next_birthday - today).days
            return days_left
        return None

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def iterator(self, N):
        for i in range(0, len(self.records), N):
            yield self.records[i:i + N]

# Приклад використання
address_book = AddressBook()
record1 = Record("John Doe", "1234567890", "1990-01-01")
record2 = Record("Jane Doe", "9876543210", "1995-05-15")
address_book.add_record(record1)
address_book.add_record(record2)

for chunk in address_book.iterator(1):
    for record in chunk:
        print(f"Name: {record.name.value}, Phone: {record.phone.value}, Birthday: {record.birthday.value}, "
              f"Days to Birthday: {record.days_to_birthday()}")
