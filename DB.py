#!/usr/bin/python3
# ---Imports---{{{
import sqlite3

# ---}}}

class DB:
    def __init__(self, db_name: str, tables: str = None, **kwargs):
        """
        Object to interact with an sqlite3 instance
        
        Inputs
        :param db_name: name of db file *with* .db extention
        :param tables: name of sql script to generate tables (optional)
        :param **kwargs:

        :Keyword Arguments:
            * *erase* (`bool`) --
                reset the entire db file
        """
        self.db_name = db_name
        if kwargs.get("erase"):
            self.erase()

        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()

        if tables:
            self.run_sql_script(tables)

    def erase(self):
        """Erases all db data."""
        open(self.db_name, "w").close()

    def run_sql_script(self, path_to_script: str):
        """Run an sql script on the DB instance."""

        with open(path_to_script, "r") as sql_file:
            sql_script = sql_file.read()

        self.cursor.executescript(sql_script)
        self.con.commit()

    # --- Internal --- {{{
    def __del__(self):
        """Close database connection"""
        self.con.close()

    def __repr__(self):
        query = """
            SELECT name FROM sqlite_master
                WHERE type='table';"""
        self.cursor.execute(query)
        return str(self.cursor.fetchall())

    # --- }}}

if __name__ == "__main__":
   # db = DB("norwegian_rail.db", "generate_railway_tables.sql", erase=True)
    db = DB("test.db", erase = True)
    db.run_sql_script("generate_railway_tables.sql")
    db.run_sql_script("data/nordlandsbanen.sql")
    db.run_sql_script("data/fill_trainroutes.sql")

    

