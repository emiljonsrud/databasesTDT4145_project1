#!/usr/bin/python3
# --- Imports --- {{{
from DB import DB
from formatters import draw_car, format_car_options, tabulate
from user_interface import clear_screen, option_response, varchar_response, int_response, datetime_response

from datetime import datetime
from typing import Callable
import numpy as np
# --- }}}

class App:
    def __init__(self, db_name, **kwargs) -> None:
        """
        
        """
        self.functions = {
            "View train routes passing through a station on a weekday" : self.view_train_routes,
            "Register a new user" : self.register_user,
            "Search train routes between two stops" : self.seach_betwean_stops,
            "Purchase a ticket" : self.purachase_ticket,
            "View upcomming orders" : self.view_customer_orders
        }
        self.db = DB(db_name)
        self.clear_sets()

    def run(self) -> None:
        """Start the application"""
        self._main_menu()

# --- Internal functions --- {{{
    def _main_menu(self) -> None:
        """Show a menu for the user to selct a function.""" 

        options = list(self.functions.keys())
        msg = "What would you like to do?"
        while True:
            try:
                clear_screen()
                user_response = option_response(msg, options)
            except SystemExit:
                try: 
                    exit = option_response("Are you sure you want to exit?", ["No", "Yes"])
                except SystemExit: 
                    continue # Continue to fnc selection
                if exit: return # Exit menu
                else: continue # Continue to fnc selection
            try:
                ret = self.functions[options[user_response]]()
                if ret:
                    clear_screen()
                    option_response(tabulate(ret, headers="firstrow", tablefmt = "rounded_grid"), ["Back to main menu"]) # Give user time to view fnc output
            except SystemExit: continue # Continue to function selection

    def _execute_query(self, db: DB, query_path: str, params: dict) -> list[tuple]:
        """Execute a query on a database.
        Inputs
        :param db: DB object to query
        :param query_path: relative path to .sql query
        :param params: dictionary containing paramaters for the query.
        
        Output
        :table: resulting table of the query

        Ex:
            contents of sql-file: SELECT * TrainRoute WHERE StartStation = :station;
            params: {"station" : "Bodø"}
        """
        
        with open(query_path, "r") as sql_file:
            query = sql_file.read()

        db.cursor.execute(query, params)
        return db.cursor.fetchall()
    
    def _recursive_menu(self, i, selections: list[Callable]) -> None:
        """Recursivley enters menu selections. This is so that the user
            may return to previous selection if they wish.
        """
        if i == len(selections): return 
        try: 
            selections[i]()
        except SystemExit:
            if i == 0: raise SystemExit
            else: return self._recursive_menu(i-1, selections)
        return self._recursive_menu(i+1, selections)

