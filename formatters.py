from __future__ import annotations # For python < 3.11

from tabulate import tabulate
from os import system
import numpy as np

def clear_screen():
    """Clear the screan, this only works for UNIX systems"""
    system("clear")
    
def draw_car(n_compartments: int, n_rows: int, seats_per_row: int, reserved_seats: list[int]) -> str:
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
    return tabulate(formatted_seats, tablefmt="rounded_grid", colalign=("center","center"))

def format_car_options(table: list[tuple]):
    '''Formats a (CarID, CarNo, NumOfRows, SeatsPerRow, NumOfCompartments)
        table into a list of ["CarNo  CarType"].
    '''
    formatted_list = [""]*len(table)
    for i, row in enumerate(table):
        car_type = "Sleep car" if row[4] else "Chair car"
        formatted_list[i] = f"{row[1]:>2} {car_type}"
    return formatted_list
