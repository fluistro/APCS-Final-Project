import json

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

    # check that courses in a NotSimultaneous blocking are in the same time slot


    # check that courses in a simultaneous blocking are in the same time slot and do not have more students than their maximum capacity


    # check that no course is being offered too many times


    # check that no course has more students than its maximum capacity


    # check that students are taking courses in the correct sequencing


    # check that students get required courses (priority <= 20)


    


# return the proportion of students who received all of their desired courses
def score(timetable):
    pass


# make a small change to the timetable by moving around students
def shuffle_students(timetable):
    pass


# make a small change to the timetable by moving around courses
def shuffle_courses(timetable):
    pass
