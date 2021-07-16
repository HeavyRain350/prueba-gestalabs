import sqlite3
from sqlite3 import Error
import os.path

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r".\test.db"

    sql_create_table_items = """ CREATE TABLE IF NOT EXISTS items (
                                        id integer PRIMARY KEY,
                                        nombre text NOT NULL
                                    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_table_items)
    else:
        print("Error, no se pudo crear la tabla de items.")


if __name__ == '__main__':
    main()