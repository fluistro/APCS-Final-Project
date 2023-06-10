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

    # course_schedule only stores the courses, it doesn't give a shit about students
    course_schedule = []
    for i in range(9):
        course_schedule.append([])

    # contains key as course codes, value is the corresponding number of sections left for that course / combination of courses:
    # if this block of course is simultaneous with another, they all appear with * seperating them
    all_courseblock_codes = {}      # doesn't store OT courses

    course_info_modify = copy.deepcopy(course_info)

    already_checked = []

    
    # deal with courses with no simultaneous blocking
    for course in course_info:

        if course in already_checked:
            continue

        # outside timetable courses
        if course_info[course]['Outside Timetable'] == True:
            course_schedule[8].append(course)
            continue

        list_of_sim_courses = []

        for rule in sim_rules:
            if course in rule:
                list_of_sim_courses = rule

        # if no course is sim with this course
        if len(list_of_sim_courses) == 0:
            already_checked.append(course)
            all_courseblock_codes[course] = course_info[course]['Sections']
            continue
        
        # if there are courses sim with this one
        else:

            # count the maximum amount of simultaneous blocks that can appear
            max_simblock_sections = course_info[course]['Sections']
            for sim_course in list_of_sim_courses:
                if int(course_info_modify[sim_course]['Sections']) < int(max_simblock_sections):
                    max_simblock_sections = int(course_info_modify[sim_course]['Sections'])

            # generate a string, which is the course code of these simultaneous courses, sperated with a *
            cur_sim_courses_codes = course
            for sim_course in list_of_sim_courses:
                cur_sim_courses_codes = cur_sim_courses_codes + "*" + sim_course

            # put the simultaneous blocks into all blocks
            all_courseblock_codes[cur_sim_courses_codes] = max_simblock_sections

            for sim_course in list_of_sim_courses:

                already_checked.append(sim_course)
                leftover = int(course_info[sim_course]["Sections"]) - max_simblock_sections
                if leftover > 0:
                    all_courseblock_codes[sim_course] = leftover

    for course_block in all_courseblock_codes:
        current_used_blocks = []                                            # to store all the blocks this course takes up

        # deal with blocks with sections > 8
        if all_courseblock_codes[course_block] > 8:

            extra_sections = all_courseblock_codes[course_block] - 8
            current_used_blocks = []

            for i in range(extra_sections):

                # put the extra sections into course_schedule first
                rand_block = return_rando_block(current_used_blocks)
                course_schedule[rand_block].append(course_block)
                current_used_blocks.append(rand_block)
                all_courseblock_codes[course_block] = 8

            current_used_blocks = []

        # non simultaneous courses
        if not '*' in course_block:
            if course_info_modify[course_block]['Outside Timetable'] == True:
                continue

        # deal with band and PE 9 and 10

        if 'MPHED10G-L' in course_block or 'MPHED10B-L' in course_block or 'MPHE-09B-L' in  course_block or 'MPHE-09G-L' in course_block:
            continue

        if 'XBA--09B-L' in course_block:
            rand_block = random.randint(0, 3)
            course_schedule[rand_block].append(course_block)    # put band 9 into a sem 1 block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09B-L')    # put boys pe in sem 2 same block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09G-L')    # girls ''
            continue
        if 'MMUCB10--L' in course_block :
            rand_block = return_rando_block(['2 A', '2 B', '2 C', '2 D' ]).split(' ') 
            course_schedule['sem1'][letter_to_num(rand_block[1])].append(course_block)    # put band 10 into a sem 1 block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHED10B-L')
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHED10G-L')
            continue

        # the NORMAL courses
        for j in range(int(all_courseblock_codes[course_block])):                # goes through all available sections of this course
            rand_block = return_rando_block(current_used_blocks).split(' ')                                # [semester#, block#]
            course_schedule['sem' + rand_block[0]][letter_to_num(rand_block[1])].append(course_block)      # put this course into the randomized 
            current_used_blocks.append(rand_block[0] + ' ' + rand_block[1])
        

# takes in a list of unvailable blocks, and spits out a random block (int 0-8) among the available blocks
def return_rando_block(used_blocks):

    # initialize the blocks that have less than 42 blocks in them
    current_available_blocks = [i for i in range(8)]

    for block in used_blocks:
        current_available_blocks.remove(block)
    
    if len(current_available_blocks) == 0:
        return -1

    return random.choice(current_available_blocks)


def letter_to_num(letter):
    if letter == 'A':
        return 0
    elif letter == 'B':
        return 1
    elif letter == 'C':
        return 2
    else:
        return 3
    
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
    if student_alternates[student]:
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
            for c in timetable[i]:
                if course in c:
                    available[i].append(course)
    
    return best_schedule_recursive(timetable, available, requests, alternates, requests + alternates, empty_schedule, 0)

def best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule, current_index):
    
    # base cases
    if (not to_be_added) or current_index > 7:
        return current_schedule
    
    next_steps = []
    for next_course_to_add in to_be_added:
        
        full_course_name = get_full_name(next_course_to_add)
        
        if next_course_to_add in available[current_index] and len(timetable[current_index][full_course_name]) <= course_info[next_course_to_add]["Max Enrollment"]:
            
            to_be_added_copy = copy.deepcopy(to_be_added)
            to_be_added_copy.remove(next_course_to_add)
            
            current_schedule_copy = copy.deepcopy(current_schedule)
            current_schedule_copy[current_index].append(next_course_to_add)
            
            next_steps.append(best_schedule_recursive(timetable, available, requests, alternates, to_be_added_copy, current_schedule_copy, current_index + 1))
    
    # no course is available this block
    if not next_steps:
        current_schedule[current_index].append("")
        return best_schedule_recursive(timetable, available, requests, alternates, to_be_added, current_schedule, current_index + 1)
    
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
            timetable[i][get_full_name(schedule[i])].append(id)
            
    for outside_timetable_course in schedule[8]:
        timetable[8][get_full_name(outside_timetable_course)].append(id)


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

    for i in range(4):
        block = timetable["sem1"][i]
        for course in block:
            for student in block[course]:
                student_schedules[student][i].append(course)
    
    for i in range(4):
        block = timetable["sem2"][i]
        for course in block:
            for student in block[course]:
                student_schedules[student][i + 4].append(course)

    for course in timetable["outside_timetable"]:
        for student in timetable["outside_timetable"][course]:
            student_schedules[student][8].append(course)

    return student_schedules

