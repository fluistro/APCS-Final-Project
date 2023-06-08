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

# returns a 2D list representing all courses that must be blocked simultaneously
def get_simultaneous_rules():

    simultaneous_rules = []

    for course in course_info:

        already_in_rules = False

        if course_info[course]["Simultaneous"]:
            sim_courses = [course] + [x for x in course_info[course]["Simultaneous"]]

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

    sim_rules = get_simultaneous_rules()

    # contains key as course codes, value is the corresponding number of sections left for that course / combination of courses:
    # if this block of course is simultaneous with another, they all appear with * seperating them
    all_courseblock_codes = {}      # doesn't store OT courses

    course_info_modify = copy.deepcopy(course_info)

    
    # deal with courses with no simultaneous blocking
    for course in course_info:

        # outside timetable courses
        if course_info[course]['Outside Timetable'] == True:
            course_schedule[8].append(course)
            continue

        # skip if we have already looked at this course
        if course_info_modify[course]['Sections'] == 0:
            continue

        list_of_sim_courses = []

        for rule in sim_rules:
            if course in rule:
                list_of_sim_courses = rule

        # if no course is sim with this course
        if len(list_of_sim_courses) == 0:
            all_courseblock_codes[course] = course_info[course]['Sections']
            continue
        
        # if there are courses sim with this one
        else:

            # count the maximum amount of simultaneous blocks that can appear
            max_simblock_sections = course_info[course]['Sections']
            for sim_course in list_of_sim_courses:
                if int(course_info_modify[sim_course]['Sections']) < int(max_simblock_sections):
                    max_simblock_sections = course_info_modify[sim_course]['Sections']

            # generate a string, which is the course code of these simultaneous courses, sperated with a *
            cur_sim_courses_codes = course
            for sim_course in list_of_sim_courses:
                cur_sim_courses_codes = cur_sim_courses_codes + "*" + sim_course

            # put the simultaneous blocks into all blocks
            all_courseblock_codes[cur_sim_courses_codes] = max_simblock_sections

            # minus the used up sections of these courses
            cur_sections = course_info_modify[course]['Sections']
            new_sections = int(cur_sections) - int(max_simblock_sections)
            course_info_modify[course]['Sections'] = new_sections               # the course itself
            for sim_course in list_of_sim_courses:                              # the sim courses w/ tis course
                cur_sections = course_info_modify[sim_course]['Sections']
                new_sections = int(cur_sections) - int(max_simblock_sections)
                course_info_modify[sim_course]['Sections'] = new_sections

            # now deal with the possible extra available sections of the sim courses

            # current course
            if course_info_modify[course]['Sections'] == 0:
                continue
            else:
                all_courseblock_codes[course] = course_info_modify[course]['Sections']

            # all the sim courses
            for sim_course in list_of_sim_courses:
                if course_info_modify[sim_course]['Sections'] == 0:
                    continue
                else:
                    all_courseblock_codes[sim_course] = course_info_modify[sim_course]['Sections']
                    course_info_modify[sim_course]['Sections'] = 0

    for course_block in all_courseblock_codes:
        current_used_blocks = []                                            # to store all the blocks this course takes up

        # deal with blocks with sections > 8
        if int(all_courseblock_codes[course_block]) > 8:
            extra_sections = int(all_courseblock_codes[course_block]) - 8
            current_used_blocks = []
            for i in range(extra_sections):

                # put the extra sections into course_schedule first
                rand_block = return_rando_block(current_used_blocks).split(' ')                    # [semester#, block#]
                course_schedule['sem' + rand_block[0]][letter_to_num(rand_block[1])].append(course_block)      # put this course into the randomized 
                current_used_blocks.append(rand_block[0] + ' ' + rand_block[1])
                all_courseblock_codes[course_block] = 8
            current_used_blocks = []

        if not '*' in course_block:
            if course_info_modify[course_block]['Outside Timetable'] == True:
                continue

        # take care of stupid(not) BANDDDDD and PEEEEEEE

        if 'MPHED10G-L' in course_block or 'MPHED10B-L' in course_block or 'MPHE-09B-L' in  course_block or 'MPHE-09G-L' in course_block:
            continue
        if 'XBA--09B-L' in course_block:
            rand_block = return_rando_block(['2 A', '2 B', '2 C', '2 D' ]).split(' ') 
            course_schedule['sem1'][letter_to_num(rand_block[1])].append(course_block)    # put band 9 into a sem 1 block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09B-L')    # put boys pe in sem 2 same block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09G-L')    # girls ''
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
        


'''
timetable is a dictionary that adds students to schedule:

{

"sem1": [
            {"course1": [student1, student2, ...], 
                "course2": [...], 
                ...
            } # block A
            {...} # B
            {...} # C
            {...} # D
        ]

"sem2": [...] same format as sem1

"outside_timetable": {"course1": [students]
                      "course2": [...]
                      ...
                     }

}

The timetable should meet all requirements under STUDENTS.
'''

# takes in a list of unvailable blocks, and spits out a random block among the available blocks
def return_rando_block(not_these_blocks):

    # initialize the blocks that have less than 42 blocks in them
    current_available_blocks = ['1 A', '1 B', '1 C', '1 D', '2 A', '2 B', '2 C', '2 D']

    for blocks in not_these_blocks:
        current_available_blocks.remove(blocks)
    
    if len(current_available_blocks) == 0:
        return -1

    rand = random.randint(0, len(current_available_blocks)-1)

    return current_available_blocks[rand]


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

