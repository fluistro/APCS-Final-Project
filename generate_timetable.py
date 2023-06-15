import json
import random
import csv
import copy

# import files

with open('student_requests.json', 'r') as f:
    student_requests = json.load(f)

with open('student_alternates.json', 'r') as f:
    student_alternates = json.load(f)

# make course_info json info global
with open('courses.json') as f:
        course_info = json.load(f)
        
# remove alternates from student_requests
for student in student_requests:
    if student in student_alternates:
        requests = student_requests[student]
        for alternate in student_alternates[student]:
            requests.remove(alternate)

# returns a 2D list representing all courses that must be blocked (non)simultaneously
def get_simultaneous_rules():

    simultaneous_rules = []

    for course in course_info:

        already_in_rules = False

        if course_info[course]["Simultaneous"] or course_info[course]["Not Simultaneous"]:

            sim_courses = [course] + [x for x in course_info[course]["Simultaneous"]] + [x for x in course_info[course]["Not Simultaneous"]]

            # check if course is already in the rules
            for rule in simultaneous_rules:
                for current_course in sim_courses:

                    if current_course in rule:

                        already_in_rules = True

                        # add any courses that should be part of the rule
                        for x in sim_courses:
                            if x not in rule:
                                rule.append(x)
                        
                        break

                if already_in_rules:
                    break
            
            if not already_in_rules:
                simultaneous_rules.append([x for x in sim_courses])

    return simultaneous_rules

sim_rules = get_simultaneous_rules()

def get_full_name(course):
    
    for rule in sim_rules:
        if course in rule:
            name = ""
            for course in rule:
                name += course + "*"
            name = name[:-1]
            return name
    return course

"""
generates a timetable:
[
    {}
]
"""
def generate_timetable(schedule):
     
    timetable = schedule_to_empty_timetable(schedule)

    student_ids = [str(i) for i in range(1000, 1838)]
    random.shuffle(student_ids)

    for student in student_ids:

        student_schedule = get_best_schedule(timetable, student)
        add_student(timetable, student, student_schedule)

    return timetable

def schedule_to_empty_timetable(schedule):

    timetable = []
    for i in range(9):
        timetable.append({})
        for course in schedule[i]:
            timetable[i][course] = []
    return timetable

'''
return a 2D list representing the best possible schedule for a student (may have spares, represented by ""):
[
sem1A course
sem1B course
...
sem2D course
[outside timetable courses]
]
'''
def get_best_schedule(timetable, student):
    
    requests = student_requests[student]
    alternates = []
    if student in student_alternates:
        alternates = student_alternates[student]
    
    empty_schedule = ["" for i in range(8)]
    outside_timetable_courses = []
    
    for course in requests + alternates:
        if course_info[course]["Outside Timetable"]:
            outside_timetable_courses.append(course)
    
    empty_schedule.append(outside_timetable_courses)
    
    available = get_available_blocks(timetable, requests, alternates)
    
    indices = [i for i in range(0, 8)]
    random.shuffle(indices)

    return best_schedule_recursive(timetable, available, requests, alternates, requests + alternates, empty_schedule, indices)

'''
    available is a 2D list of the requested/alternate courses available in various blocks:
    [
        [courses in sem1A]
        [courses in sem1B]
        ...
    ]
    does not use * names
'''
def get_available_blocks(timetable, requests, alternates):
    available = []
    
    for i in range(8):

        available.append([])

        for course in requests + alternates:

            sem_1 = False
            sem_2 = False
            
            if (course_info[course]["Post Req"]):
                for post_req in course_info[course]["Post Req"]:
                    if post_req in requests + alternates:
                        # if course must be in semester 1
                        sem_1 = True
                        break

            if (course_info[course]["Pre Req"]):
                for post_req in course_info[course]["Pre Req"]:
                    if post_req in requests + alternates:
                        # if course must be in semester 2
                        sem_2 = True
                        break

            if sem_1 and (i not in [0, 1, 2, 3]):
                continue
            if sem_2 and (i not in [4, 5, 6, 7]):
                continue

            for c in timetable[i]:
                if course in c:
                    available[i].append(course)
                    
    return available

