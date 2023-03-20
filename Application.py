#!/usr/bin/python3
from DB import DB

WeekDay = {
    "Monday"    : 0,
    "Tuesday"   : 1,
    "Wednesday" : 2,
    "Thursday"  : 3,
    "Friday"    : 4,
    "Saturday"  : 5,
    "Sunday"    : 6
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
        pass

    # --- }}}

    # --- User functions --- {{{
    def get_train_routes(self):
        """Let user get information of trainroutes"""
        pass
    # --- }}}


