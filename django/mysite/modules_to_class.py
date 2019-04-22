import sqlite3

db = "db.sqlite3"
MODULE_TABLE = "users_module"
CLASS_TABLE = "users_class"

def modules_to_csv(db_file):

    def make_class_data(data,i=-1,lesson_type=""):
        num_cohorts = data["cohorts"][0]
        if lesson_type == "CBL":
            print(i)
            print( data["cohorts_per_week"][0].split(","))
            out = [data["subject"][0],
            data["pillar"][0],
            lesson_type,
            f"{data['term'][0]}C{data['pillar'][0]}{i}",
            "",
            data["cohorts_per_week"][0].split(",")[i-1],
            data["subject_lead"][0],
            "","","","",""]
        elif lesson_type == "LEC":
            a=""
            for c in range(1,int(num_cohorts)+1):
                a += f"{data['term'][0]}C{data['pillar'][0]}{c},"
            a=a[0:len(a)-1]
            out = [data["subject"][0],
            data["pillar"][0],
            lesson_type,
            f"{a}",
            "",
            data["lectures_per_week"][0].split(",")[i-1],
            data["subject_lead"][0],
            "","","","",""]
        elif lesson_type == "LAB":
            a=""
            for c in range(1,int(num_cohorts)+1):
                a += f"{data['term'][0]}C{data['pillar'][0]}{c},"
            a=a[0:len(a)-1]
            out = [data["subject"][0],
            data["pillar"][0],
            lesson_type,
            f"{a}",
            "",
            data["labs_per_week"][0].split(",")[i-1],
            data["subject_lead"][0],
            "","","","",""]

        # EACH CLASS_RELATED SHOULD BE BATCH UNIQUE
        return out

    # Start Connection
    conn = create_connection(db_file)
    c = conn.cursor()

    # Get Rows from MODULE TABLE
    c.execute(f"SELECT * from {MODULE_TABLE}")
    modules = c.fetchall()

    c.execute(f'SELECT * FROM {MODULE_TABLE}')   
    headers = list(map(lambda x: x[0], c.description))

    for row in modules:
        data = {}
        row_id = row[0]
        for header in headers:
            data[header] = c.execute(f"SELECT {header} from {MODULE_TABLE} WHERE id={row_id}").fetchone()
        class_data = []

        count = 1
        for x in data["cohorts_per_week"][0].split(","):
            for i in range(int(data["cohorts"][0])):
                class_data = make_class_data(data,count,"CBL")
                c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,{row_id})",class_data)
            count += 1
        # Assume lectures and labs are combined
        count = 1
        for y in data["lectures_per_week"][0].split(","):
            class_data = make_class_data(data,count,"LEC")
            c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,{row_id})",class_data)
            count += 1
        
        count = 1
        for z in data["labs_per_week"][0].split(","):
            class_data = make_class_data(data,count,"LAB")
            c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,{row_id})",class_data)
            count += 1

    conn.commit()
    conn.close()

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

modules_to_csv(db)