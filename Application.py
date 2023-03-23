#!/usr/bin/python3
# --- Imports --- {{{
from DB import DB

from tabulate import tabulate
from simple_term_menu import TerminalMenu
from os import system
import time
import numpy as np
# --- }}}

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
    def _clear_screen(self) -> str:
        """Clear output screan"""
        system("clear")

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
        options = list(map(str, options)).copy()
        options += [None, "Exit to main menu"]

        terminal_menu = TerminalMenu(options, title=msg, **kwargs)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == len(options)-1:
            print("Exiting...")
            raise SystemExit
        return options[menu_entry_index]

    def _user_varchar_response(self, msg: str, min_len: int, max_len: int) -> str:
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
            self._clear_screen()

            try:
                respons = str(input(msg))
            except EOFError:
                feedback = "Enter a value"
                continue
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

    def _user_int_response(self, msg: str, min_len, max_len) -> int:
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
                time.sleep(2)
            self._clear_screen()

            try:
                response = int(input(msg))
            except EOFError:
                feedback = "Enter a value"
                continue
            except ValueError:
                feedback = "Input an numeric value"
                continue
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

    def _format_rows(self, rows, **kwargs) -> str:
        """Formats the rows of an returned sql-query into a nice table."""
        return tabulate(rows, **kwargs)    
        
    def _format_chair_car(self, n_rows: int, seats_per_row: int, reserved_seats: list[int]) -> str:
        """Formats information about a car into a nice table.
        -- Inputs
        :param n_rows: number of rows in the carrige
        :param seats_per_row: number of seats per row in the car
        :parram reserved_seats: list of seats that are reserved (1-indexed)
        """
        n_seats = n_rows * seats_per_row
        if n_seats < max(reserved_seats):
            raise ValueError(f"Only {n_seats} available. Can not reserve seat {max(reserved_seats)}")

        seats = np.arange(1, n_seats+1).tolist()
        for i in reserved_seats:
            seats[i-1] = "🚫"
        seats = np.array([str(seats[i]) + "   " + str(seats[i+1]) for i in range(0, n_seats, 2)]).reshape(n_rows, int(seats_per_row/2))

        return self._format_rows(seats, tablefmt="rounded_grid")
        
    # --- }}}

# --- }}}

# --- User functions --- {{{
    # --- View train routes {{{
    def view_train_routes(self, db: DB):
        """Let user get information of trainroutes"""
        self._clear_screen()

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
        ), tablefmt="rounded_grid")
        print(table)

    # --- }}}
    # --- Register user {{{
    def register_user(self, db: DB) -> int:
        """Let user register in the customer registry."""
        self._clear_screen()

        name = self._user_varchar_response("Full name:", 0, 255)
        phone_no = self._user_int_response("Phone number", 0, 10)
        email = self._user_varchar_response("Email:", 0, 255)
        
        try:
            db.cursor.execute(
                "INSERT INTO Customer (Name, Email, PhoneNO) VALUES (:name, :phone_no, :email)",
                {"name": name, "phone_no": phone_no, "email": email}
            )
            db.con.commit()
        except Exception as e:
            print(e)
            return 1

        print("Successfully registered user!")
        return 0

    # --- }}}
    # --- Search routes between stops --- {{{
    def seach_betwean_stops(self, db):
        """Search trainroutes between two stops"""
        self._clear_screen()

        # Get all stations
        db.cursor.execute("SELECT Name FROM RailwayStation")
        stations = [row[0] for row in db.cursor.fetchall()]

        # Get user respons
        try:
            response_station_1 = self._user_option_response("Select a start", stations)
            stations.remove(response_station_1)
            response_station_2 = self._user_option_response("Select a destination station", stations)
        except SystemExit:
            return

        # Get table of rows that match the query
        table = self._format_rows(self._execute_query(
            db, 
            "queries/routes_between_stations.sql", 
            {"start_station" : response_station_1, "end_station" : response_station_2, "date_":"2023-04-03"}
        ))
        print(table)

    # --- }}}
    # --- Purchase ticket --- {{{
    def purachase_ticket(self, db: DB):
        """Let user purchase available tickets from desired train route."""
        # TODO create get available tickets query

        # Temporary:
        tickets = [1, 6, 8]
        n_rows = 3
        seats_per_row = 4

        car_overview = self._format_chair_car(n_rows, seats_per_row, tickets)
        options = np.delete(np.arange(1, n_rows*seats_per_row+1), np.array(tickets)-1).tolist()

        self._user_option_response(msg=car_overview, options=options, multi_select=True, show_multi_select_hint=True)








        # TODO create query to book seats (e.i.) insert into Ticket

        pass



    # --- }}}
        
# --- }}}

if __name__=="__main__":
    app = App()
    # print(app._user_response(WeekDay))
    # print(app._user_varchar_response(4, 255))

    db = DB("test.db")
    # app.view_train_routes(db)
    # app._clear_screen()
    # app.register_user(db)
    # app.seach_betwean_stops(db)
    app.purachase_ticket(db)



