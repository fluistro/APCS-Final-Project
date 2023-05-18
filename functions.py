import json

'''
Requirements for a valid timetable:

COURSES
1. Covered Terms per Year
2. Simultaneous blocking: share time slots
3. NotSimultaneous blocking: share time slots
4. Sequencing

STUDENTS
1. Sequencing
2. Max enrollment not exceeded
3. Priority

'''



'''
timetable is a dictionary that represents a complete schedule that may or may not be valid:

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

Assume that sem1 and sem2 contain only courses in the timetable,
and outside_timetable contains only courses outside the timetable.

'''
def generate_timetable():
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
def is_valid(timetable):

    # read course information
    with open('course_info.json', 'r') as f:
        course_info = json.load(f)




# return the proportion of students who received all of their desired courses
def score(timetable):
    pass


# make a small change to the timetable by moving around students
def shuffle_students(timetable):
    pass


# make a small change to the timetable by moving around courses
def shuffle_courses(timetable):
    pass
