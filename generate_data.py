#!/usr/bin/python3
# ---Imports---{{{
import sqlite3

# ---}}}

def generate_empty_db(db_name: str) -> None:
    """
    Create new db file or clear the file if it allready exits.
    :param db_name: name of db file
    """
    pass

def fill_tables(db: str, path_to_script: str) -> None:
    """
    Fill db with empty tables using an sql script.

    Inputs
    :param db: name of db file
    :param path_to_script: relative or absolute path to table generation script.
    """
    pass


if __name__ == "__main__":
    generate_empty_db("./train_db.sql")

