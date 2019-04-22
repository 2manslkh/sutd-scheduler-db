import sqlite3
import csv
import sys
# from .models import myUser
# from django.db import models

def csv_to_db(csv_file_name, db_file):
    conn = create_connection(db_file)
    c = conn.cursor()
    with open(csv_file_name,"r",encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f"Filename: {csv_file_name}")
                print(f'Column names are: {", ".join(row)}')
                line_count += 1
                if "class" in csv_file_name:
                    print(get_col_headers_db(c,"users_class"))
                if "modules" in csv_file_name:
                    print(get_col_headers_db(c,"users_module"))
            else:
                if "class" in csv_file_name:
                    print(row[0])
                    row.append(get_module_id(row[0], c))
                    c.execute('INSERT INTO "users_class" VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
                    print(row)
                elif "modules" in csv_file_name:
                    c.execute('INSERT INTO "users_module" VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?)', row)
                    print(row)
    conn.commit()
    conn.close()

def get_module_id(name, cursor):
    cursor.execute('SELECT id FROM users_module WHERE subject=?', [name])
    return cursor.fetchone()[0]

def parse_modules_to_class(module_csv, class_csv):
    
    conn = create_connection("db.sqlite3")
    c = conn.cursor()
    headers = get_col_headers_db(c,"users_class")

    def is_new_file(class_csv):
        with open(class_csv,"r",newline='') as f:
            csv_reader = csv.reader(f, delimiter=',')
            row_count = sum(1 for row in csv_reader)
            if (row_count == 0):
                return True
            else:
                return False

    def insert_row(class_csv, data):
        with open(class_csv,"a",newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            
            if (is_new_file(class_csv)):
                csv_writer.writerow(headers[1:len(headers)-1])
                # csv_writer.writerow(['title','pillar','class_type','class_related','location','duration','assigned_professors','description','makeup','start','end'])
            else:
                csv_writer.writerow(data)
    
    with open(module_csv,"r",encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                col_headers = row
                name_index = get_col_index(row,"subject")
                pillar_index = get_col_index(row,"pillar")
                print(name_index)
                cohort_size_index = get_col_index(row,"cohorts")
                print(cohort_size_index)
                cohort_index = get_col_index(row,"cohorts_per_week")
                lecture_index = get_col_index(row,"lectures_per_week")
                lab_index = get_col_index(row,"labs_per_week")
                professors_index = get_col_index(row,"subject_lead")
                print(f"Filename: {module_csv}")
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                num_cohorts = row[cohort_size_index]
                cohorts = row[cohort_index]
                lectures = row[lecture_index]
                labs = row[lab_index]
                if (len(cohorts) != 0): 
                    cohorts = cohorts.split(",")
                    i = 1
                    for c in cohorts:
                        for j in range(int(num_cohorts)):
                            insert_row(class_csv,[row[name_index],row[pillar_index],f"CBL{i}",f"{j+1}","",c,row[professors_index],"","","","",""])
                            print("a")
                            i += 1
                if (len(lectures) != 0): 
                    lectures = lectures.split(",")
                    i = 1
                    a = ""
                    for c in range(1,int(num_cohorts)+1):
                        a += f"CI{c},"
                    a = a[0:len(a)-1]
                    for l in lectures: # for each entry e.g. ['1.5'] in the lecture field
                        insert_row(class_csv,[row[name_index],row[pillar_index],f"LEC{i}",f"{a}","",l,row[professors_index],"","","","",""])
                        i += 1
                if (len(labs) != 0): 
                    labs = labs.split(",")
                    i = 1
                    for l in labs:
                        insert_row(class_csv,[row[name_index],row[pillar_index],f"LAB{i}",f"{a}","",l,row[professors_index],"","","","",""])
                        i += 1

def get_col_headers_db(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')   
    return list(map(lambda x: x[0], cursor.description))
                
def get_col_headers(csv_file):
    with open(csv_file) as f:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            col_names = row
            return col_names
        
def get_col_index(col_names, my_col_name):
    for i in range(len(col_names)):
        if (col_names[i] == my_col_name):
            return i
    print("col_name not found")

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

if __name__ == "__main__":
    try:    
        method = str(sys.argv[1])
        input1 = str(sys.argv[2])
        input2 = str(sys.argv[3])

        if method == "csv_to_db":
            csv_to_db(input1,input2)
        elif method == "parse_modules_to_class":
            parse_modules_to_class(input1,input2)
        else:
            print("Invalid Method: csv_to_db(csv,db) or parse_modules_to_class(csv_modules,csv_class)")
    except IndexError:
            print("Invalid Method: csv_to_db(csv,db) or parse_modules_to_class(csv_modules,csv_class)")