def best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule, indices_to_add):
    
    # base cases
    if (not to_be_added) or (not indices_to_add):
        return current_schedule
    
    current_index = indices_to_add[0]
    
    next_steps = [] # list of all schedules that can be made by building on current_schedule
    
    for next_course_to_add in to_be_added:

        full_course_name = get_full_name(next_course_to_add)
        if full_course_name not in timetable[current_index]:
            full_course_name = next_course_to_add

        # if the course is linear, add a block of the course in both semesters
        # (this should only run when current_index is in semester 1)
        if course_info[next_course_to_add]["Base Terms/Year"] == 1 and current_index in [0, 1, 2, 3]:

            if next_course_to_add in available[current_index] and len(timetable[current_index][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:

                for i in [4, 5, 6, 7]:
                    if i in indices_to_add and next_course_to_add in available[i] and len(timetable[i][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:

                        indices_to_add_copy = [] # remove indices where the linear course is going

                        for index in indices_to_add:
                            if index != current_index and index != i:
                                indices_to_add_copy.append(index)

                        to_be_added_copy = copy.deepcopy(to_be_added)
                        to_be_added_copy.remove(next_course_to_add)
                        
                        current_schedule_copy = copy.deepcopy(current_schedule)
                        current_schedule_copy[current_index] = next_course_to_add
                        current_schedule_copy[i] = next_course_to_add

                        if next_course_to_add == "MIMCB11--L":
                            pass

                        next_steps.append(best_schedule_recursive(timetable, available, requests, alternates, to_be_added_copy, current_schedule_copy, indices_to_add_copy))
        
        elif next_course_to_add in available[current_index] and len(timetable[current_index][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:
            
            to_be_added_copy = copy.deepcopy(to_be_added)
            to_be_added_copy.remove(next_course_to_add)
            
            current_schedule_copy = copy.deepcopy(current_schedule)
            current_schedule_copy[current_index] = next_course_to_add

            indices_to_add_copy = []
            for index in indices_to_add:
                if index != current_index:
                    indices_to_add_copy.append(index)
            
            next_steps.append(best_schedule_recursive(timetable, available, requests, alternates, to_be_added_copy, current_schedule_copy, indices_to_add_copy))
    
    # no course is available this block
    if not next_steps:

        current_schedule_copy = copy.deepcopy(current_schedule)
        current_schedule_copy[current_index] = ""

        indices_to_add_copy = []
        for index in indices_to_add:
            if index != current_index:
                indices_to_add_copy.append(index)

        return best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule_copy, indices_to_add_copy)
    
    # find the best schedule
    
    best_schedule = []
    best_score = 0
    
    for next_schedule in next_steps:
        score = score_student_schedule(requests, alternates, next_schedule)
        if score >= best_score:
            if score == 8:
                return next_schedule
            best_score = score
            best_schedule = copy.deepcopy(next_schedule)
    
    return best_schedule 
    
def score_student_schedule(requests, alternates, schedule):
    
    score = 0
    
    for i in range(8):
        if schedule[i] in requests:
            score += 1
        elif schedule[i] in alternates:
            score += 0.1
    
    return score
            

# adds a student (schedule already made) to the timetable
def add_student(timetable, id, schedule):
    
    for i in range(8):
        if schedule[i] != "":
            try:
                timetable[i][get_full_name(schedule[i])].append(id)
            except:
                timetable[i][schedule[i]].append(id)
            
    for outside_timetable_course in schedule[8]:
        timetable[8][outside_timetable_course].append(id)

'''
a list representing a master timetable:
[
    [sem1A courses]
    [sem1B courses]
    [sem1C courses]
    [sem1D courses]
    [sem2A courses]
    [sem2B courses]
    [sem2C courses]
    [sem2D courses]
    [outside timetable courses]
]
'''

with open('master_schedule.json', 'r') as f:
    schedule = json.load(f)

for block in schedule:
    for i in range(len(block)):
        if "*" in block[i]:
            block[i] = get_full_name(block[i].split("*")[0])

# generate timetables

timetable_list = []

#for x in range(10):

timetable = schedule_to_empty_timetable(schedule)

ids = [i for i in range(1000, 1838)]
random.shuffle(ids)
counter = 0

for i in ids:
    add_student(timetable, i, get_best_schedule(timetable, str(i)))
        
    #timetable_list.append(timetable)
    
    #print(str(x) + " timetables generated")

with open('final_timetable.json', 'w') as out_file:
    json.dump(timetable, out_file)