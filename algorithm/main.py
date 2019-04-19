'''
TODO:
    1. HASS->fixed time slot
    2. No cohort should have same course more than once everyday (except lecture) 
    3. Input hard constraints from professors whether they would like to have lecture(s) before/after cohort(s) 
    4. Final clarification: Classroom is an input from professors
    5.

'''
import random, copy
import time
from Classes import Group, Professor, CourseClass, Room, Slot
from math import ceil, log2
import math
import csv
import db_to_algo as dbh

"""
Get inputs from sqlite DB:
dbh = db_helper("db.sqlite3")
dbh.print_all_columns("users_class")
dbh.get_columns(["title","assigned_professors","class_related","location","pillar","duration","type"],"users_class"))
"""


initial_slots = [Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], 1), Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], 2), Slot([1,2,3,4,5,6,7,8,9,10], 3),
              Slot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], 4), Slot([1,2,3,4,5,6,7,8,9,10], 5)]
given_duration = 0
for i in range(len(initial_slots)):
    given_duration = given_duration + len(initial_slots[i].block)
print(given_duration)
Slot.slots = copy.deepcopy(initial_slots)

max_score = None

cpg = []
slots = []
CourseClass.classes = []
Professor.professors = []
Group.groups = []
Room.rooms = []
bits_needed_backup_store = {}  # to improve performance

inputls = [["CSE", ["Natalie"], ["Cl02"], "CC12","ISTD",3],\
           ["CSE", ["David"], ["Cl03"], "CC12","ISTD",3],\
           ["CSE", ["Natalie"], ["Cl01"], "CC12","ISTD",3],\
           ["CSE", ["Natalie"], ["Cl02"], "CC12","ISTD",3], ["CSE", ["David"], ["Cl03"], "CC12","ISTD",3], ["CSE", ["Natalie"], ["Cl01"], "CC12","ISTD",3],\
           ["CSE lab", ["Natalie", "David"], ["Cl01", "Cl02", "Cl03"], "lt2", "ISTD", 4, "lab"], \
           ["ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",3],\
           ["ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",3], ["ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",3],\
           ["ESC", ["Sun Jun"], ["Cl02"], "CC11","ISTD",4], ["ESC", ["Sun Jun"], ["Cl03"], "CC11","ISTD",4], ["ESC", ["Sun Jun"], ["Cl01"], "CC11","ISTD",4],\
           ["P&S lec", ["Tony", "ABC"], ["Cl01", "Cl02", "Cl03"],"lt5", "ISTD", 3, "lecture"], ["P&S lec", ["Tony", "ABC"], ["Cl01", "Cl02", "Cl03"], "lt5", "ISTD", 3, "lecture"],\
           ["P&S", ["Tony"], ["Cl01"], "CC12","ISTD",3], ["P&S", ["Tony"], ["Cl02"], "CC12","ISTD",3], ["P&S", ["Tony"], ["Cl03"], "CC12","ISTD",3]]

total_duration = 0
for inp in inputls:
    total_duration = total_duration + inp[5]
print("total duration")
print(total_duration)  

        
def input_info(): 

    for e in inputls:
        if CourseClass.find(e[0]) == -1:
            CourseClass.classes.append(CourseClass(e[0],e[5],e[4]))
        if Professor.find(e[1]) == -1:
            Professor.professors.append(Professor(e[1]))
        if Group.find(e[2]) == -1:
            Group.groups.append(Group(e[2]))  
        if Room.find(e[3]) == -1:
            Room.rooms.append(Room(e[3]))
        if "lecture" in e:
            CourseClass.classes[CourseClass.find(e[0])].isLecture = True
        if "lab" in e:
            CourseClass.classes[CourseClass.find(e[0])].isLab = True

   
def get_cpg():
    input_info()
    len1 = len(inputls)
    for i in range(len1):
        
       cpg.append(CourseClass.find(inputls[i][0]))
       cpg.append(Professor.find(inputls[i][1]))
       cpg.append(Group.find(inputls[i][2]))
       cpg.append(Room.find(inputls[i][3]))


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 4):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2] + _cpg[i + 3])
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
    print(type(cpg))
    print(cpg)
    for _c in range(len(cpg)):
        #print(type(_c))
        
        if _c % 4 == 0:  # CourseClass
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')       
        elif _c % 4 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
        elif _c % 4 == 2:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')
        else:
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Room.rooms), '0')
    print("here")
    print(cpg)

    cpg = join_cpg_pair(cpg)
    print("there")
    print(cpg)
    print(Slot.slots)
    max_size = 0
    for s in Slot.slots:
        if len(s.block) > max_size:
            max_size = len(s.block)
            
    print(max_size)
    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
    print(slots)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


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


