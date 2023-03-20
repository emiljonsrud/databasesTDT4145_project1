#!/usr/bin/python3
from DB import DB

WeekDay = {
    "Monday"    : 1,
    "Tuesday"   : 2,
    "Wednesday" : 3,
    "Thursday"  : 4,
    "Friday"    : 5,
    "Saturday"  : 6,
    "Sunday"    : 7
}

class App:
    def __init__(self):
        pass
    def run(self):
        """Start the application"""
        pass

    # --- Internal functions --- {{{
    def __menu(self):
        """List possible functions and let user choose.""" 
        pass
    def __user_response(self, alternatives: dict) -> int:
        """Get a users respons given a list of alternatives.
        """
        msg = f"Please choose an alternative (0-{len(alternatives)})\n"
        
        for key, val in alternatives.items():
            msg += f"{val:>4}{key}\n"
        msg += "0: exit to menu.\n"
        msg += "~> "
        while True:
            try:
                response = int(input(msg))
            except ValueError:
                print("Please insert an integer.")
                continue
            else:
                if response not in range(0, len(alternatives)):
                    print("Pease choose a valid option")
                    continue
                else:
                    # Valid input, break the loop
                    break
        return response
        

    # --- }}}

    # --- User functions --- {{{
    def get_train_routes(self):
        """Let user get information of trainroutes"""
        pass
    # --- }}}


