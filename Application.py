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

    def _user_response(self, alternatives: dict) -> int:
        """Get a users respons given a list of alternatives.
        """
        msg = f"Please choose an alternative (0-{len(alternatives)})\n"
        linebreak = "\n\n============================================\n"
        
        for key, val in alternatives.items():
            msg += f"  ({str(key)+')':<4}{val}\n"
        msg += "0: exit to menu.\n"
        msg += "~> "

        while True:
            try:
                response = int(input(msg))
            except ValueError:
                print(linebreak + "Please insert an integer.\n")
                continue                           
            else:                                  
                if response not in range(0, len(alternatives)):
                    print(linebreak + "Pease choose a valid option\n")
                    continue                       
                else:
                    # Valid input, break the loop
                    break
        return response
        

    # --- }}}

    # --- User functions --- {{{
    def view_train_routes(self, db: DB):
        """Let user get information of trainroutes"""
        response = self._user_response(WeekDay)
        
        pass
    # --- }}}

if __name__=="__main__":
    app = App()
    print(app._user_response(WeekDay))



