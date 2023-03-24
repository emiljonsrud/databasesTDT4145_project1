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

        db = DB("test.db")
        app._clear_screen()
        self._main_menu(db)

# --- Internal functions --- {{{
    def _main_menu(self, db: DB):
        """Show a menu for the user to selct a function.""" 

        functions = {
            "View train routes passing through a station on a weekday" : self.view_train_routes,
            "Register a new user" : self.register_user,
            "Search train routes between two stops" : self.seach_betwean_stops,
            "Purchase a ticket" : self.purachase_ticket
        }

        options = list(functions.keys())
        msg = "What would you like to do?"
        while True:
            try:
                user_response = self._user_option_response(msg, options)
            except SystemExit:
                try: 
                    exit = self._user_option_response("Are you sure you want to exit?", ["No", "Yes"])
                except SystemExit:
                    continue
                if exit:
                    return
                continue
            try:
                ret = self._format_rows(functions.get(options[user_response])(db), tablefmt = "rounded_grid")
                if ret:
                    self._user_option_response(ret, ["Back to main menu"])
            except SystemExit:
                continue

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

        # --- User response --- {{{
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

        terminal_menu = TerminalMenu(options, title=msg, **kwargs)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == None:
            raise SystemExit
        return menu_entry_index

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
    def _user_datetime_response(self):
        """Gets users response for date"""
        year = str(input("Enter a year (YYYY): "))
        month = str(input("Enter a month (MM): "))
        day = str(input("Enter a day (DD): "))
        hour = str(input("Enter an hour (HH): "))
        minute = str(input("Enter a minute (MM): "))
        
        return "-".join([year, month, day]), ":".join([hour, minute])

        # --- }}}
        # --- Formatters --- {{{
    def _format_rows(self, rows, **kwargs) -> str:
        """Formats the rows of an returned sql-query into a nice table."""
        return tabulate(rows, **kwargs)    
        
    def _format_car(self, n_compartments: int, n_rows: int, seats_per_row: int, reserved_seats: list[int]) -> str:
        """Formats information about a car into a nice table.
        -- Inputs
        :param n_compartments: number of compartments in the carrige (can be 0)
        :param n_rows: number of rows in the carrige (can be 0)
        :param seats_per_row: number of seats per row in the car (can be 0)
        :parram reserved_seats: list of seats that are reserved (1-indexed)
        """
        # Assert paramaters depending on car-type
        if n_compartments:
            seats_per_row = 2
            n_rows = n_compartments
            mid_seat = 0
        else:
            mid_seat = int(np.ceil(seats_per_row/2))
        n_seats = n_rows * seats_per_row

        # Verify validity of reserved_seats
        if n_seats < max(reserved_seats):
            raise ValueError(f"Only {n_seats} available. Can not reserve seat {max(reserved_seats)}")

        # Mark reseved seats
        seats = np.arange(1, n_seats+1).tolist()
        for i in reserved_seats:
            seats[i-1] = "🚫"

        # Divide into two columns
        formatted_seats = [[" " for _ in range(2)] for _ in range(n_rows)]
        for i in range(n_rows):
            curr_seat = i*seats_per_row

            left_col = [f"{seats[j]:>3}" for j in range(curr_seat, curr_seat+mid_seat)]
            right_col = [f"{seats[j]:>3}" for j in range(curr_seat+mid_seat, curr_seat+seats_per_row)]

            formatted_seats[i][0] = "".join(left_col)
            formatted_seats[i][1] = "".join(right_col)
        return self._format_rows(formatted_seats, tablefmt="rounded_grid", colalign=("center","center"))

    def _format_car_table(self, table):
        '''Formats a (CarID, CarNo, NumOfRows, SeatsPerRow, NumOfCompartments)
            table into a list of ["CarNo  CarType"].
        '''
        formatted_list = [""]*len(table)
        for i, row in enumerate(table):
            car_type = "Sleep car" if row[4] else "Chair car"
            formatted_list[i] = f"{row[1]:>2} {car_type}"
        return formatted_list

        # --- }}}
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
            response_day = weekdays[self._user_option_response("Select a weekday", weekdays, show_shortcut_hints=True)]
            response_station = stations[self._user_option_response("Select a station", stations, show_shortcut_hints=True)]
        except SystemExit:
            return None

        # Get table of rows that match the query
        table = self._execute_query(
            db, 
            "queries/route_on_day.sql", 
            {"weekday" : response_day, "station" : response_station}
        )
        return table

    # --- }}}
    # --- Register user {{{
    def register_user(self, db: DB) -> int:
        """Let user register in the customer registry."""
        self._clear_screen()

        try:
            name = self._user_varchar_response("Full name:", 0, 255)
            phone_no = self._user_int_response("Phone number", 0, 10)
            email = self._user_varchar_response("Email:", 0, 255)
        except SystemExit:
            return None
        
        try:
            db.cursor.execute(
                "INSERT INTO Customer (Name, Email, PhoneNO) VALUES (:name, :phone_no, :email)",
                {"name": name, "phone_no": phone_no, "email": email}
            )
            db.con.commit()
        except Exception as e:
            print(e)
            return None

        return [[f"Successfully registered user {name}!"]]

    # --- }}}
    # --- Search routes between stops --- {{{
    def seach_betwean_stops(self, db: DB, **kwargs):
        """Search trainroutes between two stops
        -- Keyword Arguments:
            * ret_station: bool (return start and stop stations)
        """
        self._clear_screen()

        # Get all stations
        db.cursor.execute("SELECT Name FROM RailwayStation")
        stations = [row[0] for row in db.cursor.fetchall()]

        # Get user respons
        while True:
            try:
                response_station_1 = stations[self._user_option_response("Select a start", stations)]
                stations.remove(response_station_1)
                try: 
                    response_station_2 = stations[self._user_option_response("Select a destination station", stations)]
                    try:
                        # date, time = self._user_datetime_response()
                        implemented_dates = ["2023-04-03", "2023-04-04"] #temporary
                        date = implemented_dates[self._user_option_response("Select a date", implemented_dates)] # temporary
                        break
                    except SystemExit:
                        continue # Exit datetime selection
                except SystemExit:
                    continue # Exit stop station selection
            except SystemExit:
                return None

        # Get table of rows that match the query
        table = self._execute_query(
            db, 
            "queries/routes_between_stations.sql", 
            {"start_station" : response_station_1, "end_station" : response_station_2, "date_": date}
        )
        if kwargs.get("ret_station"):
            return table, response_station_1, response_station_2
        else:
            return table

    # --- }}}
    # --- Purchase ticket --- {{{
    def purachase_ticket(self, db: DB):
        """Let user purchase available tickets from desired train route."""

        while True:
            try:
                # Select route 
                routes, start_station, end_station = self.seach_betwean_stops(db, ret_station=True)
                options = ["  ".join(route) for route in routes]
                route_name, route_time, route_date = routes[self._user_option_response("Select a desired route", options)]

                try: 
                    # Select car
                    cars = self._execute_query(db, "queries/get_cars.sql", {"train_route":route_name})
                    options = self._format_car_table(cars)
                    car = cars[self._user_option_response("Select a car. (Car number, Car type)", options)]


                    try:
                        # Select seat
                        car_id, car_no, n_rows, seats_per_row, n_compartments = car
                        if n_compartments:
                            n_rows = n_compartments
                            seats_per_row = 2

                        params = {
                            "run_date" : route_date,
                            "name_of_route" : route_name,
                            "car_id" : car_id,
                            "start_station" : start_station,
                            "end_station" : end_station
                        }
                        tickets = [ticket[0] for ticket in self._execute_query(db, "queries/get_taken_seats.sql", params)]

                        options = np.delete(np.arange(1, (2*n_rows)+1), np.array(tickets)-1).tolist()

                        car_overview = self._format_car(n_compartments, n_rows, seats_per_row, tickets)
                        user_booking = self._user_option_response(msg=car_overview, options=options, multi_select=True, show_multi_select_hint=True)

                    except SystemExit:
                        continue # Exit seat selection

                except SystemExit:
                    continue # Exit route selection

            except SystemExit:
                return None
            except TypeError:
                return None

        # TODO create query to book seats (e.i.) insert into Ticket
        return [["Successfully booked seat(s) {tickets}"]]


    # --- }}}
    # --- View customer orders --- {{{
    def view_customer_orders(self):
        """View custmer orders"""
        pass

    # --- }}}
        
# --- }}}

if __name__=="__main__":
    app = App()
    # print(app._user_response(WeekDay))
    # print(app._user_varchar_response(4, 255))

    db = DB("test.db")
    # app._clear_screen()
    # app.view_train_routes(db)
    # app.register_user(db)
    # app.seach_betwean_stops(db)
    # app.purachase_ticket(db)

    app.run()



