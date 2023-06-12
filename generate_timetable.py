import json
import random
import csv
import copy

# import files

with open('student_requests.json', 'r') as f:
    student_requests = json.load(f)

with open('student_alternates.json', 'r') as f:
    student_alternates = json.load(f)

with open('master_schedule.json', 'r') as f:
    master_schedule = json.load(f)

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

'''
returns a list representing a master timetable:
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
def generate_course_schedule():

    # course_schedule only stores the courses
    course_schedule = []
    for i in range(9):
        course_schedule.append([])

    # {course_code: num_sections}
    # groups of simultaneous or not-simultaneous courses appear together with a * separating the course codes
    all_courseblock_codes = {}      # doesn't store OT courses

    already_checked = []

    
    # deal with courses with no simultaneous blocking
    for course in course_info:

        if course in already_checked:
            continue

        # auto assign outside timetable courses, no need to check anything further
        if course_info[course]['Outside Timetable'] == True:
            course_schedule[8].append(get_full_name(course))
            continue

        list_of_sim_courses = []

        for rule in sim_rules:
            if course in rule:
                list_of_sim_courses = rule
                break
            
        for x in list_of_sim_courses:
            already_checked.append(x)

        # if no course is simultaneous with this course
        if len(list_of_sim_courses) == 0:
            
            already_checked.append(course)
            all_courseblock_codes[course] = course_info[course]['Sections']
            sem_1 = False
            sem_2 = False
            linear = False
            
            if course_info[course]['Pre Req']:
                sem_1 = True
            if course_info[course]['Post Req']:
                sem_2 = True
            if course_info[course]['Base Terms/Year'] == 1:
                linear = True
            
            blocks = rand_blocks(course_info[course]['Sections'], sem_1, sem_2, linear)
            add_course_to_master(course_schedule, course, blocks)
            
            continue
        
        # if there are courses sim with this one
        else:

            full_sim_name = get_full_name(course) # names of all (non)simultaneous courses, separated by a *
            leftovers = {} # for if any of the courses have more sections than the others

            # get the maximum amount of simultaneous blocks that can appear
            max_simblock_sections = min([course_info[x]['Sections']] for x in list_of_sim_courses)[0]
            
            sem_1 = False
            sem_2 = False
            linear = False
            
            for sim_course in list_of_sim_courses:
                
                if course_info[sim_course]['Pre Req']:
                    sem_1 = True
                if course_info[sim_course]['Post Req']:
                    sem_2 = True
                if course_info[sim_course]['Base Terms/Year'] == 1:
                    linear = True
                    
                leftover_sections = course_info[sim_course]['Sections'] - max_simblock_sections
                if leftover_sections > 0:
                    leftovers[sim_course] = leftover_sections
            
            blocks = rand_blocks(max_simblock_sections, sem_1, sem_2, linear)
            add_course_to_master(course_schedule, full_sim_name, blocks)

            for course_with_leftover_sections in leftovers:
                blocks = rand_blocks(leftovers[course_with_leftover_sections], sem_1, sem_2, linear)
                add_course_to_master(course_schedule, course_with_leftover_sections, blocks)
                
    return course_schedule

# returns a list of indices representing random timeslots to place a course in
# note: no linear courses have sequencing rules
def rand_blocks(sections, sem_1, sem_2, linear):
    
    if sections > 8:
        sections = 8
    
    num_list = [i for i in range(0, 8)]
    sem_1_list = [i for i in range(0, 4)]
    sem_2_list = [i for i in range(4, 8)]
    random_blocks = []
    
    # linear courses appear [sections] times in each semester
    if linear:
        
        for i in range(sections):
        
            x = random.choice(sem_1_list)
            random_blocks.append(x)
            sem_1_list.remove(x)
            
            x = random.choice(sem_2_list)
            random_blocks.append(x)
            sem_2_list.remove(x)
            
        return random_blocks
    
    # courses with prerequisites/postrequisites must run at least once in semester 2/1
    # linear courses must appear in both
    if sem_1:
        x = random.randint(0, 3)
        random_blocks.append(x)
        num_list.remove(x)
    if sem_2:
        x = random.randint(4, 7)
        random_blocks.append(x)
        num_list.remove(x)
    
    while len(random_blocks) < sections:
        x = random.choice(num_list)
        random_blocks.append(x)
        num_list.remove(x)
        
    return random_blocks

def add_course_to_master(master_timetable, course_id, blocks):
    for block in blocks:
        master_timetable[block].append(course_id)

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
    
    '''
    available is a 2D list of the requested/alternate courses available in various blocks:
    [
        [courses in sem1A]
        [courses in sem1B]
        ...
    ]
    does not use * names
    '''
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
    
    return best_schedule_recursive(timetable, available, requests, alternates, requests + alternates, empty_schedule, [i for i in range(0, 8)])

def best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule, indices_to_add):
    
    # base cases
    if (not to_be_added) or (not indices_to_add):
        return current_schedule
    
    current_index = indices_to_add[0]
    
    next_steps = []
    for next_course_to_add in to_be_added:

        full_course_name = get_full_name(next_course_to_add)
        if full_course_name not in timetable[current_index]:
            full_course_name = next_course_to_add

        # if the course is linear, add a block of the course in both semesters
        # (this should only run when current_index is in semester 1)
        if course_info[next_course_to_add]["Base Terms/Year"] == 1 and current_index in [0, 1, 2, 3]:

            if next_course_to_add in available[current_index] and len(timetable[current_index][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:

                for i in [4, 5, 6, 7]:
                    if next_course_to_add in available[i] and len(timetable[i][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:

                        indices_to_add_copy = [] # remove indices where the linear course is going

                        for index in indices_to_add:
                            if index != current_index and index != i:
                                indices_to_add_copy.append(index)

                        to_be_added_copy = copy.deepcopy(to_be_added)
                        to_be_added_copy.remove(next_course_to_add)
                        
                        current_schedule_copy = copy.deepcopy(current_schedule)
                        current_schedule_copy[current_index] = next_course_to_add
                        current_schedule_copy[i] = next_course_to_add

                        next_steps.append(best_schedule_recursive(timetable, available, requests, alternates, to_be_added_copy, current_schedule_copy, indices_to_add_copy))
        
        if next_course_to_add in available[current_index] and len(timetable[current_index][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:
            
            to_be_added_copy = copy.deepcopy(to_be_added)
            to_be_added_copy.remove(next_course_to_add)
            
            current_schedule_copy = copy.deepcopy(current_schedule)
            current_schedule_copy[current_index] = next_course_to_add
            
            next_steps.append(best_schedule_recursive(timetable, available, requests, alternates, to_be_added_copy, current_schedule_copy, indices_to_add[1:]))
    
    # no course is available this block
    if not next_steps:
        current_schedule[current_index] = ""
        return best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule, indices_to_add[1:])
    
    # find the best schedule
    
    best_schedule = []
    best_score = 0
    
    for next_schedule in next_steps:
        score = score_student_schedule(requests, alternates, next_schedule)
        if score > best_score:
            best_schedule = next_schedule
            
    return best_schedule 
    
def score_student_schedule(requests, alternates, schedule):
    
    score = 0
    
    for i in range(8):
        if schedule[i] in requests:
            score += 1
        elif schedule[i] in alternates:
            score += 0.5
    
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
        timetable[8][get_full_name(outside_timetable_course)].append(id)




schedule = generate_course_schedule()
print(schedule)

timetable = schedule_to_empty_timetable(schedule)

ids = [i for i in range(1000, 1838)]
randomized_ids = random.shuffle(ids)

for i in randomized_ids:
    add_student(timetable, i, get_best_schedule(timetable, str(i)))
    print(i)

with open('recursion_timetable.json', 'w') as out_file:
    json.dump(timetable, out_file)

'''
returns a dictionary from a timetable:
{
    1000:[[sem1A course], [sem1B course],...,[outside timetable courses]]
    1001:[...]
    ...
}
'''
def get_student_schedules(timetable):

    student_schedules = {}

    for i in range(1000, 1838):
        student_schedules[str(i)] = [[], [], [], [], [], [], [], [], []]

    for i in range(8):
        block = timetable[i]
        for course in block:
            for student in block[course]:
                student_schedules[student][i].append(course)

    for course in timetable["outside_timetable"]:
        for student in timetable["outside_timetable"][course]:
            student_schedules[student][8].append(course)

    return student_schedules

def score(timetable, to_print):

    student_schedules = get_student_schedules(timetable)

    total_requests = 0
    total_alternates = 0
    successful_requests = 0
    successful_alternates = 0
    
    successful_students = 0
    success1 = True
    
    successful_students_alternates = 0
    success2 = True
    
    total_students = 0

    for student in student_requests:

        requested = student_requests[student]
        assigned = []
        
        for block in student_schedules[student]:
            for course in block:
                assigned.append(course)
        
        if student in student_alternates:
            alternates = student_alternates[student]
        else:
            alternates = []

        for course in alternates:

            total_alternates += 1
            for assigned_course in assigned:
                if course in assigned_course.split("*"):
                    successful_alternates += 1
                    break
            
        # if not an alternate
        for course in requested:
            total_requests += 1
            for assigned_course in assigned:
                if course in assigned_course.split("*"):
                    successful_requests += 1
                    break
                    
        for assigned_course in assigned:
            if (assigned_course not in alternates) and (assigned_course in requested):
                continue
            success1 = False
            if (assigned_course in alternates):
                continue
            success2 = False
            
        if len(assigned) < 8:
            success1 = False
            success2 = False   
                    
        if success1:
            successful_students += 1
        if success2:
            successful_students_alternates += 1
            
        success1 = True
        success2 = True
        total_students += 1
            
    #print("total requests: " + str(total_requests))
    
    if to_print:
        print("# requested courses placed / # requested courses: " + str(successful_requests / total_requests))
        print("# requested or alternate courses placed / # requested or alternate courses: " + str((successful_requests + successful_alternates) / (total_requests + total_alternates)))
        print("percent students with 8/8 courses (requested only): " + str(successful_students / total_students))
        print("percent students with 8/8 courses (requested or alternate): " + str(successful_students_alternates / total_students))
        print("weighted score: " + str((successful_requests + 0.5 * successful_alternates) / (total_requests)))
    return (successful_requests + 0.5 * successful_alternates) / (total_requests)

score(timetable, True)
