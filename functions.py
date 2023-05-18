import json

'''
Requirements for a valid timetable:

COURSES
1. Covered Terms per Year
2. Simultaneous blocking: share time slots
3. NotSimultaneous blocking: share time slots
4. Sequencing
5. Sections

STUDENTS
1. Sequencing
2. Max enrollment not exceeded
3. Priority

'''



'''

schedule: only courses
timetable: courses and students

Functions:

generate_course_schedule()
generate_timetable(schedule)
get_student_schedules(timetable)
is_valid(timetable)
score(timetable)
shuffle_students(timetable)
shuffle_courses(timetable)

'''



'''
returns a dictionary representing a schedule:

{

"sem1": [
            [course1, course2, ...] # block A
            [...] # B
            [...] # C
            [...] # D
        ]

"sem2": [...] same format as sem1

"outside_timetable": [course1, course2, ...]

}

sem1 and sem2 should contain only courses in the timetable,
and outside_timetable should contain only courses outside the timetable.

The generated timetable should satisfy the requirements listed under COURSES.

'''
def generate_course_schedule(course_info):
    for key in list(course_info.keys()):
        if len(course_info[key]['Students']) <= 5:
            print(course_info.pop(key))


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

def generate_timetable(schedule):
    pass


'''
Convenience method that returns a dictionary:
{
1000: [sem1A course, sem1B course, ..., sem2D course, outside timetable courses]
1001: []
...
}
'''
def get_student_schedules(timetable):

    student_schedules = {}

    for block in timetable["sem1"]:
        for course in block:
            for student in course:

                if student in student_schedules:
                    student_schedules[student].append(course)
                else:
                    student_schedules[student] = [course]
    
    for block in timetable["sem2"]:
        for course in block:
            for student in course:

                if student in student_schedules:
                    student_schedules[student].append(course)
                else:
                    student_schedules[student] = [course]

    for course in timetable["outside_timetable"]:
        for student in course:

            if student in student_schedules:
                student_schedules[student].append(course)
            else:
                student_schedules[student] = [course]

    return student_schedules


# return True if the timetable meets all of the hard requirements set by the school and False otherwise
# this method is probably inefficient and should not be used often
def is_valid(timetable):

    # read course information
    with open('course_info.json', 'r') as f:
        course_info = json.load(f)




# return the proportion of students who received all of their desired courses
def score(timetable):

    student_schedules = get_student_schedules(timetable)

    with open('student_requests.json', 'r') as f:
        student_requests = json.load(f)

    total_students = 0
    successful_students = 0
    success = True

    for student in student_requests:
        requested = student_requests[student]
        assigned = student_schedules[student]

        for course in requested:
            if course not in assigned:
                success = False
        
        total_students += 1

        if success:
            successful_students += 1
        
        success = True

    return successful_students / total_students

# make a small change to the timetable by moving around students. return a new valid timetable.
def shuffle_students(timetable):
    pass


# make a small change to the timetable by moving around courses. return a new valid timetable.
def shuffle_courses(timetable):
    pass