def slot_clash(a, b):
    if Slot.slots[int(slot_bits(a),2)].day == Slot.slots[int(slot_bits(b),2)].day:
        #print(Slot.slots[int(slot_bits(a),2)].day + " " +Slot.slots[int(slot_bits(b),2)].day)
        for i in range(len(Slot.slots[int(slot_bits(a),2)].block)):
            for j in range(len(Slot.slots[int(slot_bits(b),2)].block)):
                if Slot.slots[int(slot_bits(a),2)].block[i] == Slot.slots[int(slot_bits(b),2)].block[j]:
                    #print(Slot.slots[int(slot_bits(a),2)].block)
                    #print(Slot.slots[int(slot_bits(b),2)].block)
                    return 1
    return 0

def appropriate_cohort(chromosomes):
    scores = 0   
    for i in range(len(chromosomes)-1):
        course_cohort = CourseClass.classes[int(course_bits(chromosomes[i]),2)].code
        cohort_class = Group.groups[int(group_bits(chromosomes[i]),2)].name
        for j in range(i + 1, len(chromosomes)):
            if CourseClass.classes[int(course_bits(chromosomes[j]),2)].code == course_cohort and Group.groups[int(group_bits(chromosomes[j]),2)].name == cohort_class: 
                if Slot.slots[int(slot_bits(chromosomes[i]), 2)].day != Slot.slots[int(slot_bits(chromosomes[j]), 2)].day:
                    scores = scores + 1
    return scores

def appropriate_lecture(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c),2)].isLecture:
            #print("course class" + str(Professor.professors[int(professor_bits(_c),2)].name))
            course_code = CourseClass.classes[int(course_bits(_c),2)].code
            #print("course_code" + course_code)
            for _l in chromosomes:
                if CourseClass.classes[int(course_bits(_l),2)].code in course_code and CourseClass.classes[int(course_bits(_l),2)].isLecture == False:
                    if Slot.slots[int(slot_bits(_l),2)].day > Slot.slots[int(slot_bits(_c),2)].day:
                        scores = scores + 1
    return scores
            
def appropriate_lab(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c),2)].code:
            course_code = CourseClass.classes[int(course_bits(_c),2)].code
            #print("course_code" + course_code)
            for _l in chromosomes:
                if CourseClass.classes[int(course_bits(_l),2)].code in course_code and CourseClass.classes[int(course_bits(_l),2)].isLecture == False:
                    if Slot.slots[int(slot_bits(_l),2)].day < Slot.slots[int(slot_bits(_c),2)].day:
                        scores = scores + 1
    return scores
            
# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        profs = Professor.professors[int(professor_bits(chromosome[i]),2)].name
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            
            if slot_clash(chromosome[i], chromosome[j]):
                profs1 = Professor.professors[int(professor_bits(chromosome[j]),2)].name
                if len(profs) >= len(profs1):
                    for prof in profs:
                        if prof in profs1:
                            clash = True
                            break
                else:
                    for p1 in profs1:
                        if p1 in profs:
                            clash = True
                            break
        if not clash:
            scores = scores + 1
    return scores

def room_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):
        clash = False
        for j in range(i + 1, len(chromosome)):
            if slot_clash(chromosome[i], chromosome[j])\
                and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                clash = True
                #print("clash")
                break
        if not clash:
            scores = scores + 1
    return scores
# check that a group member takes only one class at a time.
def group_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        grps1 = Group.groups[int(group_bits(chromosomes[i]),2)].name
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]):
                grps2 = Group.groups[int(group_bits(chromosomes[j]),2)].name
                if len(grps1) >= len(grps2):
                    for grp in grps1:
                        if grp in grps2:
                            clash = True
                            break
                else:
                    for grp in grps2:
                        if grp in grps1:
                            clash = True
                            break
        if not clash:
            # print("These classes have no slot/lts clash")
            # print_chromosome(chromosomes[i])
            # print_chromosome(chromosomes[j])
            # print("____________")
            scores = scores + 1
    return scores

def check_slots(chromosomes):
    scores = 0   
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c),2)].duration != len(Slot.slots[int(course_bits(_c),2)].block):
            #print("wrong slot" + CourseClass.classes[int(course_bits(_c),2)].code)
            break
        else:
            scores = scores + 1
    return scores
        
def random_slot(cpg_c):
    temp_slot = random.choice(initial_slots)
    #print(initial_slots)
    #print(temp_slot)
    temp_block = temp_slot.block
    random_day = temp_slot.day
    #print(CourseClass.classes[int(course_bits(cpg_c),2)])
    temp_duration = CourseClass.classes[int(course_bits(cpg_c),2)].duration
    #print(temp_duration)
    temp_end = temp_slot.block[-1]
    random_start = random.randint(temp_block[0], temp_block[-1])
    while random_start + int(temp_duration) > temp_end:
        random_start = random.randint(temp_block[0], temp_block[-1])  
    temp_block = []
    random_end = random_start + int(temp_duration)
    for i in range(random_start, random_end):
        temp_block.append(i)
    
    random_slot = Slot(temp_block, random_day)
    if Slot.find(random_slot.block, random_slot.day) == -1:
        Slot.slots.append(random_slot)
        slots.append((bin(Slot.find(random_slot.block, random_slot.day))[2:]).rjust(bits_needed(Slot.slots) * ceil(log2(max_size)), '0'))
        
    #print(random_slot)   
    #print(slots[Slot.find(random_slot.block, random_slot.day)])
    return slots[Slot.find(random_slot.block, random_slot.day)]

