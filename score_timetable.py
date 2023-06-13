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
                student_schedules[str(student)][i].append(course)

    for course in timetable[8]:
        for student in timetable[8][course]:
            student_schedules[str(student)][8].append(course)

    return student_schedules

def score(timetable, to_print):

    student_schedules = get_student_schedules(timetable)

    total_requests = 0
    total_alternates = 0
    successful_requests = 0
    successful_alternates = 0
    
    successful_students = 0
    student_is_successful = True
    
    successful_students_alternates = 0
    student_is_successful_with_alternates = True
    
    total_students = 0

    for student in student_schedules:
        
        requests = student_requests[student]
        alternates = []
        if student in student_alternates:
            alternates = student_alternates[student]
            
        total_requests += len(requests)
        total_alternates += len(alternates)
            
        # go through each block in the student's schedule
        for i in range(8):
            
            block = student_schedules[student][i]
            
            # spare
            if not block:
                student_is_successful = False
                student_is_successful_with_alternates = False
                continue
            
            # alternate, not requested
            for alternate in alternates:
                if alternate in block[0]:
                    student_is_successful = False
                    successful_alternates += 1
                    break
            
            for request in requests:
                if request in block[0]:
                    successful_requests += 1
                    break
                    
        if student_is_successful:
            successful_students += 1
        if student_is_successful_with_alternates:
            successful_students_alternates += 1
            
        student_is_successful = True
        student_is_successful_with_alternates = True
        total_students += 1
        
        
    
    if to_print:
        print("# requested courses placed / # requested courses: " + str(successful_requests / total_requests * 100) + "%")
        print("# requested or alternate courses placed / # requested or alternate courses: " + str((successful_requests + successful_alternates) / (total_requests + total_alternates) * 100) + "%")
        print("percent students with 8/8 courses (requested only): " + str(successful_students / total_students * 100) + "%")
        print("percent students with 8/8 courses (requested or alternate): " + str(successful_students_alternates / total_students * 100) + "%")
        print("weighted score: " + str((successful_requests + 0.5 * successful_alternates) / (total_requests) * 100) + "%")
    return (successful_requests + 0.5 * successful_alternates) / (total_requests)

with open('recursion_timetable_not_overloaded.json', 'r') as f:
    timetable = json.load(f)

student_schedules = get_student_schedules(timetable)
    
def print_course_names(course_list):
    names = [course_info[course_code]['course name'] for full_code in course_list for course_code in full_code.split('*')]
    print("\n".join(names) + "\n")

def print_schedule():
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

def print_student_info(student):

    print("STUDENT ID: " + student)
    print()

    # print requests
    print("REQUESTS")
    for request in student_requests[student]:
        print(course_info[request]["course name"])
    print()

    # print alternates
    print("ALTERNATES")
    if student in student_alternates:
        for alternate in student_alternates[student]:
            print(course_info[alternate]["course name"])
    else:
        print("NONE")
    print()

    # print schedule

    schedule = []

    for i in range(8):
        try:
            schedule.append(course_info[student_schedules[student][i][0].split("*")[0]]["course name"])
        except:
            schedule.append("SPARE")

    print("SCHEDULE")
    for course in schedule:
        print(course)

        
print_student_info("1527")