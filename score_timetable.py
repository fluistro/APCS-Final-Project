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

with open('final_timetable.json', 'r') as f:
    timetable = json.load(f)

'''
returns a dictionary from a timetable:
{
    1000:[[sem1A course], [sem1B course],...,[outside timetable courses]]
    1001:[...]
    ...
}
'''
def get_student_schedules():

    student_schedules = {}

    for i in range(1000, 1838):
        student_schedules[str(i)] = [[], [], [], [], [], [], [], [], []]

    for i in range(8):
        block = timetable[i]
        for course in block:
            for student in block[course]:
                student_schedules[str(student)][i].append(course)

    for course in timetable[8]:
        for student in timetable[8][course]:
            student_schedules[str(student)][8].append(course)

    return student_schedules



student_schedules = get_student_schedules()
    
def print_course_names(course_list):
    names = [course_info[course_code]['course name'] for full_code in course_list for course_code in full_code.split('*')]
    print("\n".join(names) + "\n")

def print_schedule_course_names():
    print("SEMESTER 1 A BLOCK:")
    print_course_names(timetable[0].keys())
    print("SEMESTER 1 B BLOCK:")
    print_course_names(timetable[1].keys())
    print("SEMESTER 1 C BLOCK:")
    print_course_names(timetable[2].keys())
    print("SEMESTER 1 D BLOCK:")
    print_course_names(timetable[3].keys())
    print("SEMESTER 2 A BLOCK:")
    print_course_names(timetable[4].keys())
    print("SEMESTER 2 B BLOCK:")
    print_course_names(timetable[5].keys())
    print("SEMESTER 2 C BLOCK:")
    print_course_names(timetable[6].keys())
    print("SEMESTER 2 D BLOCK:")
    print_course_names(timetable[7].keys())

def print_schedule_num_blocks():
    print("SEMESTER 1 A BLOCK: " + str(len(timetable[0])) + " courses")
    print("SEMESTER 1 B BLOCK: " + str(len(timetable[1])) + " courses")
    print("SEMESTER 1 C BLOCK: " + str(len(timetable[2])) + " courses")
    print("SEMESTER 1 D BLOCK: " + str(len(timetable[3])) + " courses")
    print("SEMESTER 2 A BLOCK: " + str(len(timetable[4])) + " courses")
    print("SEMESTER 2 B BLOCK: " + str(len(timetable[5])) + " courses")
    print("SEMESTER 2 C BLOCK: " + str(len(timetable[6])) + " courses")
    print("SEMESTER 2 D BLOCK: " + str(len(timetable[7])) + " courses")

def print_student_info(student):

    print("STUDENT ID: " + student)
    print()

    # print requests
    print("REQUESTS")
    for request in student_requests[student]:
        print("  " + course_info[request]["course name"])
    print()

    # print alternates
    print("ALTERNATES")
    if student in student_alternates:
        for alternate in student_alternates[student]:
            print("  " + course_info[alternate]["course name"])
    else:
        print("  NONE")
    print()

    # print schedule

    schedule = []

    for i in range(8):
        try:
            schedule.append(student_schedules[student][i][0].split("*")[0])
        except:
            schedule.append("SPARE")


    print("0: completely not requested")
    print("1: requested as alternate")
    print("2: requested as top 8")
    print("SCHEDULE")
    for course in schedule:
        score = '0'
        if student in student_alternates and course in student_alternates[student]:
            score = '1'
        elif course in student_requests[student]:
            score = '2'

        if course == "SPARE":
            print("  SPARE")
        else:
            print("  " + score + " " + course_info[course]['course name'])

def get_student_success(id):

    student_schedule = student_schedules[id]
    num_requests_met = 0
    num_alts_met = 0

    for i in range(8):

        # they have a spare this block
        if not student_schedule[i]:
            continue

        course = student_schedule[i][0]

        for request in student_requests[id]:
            if request in course:
                num_requests_met += 1
                break
        
        if id in student_alternates:
            for alt in student_alternates[id]:
                if alt in course:
                    num_alts_met += 1
                    break
    
    return num_requests_met, num_alts_met + num_requests_met

