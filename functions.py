'''
timetable is a dictionary that represents a complete schedule:

{

"sem1": {
        "A": {"course1": [student1, student2, ...], 
              "course2": [...], 
              . . .
             }
        "B": {. . .}
        "C": {. . .}
        "D": {. . .}
        }

"sem2": {. . .} same format as sem1

"outside_timetable": {"course1": [students]
                      "course2": [...]
                      ...
                     }

}

'''

# return True if the timetable meets all of the hard requirements set by the school and False otherwise
def is_valid(timetable):
    pass


# return the proportion of students who received all of their desired courses
def score(timetable):
    pass


# make a small change to the timetable by moving around students
def shuffle_students(timetable):
    pass


# make a small change to the timetable by moving around courses
def shuffle_courses(timetable):
    pass
