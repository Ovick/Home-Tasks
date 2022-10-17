# decorator for input validation
from collections import UserDict


class Field():
    def __init__(self, isMandatory: bool) -> None:
        self.isMandatory = isMandatory


class Name(Field):
    def __init__(self, name: str, isMandatory: bool = True) -> None:
        super().__init__(isMandatory)
        self.value = name


class Phone(Field):
    def __init__(self, phoneNumber: str, isMandatory: bool = False) -> None:
        super().__init__(isMandatory)
        self.value = phoneNumber


class Record():

    NextFreeID = 1

    def __init__(self, userName: Name) -> None:
        self.ID = Record.NextFreeID
        Record.NextFreeID += 1
        self.userName = userName
        self.fields = []
        return

    def edit_user_name(self, userNameValue: str) -> None:
        self.userName.value = userNameValue
        return

    def find_field(self, fieldObj: Field) -> Field:
        fields = list(
            filter(lambda field: field == fieldObj, self.fields))
        return fields[0] if fields else None

    def add_field(self, fieldObj: Field) -> None:
        if self.find_field(fieldObj) is None:
            self.fields.append(fieldObj)
        return

    def delete_field(self, fieldObj: Field) -> None:
        if not self.find_field(fieldObj) is None:
            self.fields.remove(fieldObj)
        return

    def edit_field(self, oldFieldObj: Field, newFieldObj: Field) -> None:
        field = self.find_field(oldFieldObj)
        if not field is None:
            i = self.fields.index(field)
            self.fields[i] = newFieldObj
        return


class AddressBook(UserDict):

    def __init__(self, addressBookName: str) -> None:
        self.name = addressBookName
        self.recordsCount = 0
        self.data = dict()
        return

    def find_record(self, userName: str) -> Record:
        records = list()
        if self.recordsCount > 0:
            records = list(
                filter(lambda recordName: recordName == userName, self.data))
        # records[0] contains a key of found record, if any.
        return self.data[records[0]] if records else None

    def add_record(self, record: Record) -> None:
        userName = record.userName.value
        existingRecord = self.find_record(userName)
        if existingRecord is None:
            self.data[userName] = record
            self.recordsCount += 1
        return

    def delete_record(self, userName: str) -> None:
        if self.recordsCount > 0:
            existingRecord = self.find_record(userName)
            if not existingRecord is None:
                deletedRecord = self.data.pop(userName)
                self.recordsCount -= 1
        return


def input_error(func):
    def inner(userData: tuple, addressBook: AddressBook):
        response = ""
        if func.__name__ == "add_phone_handler" \
                or func.__name__ == "change_phone_handler":
            if userData[0] == "" or userData[1] == "":
                response = "Provide user name and phone number.\n"
        elif func.__name__ == "show_phone_handler":
            if userData[0] == "":  # name is empty
                response = "Provide user name.\n"
        if response == "":
            try:
                # call decorated function
                response = func(userData, addressBook)
            except KeyError:
                response = "Error: cannot find this user."
            except ValueError:
                response = "Error: cannot handle phone number."
            except IndexError:
                response = "Error: dictionary index error."
            except Exception as e:
                response = f"Error: {e.args[0]}"
        return response
    return inner


def hello_handler(isWorking: bool):
    if isWorking:
        responseMessage = "Already working. Please enter an action command.\n"
    else:
        responseMessage = "How can I help you?\n"
    return responseMessage


def exit_handler():
    responseMessage = "Good bye!"
    return responseMessage


@input_error
def add_phone_handler(userData: tuple, addressBook: AddressBook):
    userName = userData[0]
    phone = Phone(userData[1])
    record = addressBook.find_record(userName)
    if record is None:
        newRecord = Record(Name(userName))
        newRecord.add_field(phone)
        addressBook.add_record(newRecord)
        responseMessage = "Record was added.\n"
    else:
        pass
        # create an updated record
        record.add_field(phone)
        addressBook.data[userName] = record
        responseMessage = f"Record for {userName} was updated.\n"
    return responseMessage


@input_error
def change_phone_handler(userData: tuple, addressBook: AddressBook):
    userName = userData[0]
    phone = Phone(userData[1])
    record = addressBook.find_record(userName)
    if not record is None:
        currentValue = record.find_field(phone)
        if not currentValue is None:
            # logic of input should be changed as multiple numbers allowed
            # here current value should be replaced with new value, which needs to be added to userData
            record.edit_field(currentValue, currentValue)
        else:
            raise ValueError
    else:
        raise KeyError
    responseMessage = "Record  was changed.\n"
    return responseMessage