def get_metrics():

    print_schedule_num_blocks()
    print()

    # numbers of students with a specific number of courses placed, with or without alts
    six_req = 0
    seven_req = 0
    eight_req = 0
    six_alt = 0
    seven_alt = 0
    eight_alt = 0

    total_requests = 0
    total_requests_or_alts = 0

    total_requests_met = 0
    total_requests_or_alts_met = 0

    for i in range(1000, 1838):

        requests_met, total_met = get_student_success(str(i))

        num_requests = 0
        num_requests_and_alts = 0

        for x in student_requests[str(i)]:
            if not course_info[x]["Outside Timetable"]:
                num_requests += 1
                num_requests_and_alts += 1

        if str(i) in student_alternates:
            for x in student_alternates[str(i)]:
                if not course_info[x]["Outside Timetable"]:
                    num_requests_and_alts += 1

        if num_requests > 8:
            num_requests = 8
        if num_requests_and_alts > 8:
            num_requests_and_alts = 8

        total_missed = num_requests_and_alts - total_met
        requests_missed = num_requests - requests_met

        if total_missed == 2:
            six_alt += 1
        elif total_missed == 1:
            seven_alt += 1
        elif total_missed == 0:
            eight_alt += 1

        if requests_missed == 2:
            six_req += 1
        elif requests_missed == 1:
            seven_req += 1
        elif requests_missed == 0:
            eight_req += 1

        total_requests += len(student_requests[str(i)])
        total_requests_or_alts += len(student_requests[str(i)])
        if str(i) in student_alternates:
            total_requests_or_alts += len(student_alternates[str(i)])

        total_requests_met += requests_met
        total_requests_or_alts_met += total_met

    print("number of requested courses placed/number of requested courses: " + str(total_requests_met / total_requests * 100) + "%")
    print("number of requested or alternate courses placed/number of requested or alternate courses: " + str(total_requests_or_alts_met / total_requests_or_alts * 100) + "%")
    print()

    print("NO ALTERNATES")
    print("0 missed: " + str(eight_req / 838 * 100) + "%")
    print("1 missed: " + str(seven_req / 838 * 100) + "%")
    print("2 missed: " + str(six_req / 838 * 100) + "%")
    print("TOTAL: " + str((six_req + seven_req + eight_req) / 838 * 100) + "%")
    print()

    print("WITH ALTERNATES")
    print("0 missed: " + str(eight_alt / 838 * 100) + "%")
    print("1 missed: " + str(seven_alt / 838 * 100) + "%")
    print("2 missed: " + str(six_alt / 838 * 100) + "%")
    print("TOTAL: " + str((six_alt + seven_alt + eight_alt) / 838 * 100) + "%")
    print()

    print("students with >3 courses missed (requested or alternate): " + str((1 - (six_alt + seven_alt + eight_alt) / 838) * 100) + "%")

'''times_courses_missed = {} # course_name : times_missed

def get_missed_courses(id):
    
    reqs_and_alts = student_requests[id]
    if id in student_alternates:
        reqs_and_alts += student_alternates[id]
        
    assigned_courses = []
    
    for x in student_schedules[id]:
        if x:
            assigned_courses += x[0].split("*")
    
    for x in reqs_and_alts:
        if x not in assigned_courses:
            
            course_name = course_info[x]["course name"]
            if course_name not in times_courses_missed:
                times_courses_missed[course_name] = 1
            else:
                times_courses_missed[course_name] = times_courses_missed[course_name] + 1
                
for i in range(1000, 1838):
    get_missed_courses(str(i))

sorted_missed = dict(sorted(times_courses_missed.items(), key=lambda x:x[1], reverse=True))

def get_course_code(name):
    for course in course_info:
        if name == course_info[course]["course name"]:
            return course

for x in sorted_missed:
    course_code = get_course_code(x)
    print(x + ": " + str(len(course_info[course_code]["Students"])) + " students requested; " + str(course_info[course_code]["Sections"]) + " sections; " + str(course_info[course_code]["Max Enrollment"]) + " students per section")'''

get_metrics()
while True:
    print()
    print("Enter Student ID: ")
    id = input()
    if id == '-1':
        break
    print_student_info(id)