import sqlite3

db = "db.sqlite3"
MODULE_TABLE = "users_module"
CLASS_TABLE = "users_class"

def modules_to_csv(db_file):

    def make_class_data(data,i=-1,j=-1):
        out = [data]
        # EACH CLASS_RELATED SHOULD BE BATCH UNIQUE
        return []

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
                class_data = make_class_data(data,count,i,"CBL")
                c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, {title},?,?,?,?,?,?,?,?,?,?,?,{row_id})")
                count += 1
        # Assume lectures and labs are combined
        count = 1
        for y in data["lectures_per_week"][0].split(","):
            class_data = make_class_data(data,count,i,"LEC")
            c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, {title},?,?,?,?,?,?,?,?,?,?,?,{row_id})")
            count += 1
        
        count = 1
        for z in data["labs_per_week"][0].split(","):
            class_data = make_class_data(data,count,i,"LAB")
            c.execute(f"INSERT INTO {CLASS_TABLE} VALUES (NULL, {title},?,?,?,?,?,?,?,?,?,?,?,{row_id})")
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