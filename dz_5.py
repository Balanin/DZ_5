from collections import UserDict

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner

class Field:
    def __init__(self, value):
        self.value = value
    
class Name(Field):

    pass

class Phone(Field):
    pass

class Record:
    def __init__(self,name):
        self.name = Name(name)
        self.numbers =[]

    def add_phone(self,number):
        self.numbers.append(Phone(number))
       

    def phone_in_contact(self, number) -> bool:
        for num in self.numbers:
            if num.value == number:
                return True
        return False

    def del_phone(self, number):
        for num in self.numbers:
            if num.value == number:
                self.numbers.remove(num)
                

    def change_phones(self, number):
         for i in self.numbers:
            if i.value == number[0]:
                self.numbers.remove(i)
            self.add_phone(number[1])
    
    def get_info(self):
        phones_info = ''
        for phone in self.numbers:
            phones_info += f'{phone.value}, '
        return f'{self.name.value} : {phones_info[:-2]}'
    
    def __repr__(self):
        return f'{self.name}'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

USERS = AddressBook()

# +
@ error_handler
def add_user(data):
    name, *phones = data
    if name  in USERS:
         raise ValueError('This contact already exist.')
    record = Record(name)
    for phone  in phones:
        record.add_phone(phone)
    USERS.add_record(record)
   

    return f'User {name} added with number: {phone}'
# +
@ error_handler
def delete_contact(data):
    name, *phone = (data)
    if name not in USERS.data.keys():
        return f'Contact with name {name} not found!'
    else:
        USERS.remove_record(name)
        return f'Contact {name} has been deleted'

#+
@ error_handler
def delete_phone(data):
    name, *phone = (data)
    if name not in USERS.data.keys():
        return f'Contact with name {name} not found!'
    else:
        contact = USERS[name]
        contact.del_phone(*phone)
        return f'Number {phone} has been deleted from {name}'
#+
@ error_handler
def addd_phone(data):
    name, *phones = data
    if name  in USERS:
        record = Record(name)
        for phone  in phones:
            record.add_phone(phone)
        USERS.add_record(record)
        return f'User {name} changed the get new number: {phone}'

#+
@ error_handler
def change_phone(data):
    name, *phone = data
    record = USERS[name]
    record.change_phones(phone)
    return f'User {name} changed the phone, his new number: {phone[1]}'

# +
@ error_handler
def show_all(_):
    string = ''
    for key, record in USERS.get_all_record().items():
        string += f'{record.get_info()}\n'
    return(string)

@ error_handler
def show_phone(data):
    name = data[0]
    contact = USERS[name]
    return f'{contact.get_info()}'

def hello(_):
    return "How can I help you?"

def exit(_):
    return "Good bye!"

HANDLER = {
        
            "hello": hello,
            "good bye": exit,
            "close": exit,
            "exit": exit,
            "add contact": add_user,
            "add phone": addd_phone,   
            "delete": delete_contact,
            "del phone": delete_phone,
            "show all": show_all,
            "change": change_phone,   
            "phone": show_phone       
            
}

def parser(user_input):
    new_input = user_input
    data = ''
    for key in HANDLER:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            data = data.strip().split(' ')
            
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()


def reaction_func(reaction):
    return HANDLER.get(reaction, break_func)

def break_func():
    return 'Wrong enter.'


def main():
    while True:
        user_input = input('>>> ')
        result = parser(user_input)
        if  result == "good bye" or result =="close" or result == "exit":
            print("Good bye!")
            break
        print(result)

    
        
if __name__ == "__main__":
    
      main()
   