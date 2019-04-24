import gcal_quickstart as gCal
import sqlite3

db = "../db.sqlite3"
FILTERED_CLASS_TABLE = "users_filteredresults"

def create_connection(db_file):
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

    # Get Rows from FILTERED_CLASS_TABLE
    c.execute(f"SELECT * from {FILTERED_CLASS_TABLE}")
    data = c.fetchall()
    print(data)
    gcal = gCal.Gcal()
    gcal.create_events(data)


if __name__ == '__main__':
    main()