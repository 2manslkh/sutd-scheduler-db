import sqlite3
import csv

# from .models import myUser
# from django.db import models

def csv_to_db(csv_file_name, db_file):
    conn = create_connection(db_file)
    c = conn.cursor()
    print(c.fetchall())
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f"Filename: {csv_file_name}")
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if "class" in csv_file_name:
                    c.execute('INSERT INTO "users_class" VALUES (NULL, ?,?,?,?,?,?,?,?,?,?)', row)
                    print(row)
                elif "modules" in csv_file_name:
                    c.execute('INSERT INTO "users_module" VALUES (NULL, ?,?,?,?,?,?,?)', row)
                    print(row)
    conn.commit()
    conn.close()

def modulecsv_to_db(title,class_type,class_related,location,duration,start,end,assigned_professors,other,makeup):
    # Add modules to db
    pass

def classescsv_to_db():
    # Add classes to db
    pass

def add_to_db():
    # Add entry to DB
    pass

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

csv_to_db("sample_input_modules.csv","db.sqlite3")