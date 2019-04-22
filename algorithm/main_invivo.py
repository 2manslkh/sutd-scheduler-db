import random, copy
import time
from Classes_invivo import Group, Professor, CourseClass, Room, Slot
from math import ceil, log2
import math
import csv
import db_to_algo as dba
import datetime
from datetime import timedelta 

initial_slots = [Slot([10,11,12,13,14,15,16,17,18,19], 3),Slot([11,12,13,14,15,16,17,18,19], 5)]

Room.rooms = [Room("lt1",100), Room("lt2", 200), Room("lt3", 300)]

Slot.slots = copy.deepcopy(initial_slots)



max_score = None

cpg = []
slots = []
CourseClass.classes = []
Professor.professors = []
Group.groups = []
lts = []
bits_needed_backup_store = {}  # to improve performance

inputls = [[500051, "invivo", ["guest"], ["ISTD"], 200, 3, "2019-6-9"]]

date = inputls[0][6].split("-")
for i in range(len(date)):
    date[i] = int(date[i])
print(date)  
   
dayofweek = datetime.date(date[0], date[1], date[2]).isoweekday()
print(dayofweek)
def input_info(): 

    for e in inputls:
        if CourseClass.find(e[0], e[1], e[3]) == -1:
            CourseClass.classes.append(CourseClass(e[0], e[1], e[3], e[4], e[5]))
        if Professor.find(e[2]) == -1:
            Professor.professors.append(Professor(e[2]))
        if Group.find(e[3]) == -1:
            Group.groups.append(Group(e[3]))  

   
def get_cpg():
    input_info()
    len1 = len(inputls)
    for i in range(len1):
        
       cpg.append(CourseClass.find(inputls[i][0], inputls[i][1], inputls[i][3]))
       cpg.append(Professor.find(inputls[i][2]))
       cpg.append(Group.find(inputls[i][3]))



def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, slots, max_score, inputls, max_size
    input_info()
    cpg.clear()
    '''
    cpg = [CourseClass.find("CSE"),Professor.find("Natalie"),Group.find("Cl02"),
           CourseClass.find("CSE"),Professor.find("David"),Group.find("Cl03"),
           CourseClass.find("CSE"),Professor.find("Natalie"),Group.find("Cl01")]
    '''
    get_cpg()

    for _c in range(len(cpg)):
        #print(type(_c))
        
        if _c % 3 == 0:  # CourseClass
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')       
        elif _c % 3 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
        elif _c % 3 == 2:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')


    cpg = join_cpg_pair(cpg)

    max_size = 0
    for s in initial_slots:
        if len(s.block) > max_size:
            max_size = len(s.block)
            

    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), '0'))
    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))




def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(CourseClass.classes)]


def professor_bits(chromosome):
    i = bits_needed(CourseClass.classes)

    return chromosome[i: i + bits_needed(Professor.professors)]


def group_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors)

    return chromosome[i:i + bits_needed(Group.groups)]

def lt_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups)

    return chromosome[i:i + bits_needed(Room.rooms)]

def slot_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups) + bits_needed(Room.rooms)

    return chromosome[i:i + (bits_needed(Slot.slots) * ceil(log2(max_size)))]



       
def random_slot(cpg_c):
    
    temp_slot = random.choice(initial_slots)
    #print(temp_slot)
    temp_block = temp_slot.block
    random_day = temp_slot.day
    #print(CourseClass.classes[int(course_bits(cpg_c),2)])
    temp_duration = CourseClass.classes[int(course_bits(cpg_c),2)].duration
    random_start = random.randint(temp_block[0], temp_block[-1] - temp_duration)
    #print(random_start)
    temp_block = []
    random_end = random_start + int(temp_duration)
    for i in range(random_start, random_end):
        temp_block.append(i)
    random_slot = Slot(temp_block, random_day)
    if Slot.find(random_slot.block, random_slot.day) == -1:
        Slot.slots.append(random_slot)
        slots.append((bin(Slot.find(random_slot.block, random_slot.day))[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
    return slots[Slot.find(random_slot.block, random_slot.day)]

def random_room(cpg_c):
    temp_room = random.choice(Room.rooms)

    while temp_room.size < CourseClass.classes[int(course_bits(cpg_c),2)].population:
        temp_room = random.choice(Room.rooms)
    return lts[Room.find(temp_room.name)]

    

def init_population(n):
    global cpg
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            #print(CourseClass.classes[int(course_bits(_c), 2)].code, Group.groups[int(group_bits(_c), 2)].name)
            chromosome.append(_c + random_room(_c) + random_slot(_c))

        chromosomes.append(chromosome)
    return chromosomes


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    a = random.randint(0, len(chromosome) - 1)
    
    rand_slot = random_slot(chromosome[a])
    
    rand_room = random_room(chromosome[a])
    
    chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) +\
        group_bits(chromosome[a]) + rand_room + rand_slot

    # print("After mutation: ", end="")
    # printChromosome(chromosome)

    
def print_chromosome_csv(max_chromosomes):

        
    label = ["id", "invivo", "speaker", "pillar", "population","room", "date" "day", "start", "end"]
    out = open('schedule_invivo.csv','a', newline='')
    csv_write = csv.writer(out, dialect = 'excel')
    csv_write.writerow(label)
    for chromosome in max_chromosomes:
        daydelta = Slot.slots[int(slot_bits(chromosome), 2)].day - dayofweek
        vivo_date = datetime.date(date[0], date[1], date[2]) + timedelta(days = daydelta)
        
            
        time = str(Slot.slots[int(slot_bits(chromosome),2)]).split("-")
        csv_row = [CourseClass.classes[int(course_bits(chromosome), 2)].dbid,\
                   CourseClass.classes[int(course_bits(chromosome), 2)].code,\
                   Professor.professors[int(professor_bits(chromosome), 2)],\
                   Group.groups[int(group_bits(chromosome), 2)],\
                   Room.rooms[int(lt_bits(chromosome), 2)],\
                   vivo_date,\
                   Slot.slots[int(slot_bits(chromosome), 2)].day] + time
        csv_write.writerow(csv_row)
        print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)], " | ",
          vivo_date," | ",
          Slot.slots[int(slot_bits(chromosome), 2)], Slot.slots[int(slot_bits(chromosome), 2)].day)
    
    out.close()
    print("finish csv writing")
               


def genetic_algorithm():

    convert_input_to_bin()

    population = init_population(1)
    print("population", population)
    # print("Original population:")
    # print(population)
    print("\n------------- Genetic Algorithm --------------\n")

    chromo = []
    generation = 0
    while generation < 5:
        
        #print(population[0][0])
        print(chromo)
        #print(population[0][0] in chromo)
        if (population[0][0] in chromo) == True:
            for _p in range(len(population)):
                #crossover(population)
                #selection(population, 5)
                mutate(population[_p])  
        else:

            generation = generation + 1
            chromo.append(population[0][0])
            for _p in range(len(population)):
                #crossover(population)
                #selection(population, 5)
                mutate(population[_p]) 
            
          

    print(chromo)
    print_chromosome_csv(chromo)

        
        
        
def main():
    starttime = time.time()
    print(starttime)
    random.seed()
    genetic_algorithm()
    endtime = time.time()
    dtime = endtime - starttime
    
    print("time take: ",dtime)
main()