def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + faculty_member_one_class(chromosomes)
    score = score + room_member_one_class(chromosomes)
    score = score + group_member_one_class(chromosomes)
    score = score + appropriate_cohort(chromosomes)
    score = score + appropriate_lecture(chromosomes)
    score = score + check_slots(chromosomes)
    return score / max_score

def cost(solution):
    # solution would be an array inside an array
    # it is because we use it as it is in genetic algorithms
    # too. Because, GA require multiple solutions i.e population
    # to work.
    return 1 / float(evaluate(solution))

def init_population(n):
    global cpg, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random_slot(_c))
        chromosomes.append(chromosome)
    return chromosomes


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    a = random.randint(0, len(chromosome) - 1)
    
    rand_slot = random_slot(chromosome[a])
    
    chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) +\
        group_bits(chromosome[a]) + lt_bits(chromosome[a]) + rand_slot

    # print("After mutation: ", end="")
    # printChromosome(chromosome)


def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    

def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()


def print_chromosome(chromosome):
    print(chromosome)
    print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)], " | ",
          Slot.slots[int(slot_bits(chromosome), 2)])
    
def print_chromosome_csv(max_chromosomes):
    label = ["Course", "Professors", "Class", "Room", " Day", "Start", "End"]
    out = open('schedule.csv','a', newline='')
    csv_write = csv.writer(out, dialect = 'excel')
    csv_write.writerow(label)
    for chromosome in max_chromosomes:
        csv_row = [CourseClass.classes[int(course_bits(chromosome), 2)],\
                   Professor.professors[int(professor_bits(chromosome), 2)],\
                   Group.groups[int(group_bits(chromosome), 2)],\
                   Room.rooms[int(lt_bits(chromosome), 2)],\
                   Slot.slots[int(slot_bits(chromosome), 2)].day,\
                   Slot.slots[int(slot_bits(chromosome),2)].block[0],\
                   Slot.slots[int(slot_bits(chromosome),2)].block[-1]]
        csv_write.writerow(csv_row)
        print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)], " | ",
          Slot.slots[int(slot_bits(chromosome), 2)])
    
    out.close()
    print("finish csv writing")
               


# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab

def ssn(solution):
    

    
    a = random.randint(0, len(solution) - 1)
    
    rand_slot = random_slot(solution[a])
    
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + lt_bits(solution[a]) + rand_slot 
    return [new_solution]

# Swapping Neighborhoods
# It randomy selects two classes and swap their time slots

def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + lt_bits(solution[a]) + slot_bits(solution[b])

    new_solution[b] = course_bits(solution[b]) + professor_bits(solution[b]) +\
        group_bits(solution[b]) + lt_bits(solution[b]) + temp 
    # print("Diff", solution)
    # print("Meiw", new_solution)
    return [new_solution]

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    alpha = 0.9
    T = 1.0
    T_min = 0.00001
    print ("here")
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])
    # print("Cost of original random solution: ", old_cost)
    # print("Original population:")
    # print(population)

    for __n in range(500):
        new_solution = swn(population[0])
        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            population = new_solution
            old_cost = new_cost
        T = T * alpha
    print(population)
    # print("Cost of altered solution: ", cost(population[0]))
    print("\n------------- Simulated Annealing --------------\n")
    print_chromosome_csv(population[0])
    print("Score: ", evaluate(population[0]))

def genetic_algorithm():
    generation = 0
    convert_input_to_bin()
    population = init_population(3)

    # print("Original population:")
    # print(population)
    print("\n------------- Genetic Algorithm --------------\n")
    while True:
        
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            print("Generations:", generation)
            print("Best Chromosome fitness value", evaluate(max(population, key=evaluate)))
            print("Best Chromosome: ", max(population, key=evaluate))
            label = ["Course", "Professors", "Class", "Room", "Start", "End"]
            out = open('schedule.csv','a', newline='')
            csv_write = csv.writer(out, dialect = 'excel')
            csv_write.writerow(label)
            for lec in max(population, key=evaluate):
                print_chromosome(lec)
            break
        
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                
                # selection(population[_c], len(cpg))
                mutate(population[_c])

        generation = generation + 1
        # print("Gen: ", generation)

    # print("Population", len(population))


def main():
    starttime = time.time()
    random.seed()
    genetic_algorithm()
    simulated_annealing()
    #print(Slot.slots)
    endtime = time.time()
    dtime = endtime - starttime
    
    print("time take" + str(dtime))
main()
