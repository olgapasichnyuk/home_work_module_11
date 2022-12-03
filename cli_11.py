from collections import UserDict
from datetime import datetime


class IncorrectFormatBirthday(Exception):
    pass


class IncorrectFormatPhone(Exception):
    pass


class Field:
    pass


class Name(Field):

    def __init__(self, value: str):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if 10 <= len(value) <= 13 and value.isnumeric():
            self.__value = value
        else:
            raise IncorrectFormatPhone


class Birthday(Field):
    def __init__(self, value: str):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            if datetime.strptime(value, '%d-%m-%Y'):
                self.__value = value
        except ValueError:
            raise IncorrectFormatPhone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if Phone(phone):
            self.phones.append(Phone(phone))
            return True

    def change_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                self.add_phone(new_phone_number)
                self.phones.remove(phone)
                return True

    def delete_phone(self, delete_number):
        for phone in self.phones:
            if phone.value == delete_number:
                self.phones.remove(phone)
                return True

    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
            return True

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday_day = int(self.birthday.value.split('.')[0])
        birthday_month = int(self.birthday.value.split('.')[1])

        closest_birthday = datetime(year=today.year,
                                    month=birthday_month,
                                    day=birthday_day).date()

        if today > closest_birthday:
            closest_birthday = datetime(year=today.year + 1,
                                        month=birthday_month,
                                        day=birthday_day).date()

        delta = closest_birthday - today

        return delta.days


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, N=3):
        i = 0
        if len(list(self.items())) < N:
            while i < len(list(self.items())):
                yield list(self.items())[i]
                i += 1
        else:
            while i < N:
                yield list(self.items())[i]
                i += 1


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'There is no phone with that name, please enter valid name.'
        except IncorrectFormatBirthday:
            return 'Wrong format of birthday, put data in format "dd-mm-yyyy"'
        except IncorrectFormatPhone:
            return 'Wrong format of the phone number, the phone number can contain only digits, valid length 10-13 ' \
                   'characters '
        except IndexError:
            return 'Input please name and phone after the command "change" or "add"\nor name after the command "phone"'

    return inner


def exit_func():
    return 'Good bye!'


def start():
    return 'How can I help you?'


@input_error
def add_contact(name, phone):
    if address_book.data.get(name):
        return 'Contact already exist'

    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return 'The contact was added'


@input_error
def add_phone(name, phone):
    if address_book.data.get(name):
        record = address_book.data[name]
        is_success = record.add_phone(phone)

        if not is_success:
            return 'Wrong forman of phone number'
        return f'Phone number {phone} was added to contact with name {name}'
    else:
        return f'Contact with name {name} does not exist'


@input_error
def add_birthday(name, birthday):
    if address_book.data.get(name):
        record = address_book.data[name]
        if record.birthday:
            return f'Contact with name {name} already contain field Birthday'

        is_success = record.add_birthday(birthday)

        if is_success:

            return f'Field Birthday with value {birthday} was added to contact with name {name}'
        else:
            return 'You input  birthday in wrong format. The correct format is "dd-mm-yyyy"'

    else:
        return f'Contact with name {name} does not exist'


@input_error
def change(name, phone):
    new_phone = input('Input the new phone number: ')
    record = address_book.data[name]

    if record.change_phone(phone, new_phone) is True:
        return f'Phone number for contact with name {name}  was changed to {new_phone}'
    else:
        return 'Phone number does not exist'


@input_error
def delete_phone(name, phone):
    record = address_book.data[name]

    if record.delete_phone(phone) is True:
        return f'The contact with name {name} and phone {phone} was deleted'
    else:
        return 'Phone number does not exist'


@input_error
def show_phone(name):
    if name in address_book.data.keys():
        phones_list = []
        for phone in address_book.data[name].phones:
            phones_list.append(phone.value)
        return phones_list
    else:
        return f'The contacts book does not contain contact with name {name}'


def show_all():
    if not address_book.data:
        return 'Your contacts book is empty.'

    contacts = ''
    for name, record in address_book.items():
        phones = []
        for phone in record.phones:
            phones.append(phone.value)
        contacts += f'{name} | phones: {phones}\n'
    return contacts


def show_chunk(chunk=3):
    if not address_book.data:
        return 'Your contacts book is empty.'

    result = ''
    for name, record in address_book.iterator(int(chunk)):
        phones_list = []
        for phone in record.phones:
            phones_list.append(phone.value)

        if record.birthday:
            result += f'{name} | phones: {phones_list} | birthday: {record.birthday.value}\n'
        else:
            result += f'{name} | phones: {phones_list}\n'

    return result


def main():
    handler = {
        'hello': start,
        'show all': show_all,
        'show_participate': show_chunk,
        'add': add_contact,
        'add_phone': add_phone,
        'change': change,
        'phone': show_phone,
        'delete': delete_phone,
        'add_birthday': add_birthday,

    }

    while True:
        user_input = input('Input the command').lower()
        parsed_input = user_input.split(' ')
        command = parsed_input[0]
        args_list = parsed_input[1:]

        if user_input in ['exit', 'close', 'good bye']:
            print(exit())
            break

        if user_input in handler.keys():
            msg = handler[user_input]()
            print(msg)
            continue

        elif handler.get(command):
            msg = handler[command](*args_list)
            print(msg)
            continue
        else:
            print('I do not understand the command')
            continue


if __name__ == '__main__':
    address_book = AddressBook()
    main()
