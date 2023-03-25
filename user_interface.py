from simple_term_menu import TerminalMenu
from os import system
import time


def clear_screen() -> str:
    """Clear output screan"""
    system("clear")

# --- User response --- {{{
def option_response(msg: str, options: list, **kwargs) -> str:
    """Get a users respons given a list of alternatives.
    Inputs
    :param msg: Message to user describing options
    :param options: list of options user can choose.

    :Keyword Arguments: passed directly to TerminalMenu.

    Output
    :out: one element in options
    Raises SystemExit if user wants to exit.
    """
    options = list(map(str, options)).copy()

    terminal_menu = TerminalMenu(options, title=msg, **kwargs)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == None:
        raise SystemExit
    return menu_entry_index

def varchar_response(msg: str, min_len: int, max_len: int) -> str:
    """Get users respons for inputing a VARCHAR(255) value.

    -- Inputs
    :param max_len: maximum length of input.
    :param min_len: minimum length of inpu

    -- Out
    :response: string containing user response.
    """
    msg += "\n~> "
    feedback = ""

    while True:
        if feedback:
            print(feedback)
            feedback = ""
            time.sleep(2)
        clear_screen()

        try:
            respons = str(input(msg))
        except EOFError:
            feedback = "Enter a value"
            continue
        except KeyboardInterrupt:
            raise SystemExit
        if len(respons) > max_len:
            feedback = "Too many characters. Try again."
            continue
        elif len(respons) < min_len: 
            feedback  = "Too few characters. Try again."
            continue
        else:
            # Valid input, break the loop
            break
    return respons

def int_response(msg: str, min_len, max_len) -> int:
    """Get users respons for inputing an value.

    -- Inputs
    :param min_len: minimum length of inpu
    :param max_len: maximum length of input.

    -- Out
    :response: string containing user response.
    """
    msg += "\n~> "
    feedback = ""

    while True:
        if feedback:
            print(feedback)
            feedback = ""
            time.sleep(1.5)
        clear_screen()

        try:
            response = int(input(msg))
        except EOFError:
            feedback = "Enter a value"
            continue
        except ValueError:
            feedback = "Input an numeric value"
            continue
        except KeyboardInterrupt:
            raise SystemExit
        if len(str(response)) > max_len:
            feedback = "Too many numbers. Try again."
            continue
        elif len(str(response)) < min_len: 
            feedback = "Too few numbers. Try again."
            continue
        else:
            # Valid input, break the loop
            break
    return response
def datetime_response():
    """Gets users response for date"""
    year = str(input("Enter a year (YYYY): "))
    month = str(input("Enter a month (MM): "))
    day = str(input("Enter a day (DD): "))
    hour = str(input("Enter an hour (HH): "))
    minute = str(input("Enter a minute (MM): "))
    
    return "-".join([year, month, day]), ":".join([hour, minute])

