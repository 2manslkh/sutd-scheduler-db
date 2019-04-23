import django.mysite.gcal_quickstart as gcal
import sqlite3

db = "db.sqlite3"
FILTERED_CLASS_TABLE = "users_class_filtered"

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
 
    return None


def main():
    # Start Connection
    conn = create_connection(db)
    c = conn.cursor()

    # Get Rows from MODULE TABLE
    c.execute(f"SELECT * from {FILTERED_CLASS_TABLE}")
    data = c.fetchall()


    #TODO: Get from DB


if __name__ == '__main__':
    main()