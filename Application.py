#!/usr/bin/python3
from DB import DB
from tabulate import tabulate
from simple_term_menu import TerminalMenu


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

    # --- SQL --- {{{
    def _execute_query(self, db: DB, query_path: str, params: dict):
        """Execute a query on a database.
        Inputs
        :param db: DB object to query
        :param query_path: relative path to .sql query
        :param params: dictionary containing paramaters for the query.
        
        Output
        :rows: resulting rows of the query

        Ex:
            contents of sql-file: SELECT * TrainRoute WHERE StartStation = :station;
            params: {"station" : "Bodø"}
        """
        
        with open(query_path, "r") as sql_file:
            query = sql_file.read()

        db.cursor.execute(query, params)
        return db.cursor.fetchall()

    # --- }}}
    # --- UI --- {{{
    def _linebreak(self) -> str:
        """Return a linebreak."""
        return "\n\n============================================\n"

    def _user_option_response(self, msg: str, options: list, **kwargs) -> str:
        """Get a users respons given a list of alternatives.
        Inputs
        :param msg: Message to user describing options
        :param options: list of options user can choose.

        :Keyword Arguments: passed directly to TerminalMenu.

        Output
        :out: one element in options
        Raises SystemExit if user wants to exit.
        """
        options += [None, "Exit to main menu"]

        terminal_menu = TerminalMenu(options, title=msg, **kwargs)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == len(options)-1:
            print("Exiting...")
            raise SystemExit
        return options[menu_entry_index]

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

    def _format_rows(self, rows) -> str:
        """Formats the rows of an returned sql-query into a nice table."""
        return tabulate(rows, tablefmt='rounded_outline')    
        
    # --- }}}

    # --- }}}

    # --- User functions --- {{{
    def view_train_routes(self, db: DB):
        """Let user get information of trainroutes"""

        # Get all stations
        db.cursor.execute("SELECT Name FROM RailwayStation")
        stations = [row[0] for row in db.cursor.fetchall()]

        # Get all weekdays
        db.cursor.execute("SELECT Name FROM WeekDay")
        weekdays= [row[0] for row in db.cursor.fetchall()]

        # Get user respons
        try:
            response_day = self._user_option_response("Select a weekday", weekdays)
            response_station = self._user_option_response("Select a station", stations)
        except SystemExit:
            return

        # Get table of rows that match the query
        table = self._format_rows(self._execute_query(
            db, 
            "queries/route_on_day.sql", 
            {"weekday" : response_day, "station" : response_station}
        ))
        print(table)



    def register_user(self, db: DB):
        """Let user register in the customer registry."""
        pass
        
    # --- }}}

if __name__=="__main__":
    app = App()
    # print(app._user_response(WeekDay))
    # print(app._user_varchar_response(4, 255))

    db = DB("test.db")
    app.view_train_routes(db)



