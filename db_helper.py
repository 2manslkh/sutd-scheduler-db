"""
DB Helper Class
"""
import json

class db_helper:
        
    def __init__(self, json_file):
         self.rawdata = json_file
         self.data = self.load_json(self.rawdata)
         
    def load_json(self, rawdata):
        with open(self.rawdata, "r") as read_file:
            data = json.load(read_file)
            return data
        
    def print_json(self):
        print(self.data)
        
    def save_json(self):
        with open("module_database_new.json", "w") as write_file:
            json.dump(self.data, write_file)
            
    def add_module(self, new_module):
        module_id = list(new_module.keys())[0]
        self.data["MODULES_DB"][module_id] = new_module
        
    def get_moduleID(module):
        return module
        
    def remove_module():
        #TODO
        pass
        
    def edit_module():
        #TODO
        pass

# =============================================================================
# Module Builder
# =============================================================================
"""
module: Unique Module ID (int)
subjectCode: Subject code of the module (str)
subjectName: Subject name of the module (str)
subjectLead: Course Leads [str]
"""


class Module_Builder():
        
    def __init__(self):
        self.module_id = ""
        self.json_data = {}
        
    def add_module(self, module_id):
        self.module_id = str(module_id)
        self.json_data[self.module_id] = {}
        return self
        
    def add_subjectCode(self, subject_code):
        self.json_data[self.module_id]["subjectCode"] = str(subject_code)
        return self
        
    def add_subjectName(self, subject_name):
        self.json_data[self.module_id]["subjectName"] = str(subject_name)
        return self
        
    def add_subjectLead(self, subject_lead):
        if type(subject_lead) != list:
            self.json_data[self.module_id]["subjectLead"] = [str(subject_lead)]
        else:
            self.json_data[self.module_id]["subjectLead"] = str(subject_lead)
        return self
        
    def add_sizeCohort(self, size_cohort):
        self.json_data[self.module_id]["sizeCohort"] = size_cohort
        return self
        
    def add_numCohort(self, num_cohort):
        self.json_data[self.module_id]["numCohort"] = num_cohort
        return self
        
    def add_sizeEnrollment(self, size_enrollment):
        self.json_data[self.module_id]["sizeEnrollment"] = size_enrollment
        return self
        
    def add_Slot(self, SlotBuilder):
        self.json_data[self.module_id]["CLASS_RELATED"] = SlotBuilder
        return self
    
    def add_Exam(self, ExamBuilder):
        self.json_data[self.module_id]["EXAM_RELATED"] = ExamBuilder
        return self
        
    def build(self):
        return self.json_data
        
    def _print_current(self):
        print(self.json_data)
        
class Slot_Builder():
        
    def __init__(self):
        self.slot_name = ""
        self.json_data = {}
        
    def add_name(self, slot_name):
        self.slot_name = str(slot_name)
        self.json_data[self.slot_name] = {}
        return self
        
    def add_type(self, slot_type):
        self.json_data[self.slot_name]["type"] = slot_type
        return self
        
    def add_location(self, slot_location):
        self.json_data[self.slot_name]["location"] = slot_location
        return self
    
    def add_sessions(self, sessions):
        self.json_data[self.slot_name]["sessions"] = sessions
        return self
    
    def add_others(self, others):
        self.json_data[self.slot_name]["others"] = others
        return self
    
    def add_makeup(self, makeup):
        self.json_data[self.slot_name]["makeup"] = makeup
        return self
    
    def build(self):
        return self.json_data

class Exam_Builder():
    
    def __init__(self):
        self.exam_name = ""
        self.json_data = {}
        
    def add_exam(self, exam_name):
        self.exam_name = str(exam_name)
        self.json_data[self.exam_name] = {}
        return self
        
    def add_duration(self, duration):
        self.json_data[self.exam_name]["duration"] = duration
        return self
    
    def add_location(self, location):
        self.json_data[self.exam_name]["location"] = location
        return self
        
    def add_admin(self, admin):
        self.json_data[self.exam_name]["admin"] = admin
        return self
    
    def build(self):
        return self.json_data
