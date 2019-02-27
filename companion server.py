# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:43:05 2019

@author: jen yang
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:/Users/Ng Jen Yang/Downloads/esc2019-462ed-firebase-adminsdk-e0yey-332b104e0a.json")
#firebase_admin.initialize_app(cred, {    'databaseURL': 'https://esc2019-462ed.firebaseio.com/'})


mainref = db.reference("")

hi=mainref.get()

#print(hi)
sample_course = hi["MODULES_DB"]['3007']
sample_details = sample_course["CLASS_RELATED"]["CI01"]["location"], sample_course["subjectName"], sample_course["subjectLead"]
sample_course_2 = hi["MODULES_DB"]['50034']
sample_details_2 = sample_course_2["CLASS_RELATED"]["CI01"]["location"], sample_course_2["subjectName"], sample_course_2["subjectLead"]
sample_start_time = 830
sample_end_time = 1000
sample_start_time_2 = 1000
sample_end_time_2 = 1200
sample_start_time_3 = 1100
sample_end_time_3 = 1230

class DayTemplate():
    def __init__(self,day):
        self.start = 0000
        self.end = 2359
        self.events_list = []
        self.name = day
    def name(self):
        return self.name
    def add_event(self, start_time, end_time, event_details):
        print("init add event")
        if start_time < 0000 or end_time > 2359:
            print("invalid timeslot")
        else:
            print("valid timeslot")
            events_for_the_day = self.events_list
            if events_for_the_day == []:
                events_for_the_day.append((start_time,end_time, event_details))
                print("event created")
            else:
                for item in self.events_list:
                    print(item)
                    if item[0] != start_time:
                        print("s no clash")
                        if item[1] != end_time:
                            print("e no clash")
                            if item[1] - start_time < 0:
                                print("not in middle")
                                self.events_list.append((start_time,end_time, event_details))
                                print("event created")
                            else:
                                print("in middle of other lesson")
                        else:
                            print("end time clash")
                    else:
                        print("start time clash")
    def remove_event(self, start_time, end_time, event_details):
        event_to_be_removed = (start_time,end_time,event_details)
        print("init remove event")
        for i in self.events_list:
            if i == event_to_be_removed:
                self.events_list.remove(event_to_be_removed)
                print("success")
            else:
                print("error")
        


class WeekTemplate():
    def __init__(self):
        self.Monday = DayTemplate("Monday")
        self.Tuesday = DayTemplate("Tuesday")
        self.Wednesday = DayTemplate("Wednesday")
        self.Thursday = DayTemplate("Thursday")
        self.Friday = DayTemplate("Friday")
        self.Saturday = DayTemplate("Saturday")
        self.Sunday = DayTemplate("Sunday")
        self.days = [self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday]
    def print_weekly_schedule(self):        
        a = self.Monday.events_list
        b = self.Tuesday.events_list
        c = self.Wednesday.events_list
        d = self.Thursday.events_list
        e = self.Friday.events_list
        f = self.Saturday.events_list
        g = self.Sunday.events_list
        if a == []:
            amsg = "Nothing on!"
        else: 
            amsg = a
        b = self.Tuesday.events_list
        if b == []:
            bmsg = "Nothing on!"   
        else:
            bmsg = b
        if c == []:
            cmsg = "Nothing on!"
        else:
            cmsg = c
        if d == []:
            dmsg = "Nothing on!"
        else:
            dmsg = d
        if e == []:
            emsg = "Nothing on!"
        else:
            emsg = e
        if f == []:
            fmsg = "Weekend"
        else:
            fmsg = f
        if g == []:
            gmsg = "Weekend"
        else:
            gmsg = g
        to_console = "Monday : {} \nTuesday : {} \nWednesday : {} \nThursday : {} \nFriday : {} \nSaturday : {} \nSunday : {} \n".format(amsg,bmsg,cmsg,dmsg,emsg,fmsg,gmsg)
        print(to_console)
    def collect(self,group):
#        print("init collect")
        collected = []
        for i in self.days:
            templs = i.events_list
            for event in templs:
#                print(event[2][1])
                if event[2][1] == group:
                    collected.append((i.name, event[0],event[1],event[2][0]))
#                    print("success")
#            print(collected)\
        amsg = []
        bmsg = []
        cmsg = []
        dmsg = []
        emsg = []
        fmsg = []
        gmsg = []
        for i in collected:
            gmsg = []
#            print(i[0])
            if i[0] == "Monday":
                amsg.append((i[1],i[2],i[3]))
            elif i[0] == "Tuesday":
                bmsg.append((i[1],i[2],i[3]))
            elif i[0] == "Wednesday":
                cmsg.append((i[1],i[2],i[3]))
            elif i[0] == "Thursday":
                dmsg.append((i[1],i[2],i[3]))
            elif i[0] == "Friday":
                emsg.append((i[1],i[2],i[3]))
            elif i[0] == "Saturday":
                fmsg.append((i[1],i[2],i[3]))
            elif i[0] == "Sunday":
                gmsg.append((i[1],i[2],i[3]))
        to_console = "Monday : {} \nTuesday : {} \nWednesday : {} \nThursday : {} \nFriday : {} \nSaturday : {} \nSunday : {} \n".format(amsg,bmsg,cmsg,dmsg,emsg,fmsg,gmsg)
        print(to_console)
                
                    
    
new_week = WeekTemplate()
new_week.print_weekly_schedule()
new_week.Monday.add_event(sample_start_time,sample_end_time,sample_details)
#new_week.print_weekly_schedule()
new_week.Tuesday.add_event(sample_start_time_2,sample_end_time_2,sample_details)
#new_week.print_weekly_schedule()
new_week.Thursday.add_event(sample_start_time_2,sample_end_time_2,sample_details)
#new_week.print_weekly_schedule()

new_week.Monday.add_event(sample_start_time_3,sample_end_time_3,sample_details_2)
#new_week.print_weekly_schedule()
new_week.Tuesday.add_event(sample_start_time_3,sample_end_time_3,sample_details_2)
#new_week.print_weekly_schedule()
new_week.Wednesday.add_event(sample_start_time_2,sample_end_time_2,sample_details_2)
print("\n\n\n")
new_week.print_weekly_schedule()
print("\n\n\n")
print("looking for collect 1")
new_week.collect("Introduction to Design")
print("looking for collect 2")
new_week.collect("Introduction to Probability and Statistics")
print("\n\n\n")
new_week.Friday.add_event(sample_start_time_2,sample_end_time_2,sample_details_2)
new_week.print_weekly_schedule()
new_week.Friday.remove_event(sample_start_time_2,sample_end_time_2,sample_details_2)
new_week.print_weekly_schedule()