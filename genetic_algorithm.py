import random
import json
import copy

with open('timetable.json', 'r') as f:
    sample_timetable = json.load(f)

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


# return a dictionary representing the course schedule (remove all students from timetable):
def get_course_schedule(timetable):
    
    schedule = copy.deepcopy(timetable)
    
    for block in schedule["sem1"]:
        for course in block:
            block[course].clear()
            
    for block in schedule["sem2"]:
        for course in block:
            block[course].clear()
    
    for course in schedule["outside timetable"]:
        schedule["outside timetable"][course].clear()
        
    return schedule


# combines two timetables into one timetable by randomly choosing students from both
# the timetables must have the same course schedule (only students will differ)
# does not check for validity of the resulting timetable
def cross(timetable_1, timetable_2):
    
    # get student schedules
    student_schedules_1 = get_student_schedules(timetable_1)
    student_schedules_2 = get_student_schedules(timetable_2)
    
    # what proportion of genes to choose from timetable_1
    proportion = 0.5
    num_students = int(proportion * 838)
    
    # choose students randomly from both timetables
    
    student_ids = [str(i) for i in range(1000, 1838)]
    
    dict_1 = {}
    dict_2 = {}
    
    for i in range(num_students):
        student = random.choice(student_ids)
        student_ids.remove(student)
        dict_1[student] = student_schedules_1[student]
        
    for student in student_ids:
        dict_2[student] = student_schedules_2[student]
        
    # combine students from both timetables into a new timetable
    
    new_timetable = get_course_schedule(timetable_1)
    
    for student in dict_1:
        insert_student(new_timetable, student, dict_1[student])
    for student in dict_2:
        insert_student(new_timetable, student, dict_2[student])

# inserts a student into an existing timetable
def insert_student(timetable, student_id, student_schedule):
    
    for i in range(4):
        timetable["sem1"][i][student_schedule[i]].append(student_id)
    
    for i in range(4):
        timetable["sem2"][i][student_schedule[i + 4]].append(student_id)
    
    timetable["outside timetable"][student_schedule[8]].append(student_id)
    
