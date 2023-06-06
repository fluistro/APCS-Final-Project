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


def generate_timetable(schedule):
     
    timetable = schedule_to_empty_timetable()

    student_schedules = {i for i in range(1000, 1838)}
    random.shuffle(student_schedules)

    for student in student_schedules:

        requests = student_requests[student]
        alternates = student_alternates[student]

        student_schedule = []
        for i in range(9):
            student_schedule.append([])

        for alternate in alternates:
            requests.remove(alternate)

        sorted_requests = sort_requests(requests, alternates)

        for request in sorted_requests:

            if len(student_schedule) == 8:
                break

            add(timetable, student, student_schedule, request)
        
        fill_random(timetable, student, student_schedule)

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
            if len(block[random_course]) < int(course_info[random_course]["Max Enrollment"]) and not course_info[random_course["Pre Reqs"]] and not course_info[random_course["Post Reqs"]]:
                block[random_course].append(student)
                student_schedule[index].append(random_course)
                return


# attempts to give a requested course to a student
def add(timetable, student, student_schedule, request):
    
    # automatically give the course if it's outside the timetable
    if course_info[request]["Outside Timetable"] == "true":
        timetable["outside timetable"][request].append(student)
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
    
    for index in free_blocks:
        block = get_block(index, timetable)
        if request in block:
            if len(block[request]) < int(course_info[request]["Max Enrollment"]):
                block[request].append(student)
                student_schedule[index].append(request)
                return
    
def get_block(index, timetable):
    if index == 0:
        return timetable["sem1"]["A"]
    if index == 1:
        return timetable["sem1"]["B"]
    if index == 2:
        return timetable["sem1"]["C"]
    if index == 3:
        return timetable["sem1"]["D"]
    if index == 4:
        return timetable["sem2"]["A"]
    if index == 5:
        return timetable["sem2"]["B"]
    if index == 6:
        return timetable["sem2"]["C"]
    if index == 7:
        return timetable["sem2"]["D"]

def sort_requests(requests, alternates):

    sorted_list = []

    sorting_dict = {request : int(course_info[request]["Covered Terms/Year"]) for request in requests}

    for request in requests:
        sorted_list.append(request)

    for alternate in alternates:
        sorted_list.append(alternate)


def schedule_to_empty_timetable(schedule):

    timetable = {

        "sem1":
        {
            "A":{},
            "B":{},
            "C":{},
            "D":{},
        },

        "sem2":
        {
            "A":{},
            "B":{},
            "C":{},
            "D":{},
        },

        "outside timetable":{}

    }

    for course in schedule["sem1"]["A"]:
        timetable["sem1"]["A"][course] = []
    for course in schedule["sem1"]["B"]:
        timetable["sem1"]["B"][course] = []
    for course in schedule["sem1"]["C"]:
        timetable["sem1"]["C"][course] = []
    for course in schedule["sem1"]["D"]:
        timetable["sem1"]["D"][course] = []
    for course in schedule["sem2"]["A"]:
        timetable["sem2"]["A"][course] = []
    for course in schedule["sem2"]["B"]:
        timetable["sem2"]["B"][course] = []
    for course in schedule["sem2"]["C"]:
        timetable["sem2"]["C"][course] = []
    for course in schedule["sem2"]["D"]:
        timetable["sem2"]["D"][course] = []
    for course in schedule["sem1"]["OT"]:
        timetable["outside timetable"][course] = []
    
    return timetable