@input_error
def show_phone_handler(userData: tuple, addressBook: AddressBook):
    userName = userData[0]
    record = addressBook.find_record(userName)
    if not record is None:
        phones = [field.value for field in record.fields]
        responseMessage = f"Found {userName}: {', '.join(phones)}.\n"
    else:
        responseMessage = f"Not found: {userName}.\n"
    return responseMessage


@input_error
def show_all_phones_handler(userData: tuple, addressBook: AddressBook):
    if addressBook.recordsCount > 0:
        responseMessage = "Current address book contains:\n"
        for item in enumerate(addressBook.data.items(), 1):
            position = item[0]
            userName = item[1][0]
            phones = ", ".join([phone.value for phone in item[1][1].fields])
            responseMessage += f"{position}. {userName}: {phones}\n"
    else:
        responseMessage = "Current address book is empty.\n"
    return responseMessage


# decorator for command validation

def get_command_handler(command: str, COMMAND_HANDLER: dict):
    command = command.lower()
    commandHandler = None
    if COMMAND_HANDLER:
        commandHandler = COMMAND_HANDLER.get(command)
    return commandHandler

# parse user input


def parse_command_line(command_line: str, COMMAND: dict) -> str:
    command = ""
    userPhoneNumber = ""
    userName = ""
    userData = []
    for registeredCommand in COMMAND:
        if command_line.startswith(registeredCommand):
            command = registeredCommand
            data = command_line.removeprefix(command).strip()
            if data:
                data_components = data.split(" ")
                for component in data_components:
                    if component.isalpha():
                        userName += component + " "
                userName = userName.strip()
                userPhoneNumber = data.removeprefix(userName).strip()
            break
    userData.append(userName)
    userData.append(userPhoneNumber)
    return (command, userData)


def main():

    isWorking = False

    COMMAND = {
        "hello": "Start work with this bot",
        "add": "Add a phone number - add <user name> <phone number>",
        "change": "Change a phone number - change <user name> <phone number>",
        "phone": "Show user's phone number - phone <user name>",
        "show all": "Show all contacts",
        "good bye": "Finish work and exit",
        "close": "Finish work and exit",
        "exit": "Finish work and exit"
    }

    COMMAND_HANDLER = {
        "hello": hello_handler,
        "add": add_phone_handler,
        "change": change_phone_handler,
        "phone": show_phone_handler,
        "show all": show_all_phones_handler,
        "good bye": exit_handler,
        "close": exit_handler,
        "exit": exit_handler
    }

    commandHandler = None
    print("Hello! This is assistant bot. Here is what I can do:")
    for key, value in COMMAND.items():
        print("{:<15}{}".format(key, value))

    # awaiting for a command to start the bot or exit
    while not isWorking:
        inputCommand = str(
            input("Please enter a command to start work or exit:\n"))
        parsedCommand = parse_command_line(inputCommand, COMMAND)
        commandHandler = get_command_handler(parsedCommand[0], COMMAND_HANDLER)
        if not commandHandler is None:
            if commandHandler.__name__ == "hello_handler":
                response = commandHandler(isWorking)
                print(response)
                isWorking = True
                addressBook = AddressBook("General")
            elif commandHandler.__name__ == "exit_handler":
                response = commandHandler()
                print(response)
                break
            else:
                print(
                    f"Cannot start work with action command {parsedCommand[0]}.\n")
        else:
            print("The command does not exist.\n")
    # work loop
    while isWorking:
        inputCommand = str(input("Please enter an action command:\n"))
        # parse input, get a command and userData
        parsedCommand = parse_command_line(inputCommand, COMMAND)
        commandHandler = get_command_handler(
            parsedCommand[0], COMMAND_HANDLER)  # command
        if not commandHandler is None:
            if commandHandler.__name__ == "hello_handler":
                response = commandHandler(isWorking)
                print(response)
            elif commandHandler.__name__ == "exit_handler":
                response = commandHandler()
                print(response)
                isWorking = False
            else:
                response = commandHandler(
                    parsedCommand[1], addressBook)  # userData
                print(response)
        else:
            print(f"The command {parsedCommand[0]} does not exist.")
    return


if __name__ == "__main__":
    main()
