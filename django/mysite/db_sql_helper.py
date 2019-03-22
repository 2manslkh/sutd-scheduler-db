import sqlite3
from sqlite3 import Error

"""
SQLITE CHEATSHEET
SELECT column1, column2, columnN 
FROM table_name
WHERE [condition1] AND [condition2]...AND [conditionN];
* --> Wildcard / ALL
? --> Placeholder
"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        print()
 
    return None


def parse_filters(conditions):
    """
    conditions: array of conditions
    out: SQL Query formatted
    """
    out = ""
    if type(conditions) == list:
        if (len(conditions) > 0):
            out = conditions[0]
            if len(conditions) > 1:
                for i in range(1,len(conditions)):
                    out += " OR {}".format(conditions[i])
    else:
        out = conditions

    return out

def add_headers(conn,table_name):
    cur = conn.cursor()
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME={}".format(table_name))
    out = cur.fetchall()
    return out



def filter_by_module(conn, a,b,c):
    """
    a = table name
    b = filter by
    c = conditions, 1D array
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:

    PRINTS ALL FILTERED ROWS
    """
    c = parse_filters(c)

    cur = conn.cursor() 
    cur.execute("SELECT * FROM {} WHERE {}={}".format(a,b,c))
    rows = cur.fetchall()
    print(rows)

    # for row in rows:
    #     print(row)

def get_all_modules(conn, sql_table):
    """
    a = table name
    b = filter by
    c = conditions, 1D array
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:

    PRINTS ALL ROWS
    """

    cur = conn.cursor() 
    cur.execute("SELECT * FROM {}".format(sql_table))
    rows = cur.fetchall()
    print(rows)

    # for row in rows:
    #     print(row)

conn = create_connection("db.sqlite3")
print(conn)
with conn:
#     filter_by_module(conn, "schedule_module", "UnitPrice", "1.99")
#     print(add_headers(conn,"invoice_items"))
       get_all_modules(conn,"schedule_module")