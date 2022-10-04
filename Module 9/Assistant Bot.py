USER_DATA = {
    "": "",
}

IS_WORKING = False

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

# decorator for input validation


def input_error(func):
    def inner(userData: tuple):
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
                response = func(userData)  # call decorated function
            except KeyError:
                response = "Error: cannot find this user."
            except ValueError:
                response = "Error: cannot handle phone number."
            except IndexError:
                response = "Error: dictionary index error."
            except:
                response = "Error: unclassified error occured."
        return response
    return inner


def hello_handler(*args):
    global USER_DATA
    global IS_WORKING
    USER_DATA.clear()
    IS_WORKING = True
    responseMessage = "How can I help you?"
    return responseMessage


def exit_handler(*args):
    global IS_WORKING
    IS_WORKING = False
    responseMessage = "Good bye!"
    return responseMessage


@input_error
def add_phone_handler(userData: tuple):
    global USER_DATA
    if userData[0] in USER_DATA.keys():
        responseMessage = f"Record for {userData[0]} already exists."
    else:
        USER_DATA[userData[0]] = userData[1]
        responseMessage = "Record was added.\n"
    return responseMessage


@input_error
def change_phone_handler(userData: tuple):
    global USER_DATA
    if userData[0] in USER_DATA.keys():
        USER_DATA[userData[0]] = userData[1]
    else:
        raise KeyError
    responseMessage = "Record was changed.\n"
    return responseMessage


@input_error
def show_phone_handler(userData: tuple):
    global USER_DATA
    userPhoneNumber = USER_DATA[userData[0]]
    responseMessage = f"Found {userData[0]}: {userPhoneNumber}"
    return responseMessage


@input_error
def show_all_phones_handler(userData: tuple):
    global USER_DATA
    i = 1
    responseMessage = "Current dictionary contains:\n"
    for key, value in USER_DATA.items():
        responseMessage += f"{i}. {key}: {value}\n"
        i += 1
    return responseMessage


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

# decorator for command validation

# TO-DO embed output to main()


def validate_input_command(func):
    def inner(command):
        result = func(command)  # call decorated function
        if result == None:
            print(f"The command does not exist.\n")
        else:
            if command in ("hello") and IS_WORKING:
                result = None
                print("Already working. Please enter an action command.\n")
            elif command in (
                "add", "change", "phone", "show all"
            ) and not IS_WORKING:
                result = None
                print(f"Cannot start work with action command '{command}'.\n")
        return result
    return inner


@validate_input_command
def get_command_handler(command: str):
    command = command.lower()
    commandHandler = None
    if len(COMMAND_HANDLER) > 0:
        commandHandler = COMMAND_HANDLER.get(command)
    return commandHandler

# parse user input


def parse_command_line(command_line: str) -> str:
    command = ""
    userPhoneNumber = ""
    userName = ""
    userData = []
    for registeredCommand in COMMAND:
        if command_line.startswith(registeredCommand):
            command = registeredCommand
            data = command_line.removeprefix(command).strip()
            if not (data == "" or data == None):
                data_components = data.split(" ")
                for dc in data_components:
                    if dc.isalpha():
                        userName += dc + " "
                userName = userName.strip()
                userPhoneNumber = data.removeprefix(userName).strip()
            break
    userData.append(userName)
    userData.append(userPhoneNumber)
    return (command, userData)


def main():
    commandHandler = None
    print("Hello! This is assistant bot. Here is what I can do:")
    for key, value in COMMAND.items():
        print("{:<15}{}".format(key, value))
    # awaiting for a command to start the bot or exit
    while commandHandler == None:
        inputCommand = str(
            input("Please enter a command to start work or exit:\n"))
        parsedCommand = parse_command_line(inputCommand)
        commandHandler = get_command_handler(parsedCommand[0])

    response = commandHandler()
    print(response)
    # work loop
    while IS_WORKING:
        inputCommand = str(input("Please enter an action command:\n"))
        # parse input, get a command and userData
        parsedCommand = parse_command_line(inputCommand)
        commandHandler = get_command_handler(parsedCommand[0])  # command
        if commandHandler != None:
            response = commandHandler(parsedCommand[1])  # userData
            print(response)
    return


if __name__ == "__main__":
    main()