"""
def generate_timetable(schedule):
     
    timetable = schedule_to_empty_timetable(schedule)

    student_ids = [str(i) for i in range(1000, 1838)]
    random.shuffle(student_ids)

    student_schedules = {}

    for student in student_ids:

        requests = student_requests[student]
        alternates = []
        if student in student_alternates:
            alternates = student_alternates[student]

        student_schedule = []
        for i in range(9):
            student_schedule.append([])

        for alternate in alternates:
            if alternate in requests:
                requests.remove(alternate)

        sorted_requests = sort_requests(requests, alternates)

        for request in sorted_requests:

            if len(student_schedule) == 8:
                break

            add(timetable, student, student_schedule, request)
        
        fill_random(timetable, student, student_schedule)

        student_schedules[student] = student_schedule

    return timetable

# fills any empty blocks with random courses
def fill_random(timetable, student, student_schedule):
    
    free_blocks = [] # indices of free blocks

    for i in range(0,8):
        if not student_schedule[i]:
            free_blocks.append(i)

    for index in free_blocks:
        block = get_block(index, timetable)
        while True:
            random_course = random.choice(list(block.keys()))
            single_course = random_course.split("*")[0]
            if len(block[random_course]) < int(course_info[single_course]["Max Enrollment"]) and not course_info[single_course]["Pre Req"] and not course_info[single_course]["Post Req"]:
                block[random_course].append(student)
                student_schedule[index].append(random_course)
                return


# attempts to give a requested course to a student
def add(timetable, student, student_schedule, request):
    
    # automatically give the course if it's outside the timetable
    if course_info[request]["Outside Timetable"]:
        timetable["outside_timetable"][request].append(student)
        student_schedule[8].append(request)
        return
    
    free_blocks = [] # indices of free blocks
    s1 = False
    s2 = False

    # course must be in s2
    if course_info[request]["Pre Req"]:
        for prerequisite in course_info[request]["Pre Req"]:
            if prerequisite in student_requests[student]:
                s2 = True
                break

    # course must be in s1
    if course_info[request]["Post Req"]:
        for postrequisite in course_info[request]["Post Req"]:
            if postrequisite in student_requests[student]:
                s1 = True
                break

    if s1:
        for i in range(0,4):
            if not student_schedule[i]:
                free_blocks.append(i)
    elif s2:
        for i in range(4,8):
            if not student_schedule[i]:
                free_blocks.append(i)
    else:
        for i in range(0,8):
            if not student_schedule[i]:
                free_blocks.append(i)

    random.shuffle(free_blocks)

    # linear course
    if course_info[request]["Base Terms/Year"] == "1":
        for index in range(4):
            if index in free_blocks and (index + 4) in free_blocks:
                block_1 = get_block(index, timetable)
                block_2 = get_block(index + 4, timetable)
                if request in block_1 and request in block_2:
                    if len(block_1[request]) < int(course_info[request]["Max Enrollment"]) and len(block_2[request]) < int(course_info[request]["Max Enrollment"]):
                        block_1[request].append(student)
                        block_2[request].append(student)
                        student_schedule[index].append(request)
                        student_schedule[index + 4].append(request)
                        return
        return
                
    
    for index in free_blocks:
        block = get_block(index, timetable)
        if request in block:
            if len(block[request]) < int(course_info[request]["Max Enrollment"]):
                block[request].append(student)
                student_schedule[index].append(request)
                return
    
def get_block(index, timetable):
    if index <= 3:
        return timetable["sem1"][index]
    return timetable["sem2"][index - 4]

def sort_requests(requests, alternates):

    sorted_list = []

    temp = {request : int(course_info[request]["Covered Terms/Year"]) for request in requests}
    sorted_dict = dict(sorted(temp.items(), key=lambda x:x[1]))


    for request in sorted_dict:
        sorted_list.append(request)

    for alternate in alternates:
        sorted_list.append(alternate)

    return sorted_list


def schedule_to_empty_timetable(schedule):

    timetable = {
        "sem1":[{}, {}, {}, {}],
        "sem2":[{}, {}, {}, {}],
        "outside_timetable":{}
    }

    for course in schedule["sem1"]["A"]:
        timetable["sem1"][0][course] = []
    for course in schedule["sem1"]["B"]:
        timetable["sem1"][1][course] = []
    for course in schedule["sem1"]["C"]:
        timetable["sem1"][2][course] = []
    for course in schedule["sem1"]["D"]:
        timetable["sem1"][3][course] = []
    for course in schedule["sem2"]["A"]:
        timetable["sem2"][0][course] = []
    for course in schedule["sem2"]["B"]:
        timetable["sem2"][1][course] = []
    for course in schedule["sem2"]["C"]:
        timetable["sem2"][2][course] = []
    for course in schedule["sem2"]["D"]:
        timetable["sem2"][3][course] = []
    for course in schedule["sem1"]["OT"]:
        timetable["outside_timetable"][course] = []
    
    return timetable

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

