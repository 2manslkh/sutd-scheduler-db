import csv
# from .models import myUser
# from django.db import models
from models import Module

def csv_to_db(csv_file_name, model):
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
                    Class(title = row[0],
                    class_type = row[1],
                    class_related = row[2],
                    location = row[3],
                    duration = row[4],
                    start = row[5],
                    end = row[6],
                    assigned_professors = row[7],
                    others = row[8],
                    makeup = row[9])


                elif "modules" in csv_file_name:
                    Modules(subject = row[0],
                    code = row[1],
                    term = row[2],
                    core = row[3],
                    subject_lead = row[4],
                    cohort_size = row[5],
                    enrolment_size = row[6])
                    
        

def modulecsv_to_db(title,class_type,class_related,location,duration,start,end,assigned_professors,other,makeup):

    # Add modules to db
    pass

def classescsv_to_db():
    # Add classes to db
    pass

def add_to_db():
    # Add entry to DB
    pass

csv_to_db("sample_input_modules.csv","")