class Group:
    groups = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find(name):
        for i in range(len(Group.groups)):
            if Group.groups[i].name == name:
                return i
        return -1
    


        
    def __repr__(self):
        #return "Class: " + str(self.name)
        return str(self.name)

class Professor:
    professors = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find(name):
        for i in range(len(Professor.professors)):
            if Professor.professors[i].name == name:
                return i
        return -1
    


    def __repr__(self):
        #return str(self.name)
        return str(self.name)

class CourseClass:
    classes = None

    def __init__(self, code, duration, pillar, isLecture = False, isLab = False):
        self.code = code
        self.duration = duration
        self.pillar = pillar
        self.isLecture = isLecture
        self.isLab = isLab
        
    @staticmethod
    def find(code):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].code == code:
                return i
        return -1


    def __repr__(self):
        if self.isLecture == True:
            #return "Course: " + str(self.code) + " lecture"
            return str(self.code) + " lecture"
        elif self.isLab == True:
            #return "Course: " + str(self.code) + " lab"
            return str(self.code) + " lab"
        else:
            #return "Course: " + str(self.code) + " cohort"
            return str(self.code) + " cohort"
        
class Room:
    rooms = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find(name):
        for i in range(len(Room.rooms)):
            if Room.rooms[i].name == name:
                return i
        return -1
    


    def __repr__(self):
        #return "Room: " + self.name
        return self.name

#Every block is half an hour
#First block starts from 8:30 
#Last block different from days(Wed, Friday are shorter)
class Slot:
    slots = None

    def __init__(self, block, day):
        self.block = block
        self.day = day
        
    def find(block, day):
        for i in range(len(Slot.slots)):
            if Slot.slots[i].block == block and Slot.slots[i].day == day:
                return i
        return -1
     
    def hour_start(self):
        start_hour_count = int((self.block[0] + 1)/2)
        start_hour = 8 + start_hour_count
        return str(start_hour)
    
    def minute_start(self):
        start_minute_count = self.block[-1] % 2
        if start_minute_count == 0:
            return "30"
        return "00"
    
    def hour_end(self):
        end_hour_count = int((self.block[-1] + 1)/2)
        end_hour = 8 + end_hour_count
        return str(end_hour)
    
    def minute_end(self):
        end_minute_count = self.block[-1] % 2
        if end_minute_count == 0:
            return "30"
        return "00"
    
    def __repr__(self):
        #return "Slot: " + Slot.hour_start(self) + ":" + Slot.minute_start(self) + " - " + Slot.hour_end(self) + ":" + Slot.minute_end(self)
        #return "Slot: " + str(self.block[0]) + " - " + str(self.block[-1]) + " Day: " + str(self.day)
        return str(self.block) + "\\" + str(self.day)  
'''
#test
print(Slot([4,5,6,7], "Mon"))
'''