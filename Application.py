#!/usr/bin/python3
# --- Imports --- {{{
from DB import DB
from formatters import draw_car, format_car_options, tabulate
from user_interface import clear_screen, option_response, varchar_response, int_response, datetime_response

from datetime import datetime
import numpy as np
# --- }}}

class App:
    def __init__(self) -> None:
        """
        
        """
        self.functions = {
            "View train routes passing through a station on a weekday" : self.view_train_routes,
            "Register a new user" : self.register_user,
            "Search train routes between two stops" : self.seach_betwean_stops,
            "Purchase a ticket" : self.purachase_ticket,
            "View upcomming orders" : self.view_customer_orders
        }
    def run(self) -> None:
        """Start the application"""
        db = DB("test.db")
        self._main_menu(db)

# --- Internal functions --- {{{
    def _main_menu(self, db: DB) -> None:
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
                ret = self.functions[options[user_response]](db)
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

# --- }}}

# --- User functions --- {{{
    # --- View train routes {{{
    def view_train_routes(self, db: DB):
        """Let user get information of trainroutes"""
        clear_screen()

        # Get all stations
        db.cursor.execute("SELECT Name FROM RailwayStation")
        stations = [row[0] for row in db.cursor.fetchall()]

        # Get all weekdays
        db.cursor.execute("SELECT Name FROM WeekDay")
        weekdays= [row[0] for row in db.cursor.fetchall()]

        # Get user respons
        try:
            response_day = weekdays[option_response("Select a weekday", weekdays, show_shortcut_hints=True)]
            response_station = stations[option_response("Select a station", stations, show_shortcut_hints=True)]
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
    def register_user(self, db: DB) -> list[tuple] | None:
        """Let user register in the customer registry."""
        clear_screen()

        try:
            name = varchar_response("Full name:", 0, 255)
            phone_no = int_response("Phone number", 0, 10)
            email = varchar_response("Email:", 0, 255)
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

        return [(f"Successfully registered user {name}!",)]

    # --- }}}
    # --- Search routes between stops --- {{{
    def seach_betwean_stops(self, db: DB, **kwargs) -> list[tuple] | tuple[list[tuple], str, str] | None:
        """Search trainroutes between two stops
        -- Keyword Arguments:
            * ret_station: bool (return start and stop stations)
        """
        clear_screen()

        # Get all stations
        db.cursor.execute("SELECT Name FROM RailwayStation")
        stations = [row[0] for row in db.cursor.fetchall()]

        # Get user respons
        while True:
            try:
                response_station_1 = stations[option_response("Select a start", stations)]
                stations.remove(response_station_1)
                try: 
                    response_station_2 = stations[option_response("Select a destination station", stations)]
                    try:
                        # date, time = datetime_response()
                        implemented_dates = ["2023-04-03", "2023-04-04"] #temporary
                        time_ = varchar_response("Please select a time (hhmm)", 4, 4)
                        time_formatted = f"{time_[:2]}:{time_[2:]}"
                        print(time_formatted)

                        date = implemented_dates[option_response("Select a date", implemented_dates)] # temporary
                    except SystemExit:
                        continue # Exit datetime selection
                except SystemExit:
                    continue # Exit stop station selection
            except SystemExit:
                return None
            break

        # Get table of rows that match the query
        table = self._execute_query(
            db, 
            "queries/routes_between_stations.sql", 
            {"start_station" : response_station_1, "end_station" : response_station_2, "date_": date, "time_":time_formatted}
        )
        if kwargs.get("ret_station"):
            return table, response_station_1, response_station_2
        else:
            headers = ("Route", "Date", "Start", "Departure", "End", "Arrival")
            table.insert(0, headers)
            return table

    # --- }}}
    # --- Purchase ticket --- {{{
    def purachase_ticket(self, db: DB) -> list[tuple] | None:
        """Let user purchase available tickets from desired train route."""

        while True:
            try:
                # Select stations and date
                routes, start_station, end_station = self.seach_betwean_stops(db, ret_station=True)

                try: 
                    # Select train occurance
                    options = ["  ".join(route) for route in routes]
                    route_name, route_time, route_date = routes[option_response("Select a desired route", options)]

                    # Select car
                    cars = self._execute_query(db, "queries/get_cars.sql", {"train_route":route_name})
                    options = format_car_options(cars)
                    car = cars[option_response("Select a car. (Car number, Car type)", options)]
                    car_id, car_no, n_rows, seats_per_row, n_compartments = car

                    # Find start and stop subsection numbers
                    start_sec_no = db.cursor.execute(
                        "SELECT TSS.SubSectionNo FROM TrackSubSection AS TSS WHERE TSS.StartsAt = :start_station",
                        {"start_station":start_station}
                    ).fetchall()[0][0]
                    end_sec_no = db.cursor.execute(
                        "SELECT TSS.SubSectionNo FROM TrackSubSection AS TSS WHERE TSS.EndsAt = :end_station",
                        {"end_station":end_station}
                    ).fetchall()[0][0]
                    if start_sec_no > end_sec_no: start_sec_no, end_sec_no = end_sec_no, start_sec_no

                    # Find reserved seats
                    params = {
                        "run_date" : route_date,
                        "name_of_route" : route_name,
                        "car_id" : car_id,
                        "start_sec_no":start_sec_no, 
                        "end_sec_no":end_sec_no
                    }
                    tickets = [ticket[0] for ticket in self._execute_query(db, "queries/get_taken_seats.sql", params)]

                    # Check if sleep car
                    if n_compartments:
                        n_rows = n_compartments
                        seats_per_row = 2
                        # One bed reserves a whole coupe
                        for ticket in tickets.copy():
                            if ticket%2: tickets.append(ticket+1)
                            else: tickets.append(ticket-1)

                    # Select seat
                    options = np.arange(1, seats_per_row*n_rows+1)
                    if len(tickets) > 0: 
                        options = np.delete(options, np.array(tickets)-1).tolist() # remove reseved seats
                    car_overview = draw_car(n_compartments, n_rows, seats_per_row, tickets) # visualization of car (str)

                    user_choice_indeces = option_response(msg=car_overview, options=options, multi_select=True, show_multi_select_hint=True)
                    print(user_choice_indeces)
                    user_booking = np.array(options)[np.array(user_choice_indeces)].tolist() #need numpy to slice list of indeces

                    # Get time
                    now = datetime.now()
                    date = now.strftime("%Y-%m-%d")
                    time_ = now.strftime("%H:%M")

                    # Get customer id, this solution is not optimal, but there is no login system
                    customer_id = int_response("What is your custmer-id?", 0, 4)

                    # Create CustomerOrder
                    db.cursor.execute(
                        "INSERT INTO CustomerOrder(OrderDate, OrderTime, CustomerID)\
                        VALUES (:order_date, :order_time, :customer_id);",
                        {"order_date":date, "order_time":time_, "customer_id":customer_id}
                    )
                    db.con.commit()
                    order_id = db.cursor.execute("SELECT last_insert_rowid();").fetchall()[0][0]

                    # Create Tickets
                    params = {
                        "order_id":order_id,
                        "car_id":car_id,
                        "route_name":route_name,
                        "start_station":start_station,
                        "end_station":end_station,
                        "run_date":route_date
                    }
                    for seat in user_booking:
                        params["place_no"] = seat
                        db.cursor.execute(
                            "INSERT INTO Ticket(OrderID, CarID, PlaceNo, NameOfRoute, StartStation, EndStation, RunDate)\
                            VALUES (:order_id, :car_id, :place_no, :route_name, :start_station, :end_station, :run_date);",
                            params
                        )
                        db.con.commit()

                except SystemExit: continue # Exit to route selection
            except SystemExit: return None # Exit to main menu
            except TypeError: return None
            break # No exceptions! Break the loop

        return [("Successfully booked seat(s):", *user_booking, f"With order id {order_id}",)]


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



