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
        return "Group: " + self.name


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
        return "Professor: " + self.name


class CourseClass:
    classes = None

    def __init__(self, code):
        self.code = code
        
    @staticmethod
    def find(code):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].code == code:
                return i
        return -1


    def __repr__(self):
        return "CourseClass: " + self.code


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
        return "Room: " + self.name


class Slot:
    slots = None

    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day

        

    def __repr__(self):
        return "Slot: " + self.start + "-" + self.end + " Day: " + self.day