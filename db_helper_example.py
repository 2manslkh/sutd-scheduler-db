# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:17:21 2019

@author: kengh

"""

from db_helper import Module_Builder, Slot_Builder, Exam_Builder, db_helper

# =============================================================================
# DB Helper Example
# =============================================================================
        
new_module = (
     Module_Builder()
    .add_module(3007)
    .add_subjectCode("3.007")
    .add_subjectName("Introduction to Design")
    .add_subjectLead("Lim Keng Hin")
    .add_sizeCohort(50)
    .add_numCohort(3)
    .add_sizeEnrollment(150)
    .add_Slot(
            Slot_Builder()
            .add_name("LI01")
            .add_type("Lecture")
            .add_location("*LT")
            .add_sessions([1.5,1.5])
            .add_others("Boring")
            .add_makeup(False)
            .add_name("CI01")
            .add_type("Cohort")
            .add_location("*LT")
            .add_sessions([1.5,1.5])
            .add_others("Boring")
            .add_makeup(False)
            .add_name("CI02")
            .add_type("Cohort")
            .add_location("*LT")
            .add_sessions([1.5,1.5])
            .add_others("Boring")
            .add_makeup(False)
            .add_name("CI03")
            .add_type("Cohort")
            .add_location("*LT")
            .add_sessions([1.5,1.5])
            .add_others("Boring")
            .add_makeup(False)
            .build()
            )
    .add_Exam(
            Exam_Builder()
            .add_exam("MID TERM")
            .add_duration(999)
            .add_admin("Lim Keng Hin")
            .add_location("Toilet")
            .build()
            )
    .build()
    )

stored_db = db_helper("module_database.json")
#print(list(stored_db.data["MODULES_DB"].keys()))
stored_db.add_module(new_module)
stored_db.print_json()
stored_db.save_json()