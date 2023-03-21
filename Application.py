#!/usr/bin/python3
from DB import DB

WeekDay = {
    1 : "Monday",
    2 : "Tuesday",
    3 : "Wednesday",
    4 : "Thursday",
    5 : "Friday",
    6 : "Saturday",
    7 : "Sunday",
}

class App:
    def __init__(self):
        pass
    def run(self):
        """Start the application"""
        pass

    # --- Internal functions --- {{{
    def _menu(self):
        """List possible functions and let user choose.""" 
        pass

    def _linebreak(self) -> str:
        """Return a linebreak."""
        return "\n\n============================================\n"

    def _user_option_response(self, alternatives: dict) -> int:
        """Get a users respons given a list of alternatives.
        """
        msg = f"Please choose an alternative (0-{len(alternatives)})\n"
        
        for key, val in alternatives.items():
            msg += f"  ({str(key)+')':<4}{val}\n"
        msg += "0: exit to menu.\n"
        msg += "~> "

        while True:
            try:
                response = int(input(msg))
            except ValueError:
                print(self._linebreak() + "Please insert an integer.\n")
                continue                           
            if response not in range(0, len(alternatives)):
                print(self._linebreak() + f"{response} is not a valid option.\n")
                continue                       
            else:
                # Valid input, break the loop
                break
        return response

    def _user_varchar_response(self, max_len: int, min_len: int) -> str:
        """Get users respons for inputing a VARCHAR(255) value.

        -- Inputs
        :param max_len: maximum length of input.
        :param min_len: minimum length of inpu

        -- Out
        :response: string containing user response.
        """
        msg = "~> "

        while True:
            try:
                respons = str(input(msg))
            except EOFError:
                print(self._linebreak() + "Enter a value")
                continue
            if len(respons) > 255:
                print(self._linebreak() + "Too many characters. Try again.")
                continue
            elif len(respons) < 4: 
                print(self._linebreak() + "Too few characters. Try again.")
                continue
            else:
                # Valid input, break the loop
                break
        return respons
        

    # --- }}}

    # --- User functions --- {{{
    def view_train_routes(self, db: DB):
        """Let user get information of trainroutes"""
        response = self._user_option_response(WeekDay)

    def register_user(self, db: DB):
        """Let user register in the customer registry."""
        pass


        
        pass
    # --- }}}

if __name__=="__main__":
    app = App()
    # print(app._user_response(WeekDay))
    print(app._user_varchar_response())



