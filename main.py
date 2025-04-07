import pyjokes

from com_parser import *
from classes import *
from init import init


def main():
    """
    Консольний бот-помічник, який розпізнає команди, що вводяться з клавіатури, та відповідає згідно із введеною командою.
    Він вміє зберігати, змінювати, видаляти та показувати збережені контакти, відповідні номери телефонів і дні народження.
    Показує випадковий жарт за відповідної команди з бібліотеки pyjokes.
    """
    book = AddressBook()
    commands = init()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
            
        elif command == "add":
            print(add_contact(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "joke":
            print(pyjokes.get_joke())

        elif command == 'phone':
            print(show_phone(args, book))

        elif command == 'delete':
            print(contact_delete(args, book))

        elif command == 'help':
            print(commands)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    init()
    main()
