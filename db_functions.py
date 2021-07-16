import sqlite3
from sqlite3 import Error

database = r".\test.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

## Método que inserta un item en la tabla items
def create_item(item):
    conn = create_connection(database)
    sql = ''' INSERT INTO items(nombre)
              VALUES(?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()
        return cur.lastrowid

## Método que obtiene el último id insertado en la tabla items
def obtain_items_last_id():
    conn = create_connection(database)
    with conn:
        sql = '''SELECT id FROM items ORDER BY id DESC LIMIT 1;'''
        cur = conn.cursor()
        cur = cur.execute(sql)
        if(cur.fetchone() is not None):
            id = cur.fetchone()[0]
        else:
            id = 0
        return id
