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

    def __init__(self, code, duration, pillar, isLecture = False, isLab = False, isHASS = False, isMorning = False, isAfternoon = False):
        self.code = code
        self.duration = duration
        self.pillar = pillar
        self.isLecture = isLecture
        self.isLab = isLab
        self.isHASS = isHASS
        self.isMorning = isMorning
        self.isAfternoon = isAfternoon
        
    @staticmethod
    def find(code, duration):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].code == code and CourseClass.classes[i].duration == duration:
                return i
        return -1



    def __repr__(self):
        if self.isLecture == True:
            #return "Course: " + str(self.code) + " lecture"
            return str(self.code) + " lecture" + " duration " + str(self.duration)
        elif self.isLab == True:
            #return "Course: " + str(self.code) + " lab"
            return str(self.code) + " lab" + " duration " + str(self.duration)
        else:
            #return "Course: " + str(self.code) + " cohort"
            return str(self.code) + " cohort" + " duration " + str(self.duration)
        
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

    def __init__(self, block, day, isHASS = False):
        self.block = block
        self.day = day
        self.isHASS = isHASS
        
    def find(block, day):
        for i in range(len(Slot.slots)):
            if Slot.slots[i].block == block and Slot.slots[i].day == day:
                return i
        return -1
     
    def hour_start(self):
        start_hour_count = int((self.block[0])/2)
        start_hour = 8 + start_hour_count
        return str(start_hour)
    
    def minute_start(self):
        start_minute_count = (self.block[0]) % 2
        if start_minute_count == 0:
            return "00"
        return "30"
    
    def hour_end(self):
        end_hour_count = int((self.block[-1] + 1)/2)
        end_hour = 8 + end_hour_count
        return str(end_hour)
    
    def minute_end(self):
        end_minute_count = (self.block[-1]) % 2
        if end_minute_count == 0:
            return "30"
        return "00"
    
    def __repr__(self):
        #return "Slot: " + Slot.hour_start(self) + ":" + Slot.minute_start(self) + " - " + Slot.hour_end(self) + ":" + Slot.minute_end(self)
        #return "Slot: " + str(self.block[0]) + " - " + str(self.block[-1]) + " Day: " + str(self.day)
        return str(self.block) + "\\" + str(self.day)#  + str(self.isHASS)

#test
#print(Slot([1,6], "Mon"))