# --- }}}


    # --- Getters --- {{{
    def get_station(self, msg: str) -> str:
        """Let user select a station from current stored stations"""
        if not self._stations: 
            raise RuntimeError("Update stations")
        return self._stations[option_response(msg, self._stations)]
    def get_weekday(self, msg: str) -> str:
        if not self._weekdays: raise RuntimeError("Update weekdays")
        return self._weekdays[option_response(msg, self._weekdays)]

    # --- }}}
    # --- Update internal lists --- {{{
    def update_stations(self) -> None:
        """Update the stored stations accoring to the db"""
        self.db.cursor.execute("SELECT Name FROM RailwayStation")
        self._stations = [row[0] for row in self.db.cursor.fetchall()]

    def update_weekdays(self) -> None:
        """Update the stored weekdays accoring to the db"""
        self.db.cursor.execute("SELECT Name FROM WeekDay")
        self._weekdays= [row[0] for row in self.db.cursor.fetchall()]

    def update_train_occurances(self) -> None:
        """Update stored train occurances that match the internal stored paramaters.
        Train occurances is stored as a list of tuples:
            (TR.Name , TOc.RunDate, RS1.Station, RS1.TimeOfDay, RS2.Station, RS2.TimeOfDay)
            RS1: start station, RS2: end station
        """
        if not (self._end_station and self._date and self._time):
            raise RuntimeError("Need to set date, time, start- and end station first")

        # Get table of train occurances that match the search paramaters
        params = {
            "start_station" : self._start_station,
            "end_station" : self._end_station,
            "date_": self._date,
            "time_": self._time
        }
        self._train_occurances = self._execute_query(
            self.db, 
            "queries/routes_between_stations.sql", 
            params
        )

    # --- }}}
    # --- Setters {{{
    def clear_sets(self):
        """Cleares all set values"""
        self._start_station = None
        self._end_station = None
        self._stations = None
        self._date = None
        self._time = None
        self._train_occurance = None
        self._train_occurances = None
        self._car = None
        self._seat_no = None
        self._customer_id = None

    def set_start_station(self):
        """Set the current selected start station"""
        self.update_stations()
        self._start_station = self.get_station("Select start")

        # # Also store the start-subsection no
        # self._start_sec_no = db.cursor.execute(
        #     "SELECT TSS.SubSectionNo FROM TrackSubSection AS TSS WHERE TSS.StartsAt = :start_station",
        #     {"start_station":start_station}
        # ).fetchall()[0][0]

    def set_end_station(self):
        """Set the current selection for end station"""
        if not (self._start_station and self._stations):
            raise RuntimeError("Select start station first")

        if self._start_station in self._stations:
            self._stations.remove(self._start_station) # cannot start and end at same station
        self._end_station = self.get_station("Select a destination station")

        # self._end_sec_no = db.cursor.execute(
        #     "SELECT TSS.SubSectionNo FROM TrackSubSection AS TSS WHERE TSS.StartsAt = :end_station",
        #     {"end_station":end_station}
        # ).fetchall()[0][0]

    def set_date(self):
        """Select current search date"""
        # self._date = datetime_response()[0]

        # Temporary, for ease of testing the application
        implemented_dates = ["2023-04-03", "2023-04-04"] #temporary
        self._date = implemented_dates[option_response("Select a date", implemented_dates)] # temporary
        clear_screen()

    def set_time(self):
        """Select current search time"""
        time_ = varchar_response("Please select a time (hhmm)", 4, 4)
        self._time = f"{time_[:2]}:{time_[2:]}"
        clear_screen()

    def set_train_occurance(self):
        """Set current selected train occurance. Need to have time, date, start-, end-station"""
        self.update_train_occurances()
        assert self._train_occurances
        options = ["  ".join(route) for route in self._train_occurances] # join train-occ info
        self._train_occurance = self._train_occurances[option_response("Select a desired route", options)]

    def set_car_no(self):
        """Sets current selected car. Stored as a tuple (values can be null):
            (car_id, car_no, n_rows, seats_per_row, n_compartments)
        """
        if not self._train_occurance:
            raise RuntimeError("Select a train occurance first")

        cars = self._execute_query(self.db, "queries/get_cars.sql", {"train_route":self._train_occurance[0]})
        options = format_car_options(cars)
        self._car = cars[option_response("Select a car. (Car number, Car type)", options)]

    def set_seat_no(self):
        """Sets current selected seat numbers. Stored as a list[int]"""
        if not self._car:
            raise RuntimeError("Select a car first")

        car_id, car_no, n_rows, seats_per_row, n_compartments = self._car
        assert self._train_occurance
        route_name = self._train_occurance[0]

        # Find reserved seats
        params = {
            "run_date" : self._date,
            "name_of_route" : route_name,
            "car_id" : car_id,
            "start_station": self._end_station, 
            "end_station": self._start_station
        }
        tickets = [ticket[0] for ticket in self._execute_query(self.db, "queries/get_taken_seats.sql", params)]

        # Check if sleep car
        if n_compartments:
            n_rows = n_compartments
            seats_per_row = 2
            # One bed reserves a whole coupe
            for ticket in tickets.copy():
                if ticket%2: tickets.append(ticket+1)
                else: tickets.append(ticket-1)

        # Get available seats
        options = np.arange(1, seats_per_row*n_rows+1)
        if len(tickets) > 0: 
            options = np.delete(options, np.array(tickets)-1).tolist() # remove reseved seats

        car_overview = draw_car(n_compartments, n_rows, seats_per_row, tickets) # visualization of car (str)
        user_choice_indeces = option_response(msg=car_overview, options=options, multi_select=True, show_multi_select_hint=True)
        self._seat_no = np.array(options)[np.array(user_choice_indeces)].tolist() #need numpy to slice list of indeces

    def set_customer_id(self):
        """Set the current workning customer id.
        This function has loads of room for improvement, but works 
        for the current objective. (To test SQL-knowledge)
        """
        self._customer_id = int_response("What is your custmer-id?", 0, 4)

    # }}}

    # --- View train routes {{{
    def view_train_routes(self):
        """Let user get information of trainroutes"""
        clear_screen()
        self.update_stations()
        self.update_weekdays()

        # Get user response
        params = {
            "weekday" : self.get_weekday("Select a weekday"),
            "station" : self.get_station("Select a railway station")
        }
        # Get table of rows that match the query
        table = self._execute_query(self.db, "queries/route_on_day.sql", params)
        return table

    # --- }}}
    # --- Register user {{{
    def register_user(self) -> list[tuple]:
        """Let user register in the customer registry."""
        clear_screen()

        name = varchar_response("Full name:", 0, 255)
        phone_no = int_response("Phone number", 0, 10)
        email = varchar_response("Email:", 0, 255)
        
        self.db.cursor.execute(
            "INSERT INTO Customer (Name, Email, PhoneNO) VALUES (:name, :phone_no, :email)",
            {"name": name, "phone_no": phone_no, "email": email}
        )
        self.db.con.commit()
        customer_id = self.db.cursor.execute("SELECT last_insert_rowid();").fetchall()[0][0]

        return [(f"Successfully registered user {name}! Customer id: {customer_id}",)]

    # --- }}}
    # --- Search routes between stops --- {{{
    def seach_betwean_stops(self, **kwargs) -> list[tuple] | tuple[list[tuple], str, str] | None:
        """Search trainroutes between two stops
        -- Keyword Arguments:
            * ret_station: bool (return start and stop stations)
        """
        clear_screen()
        selections = [
            self.set_start_station,
            self.set_end_station,
            self.set_date,
            self.set_time
        ]
        self._recursive_menu(0, selections)
                
        # Get table of rows that match the query
        params = {
            "start_station" : self._start_station,
            "end_station" : self._end_station,
            "date_" : self._date,
            "time_" : self._time
        }
        table = self._execute_query(self.db, "queries/routes_between_stations.sql", params)
        self.clear_sets()

        headers = ("Route", "Date", "Start", "Departure", "End", "Arrival")
        table.insert(0, headers)
        return table

    # --- }}}
    # --- Purchase ticket --- {{{
    def purachase_ticket(self) -> list[tuple]:
        """Let user purchase available tickets from desired train route."""
        clear_screen()
        selections = [
            self.set_start_station,
            self.set_end_station,
            self.set_date,
            self.set_time,
            self.set_train_occurance,
            self.set_car_no,
            self.set_seat_no,
            self.set_customer_id
        ]
        self._recursive_menu(0, selections)

        # Get current time
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        # Create CustomerOrder entry
        params = {
            "order_date" : current_date,
            "order_time" : current_time,
            "customer_id" : self._customer_id
        }
        self.db.cursor.execute(
            "INSERT INTO CustomerOrder(OrderDate, OrderTime, CustomerID)\
            VALUES (:order_date, :order_time, :customer_id);",
            params
        )
        self.db.con.commit()
        order_id = self.db.cursor.execute("SELECT last_insert_rowid();").fetchall()[0][0]

        # Create Tickets entries
        assert self._car and self._train_occurance and self._seat_no
        params = {
            "order_id" : order_id,
            "car_id" : self._car[0],
            "route_name" : self._train_occurance[0],
            "start_station" : self._start_station,
            "end_station" : self._end_station,
            "run_date" : self._date
        }
        for seat in self._seat_no:
            params["place_no"] = seat
            self.db.cursor.execute(
                "INSERT INTO Ticket(OrderID, CarID, PlaceNo, NameOfRoute, StartStation, EndStation, RunDate)\
                VALUES (:order_id, :car_id, :place_no, :route_name, :start_station, :end_station, :run_date);",
                params
            )
            self.db.con.commit()

        booked_seats = self._seat_no
        self.clear_sets()
        return [("Successfully booked seat(s):", *booked_seats, f"With order id {order_id}",)]


    # --- }}}
    # --- View customer orders --- {{{
    def view_customer_orders(self, db: DB):
        """View custmer orders"""
        customer_id = int_response("Write your customer ID", 1, 4)
        orders = self._execute_query(db, "queries/orders.sql", {"customer_id":customer_id})

        headers = ("Start", "End", "Departure", "Arrival", "Seat", "Car", "Route")
        orders.insert(0, headers)
        return orders

    # --- }}}

if __name__=="__main__":
    app = App("test.db")
    # print(app._user_response(WeekDay))
    # print(app._user_varchar_response(4, 255))

    # db = DB("test.db")
    # app._clear_screen()
    # app.view_train_routes(db)
    # app.register_user(db)
    # app.seach_betwean_stops(db)
    # app.purachase_ticket(db)

    app.run()



