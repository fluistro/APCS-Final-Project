import json
import random

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
    
  
    with open('course.json') as f:
        course_info = json.load(f)
    with open('student_requests.json') as f:
        student_info = json.load(f)

    print(course_info)
    
    # inside timetable courses
        # go through student info one student at a time
            # Sort their courses by priority
            # Start with most prioritized courses
                # Check if student meets sequencing, and pre req if have two courses that have order
                    # find course in schedule that does not contridict with student's current schedule and check if course is at max enrollment
                        # add student
                    # if there is no space in any of the schedule for this course, 
                        # Skip this course and go onto the next prioritized one (assuming that there will always be enough space for required courses)
                # If doesn't meet sequencing / pre req
                    # Skip this course and go onto the next prioritized one (assuming student will always have required courses with right sequence and pre req ex. no english 9, 10, 11)


    # outside timetable courses
        # check sequencing and pre req
            # add course
        # doesn't meet just skip

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
# does not shuffle students in outside timetable courses.
def shuffle_students(timetable):

    n = 50

    # swap n pairs of students
    for i in range(n):

        # find some way to select students such that switching them is good
        # currently chooses randomly
        # does not yet check for spares

        timeslot = random.randint(0,7)
        student1 = random.randint(1000,1837)
        student2 = random.randint(1000,1837)

        if (student1 == student2):
            while (student1 == student2):
                student2 = random.randint(1000,1837)

        student_schedules = get_student_schedules(timetable)

        student1_course = student_schedules[student1][timeslot]
        student2_course = student_schedules[student2][timeslot]


        # swap the two students in the timeslot
        if 0 <= timeslot <= 3:
            timetable["sem1"][timeslot][student1_course].append(student2)
            timetable["sem1"][timeslot][student1_course].remove(student1)
            timetable["sem1"][timeslot][student2_course].append(student1)
            timetable["sem1"][timeslot][student2_course].remove(student2)
        elif 4 <= timeslot <= 7:
            timeslot -= 4
            timetable["sem2"][timeslot][student1_course].append(student2)
            timetable["sem2"][timeslot][student1_course].remove(student1)
            timetable["sem2"][timeslot][student2_course].append(student1)
            timetable["sem2"][timeslot][student2_course].remove(student2)
    
    return timetable


# make a small change to the timetable by moving around courses. return a new valid timetable.
def shuffle_courses(timetable):
    
    with open('course.json') as f:
        course_info = json.load(f)

    # pick course 1

    # pick a random block
    timeslot1 = random.randint(0,7)

    semester1 = ""

    if (timeslot1 <= 3):
        semester1 = "sem1"
    else:
        semester1 = "sem2"
        timeslot1 -= 4

    while True:

        # pick a random course in that block. Does not select courses with requirements for blocking and sequencing
        course1, students1 = random.choice(list(timetable[semester1][timeslot1].items()))

        # check for blocking/sequencing requirements
        if course_info[course1]['Prereqs'] or course_info[course1]['Postreqs'] or course_info[course1]['Simultaneous'] or course_info[course1]['NotSimultaneous']:
            continue

        break


    # pick course 2

    # pick a random block
    timeslot2 = random.randint(0,7)

    semester2 = ""

    if (timeslot2 <= 3):
        semester2 = "sem1"
    else:
        semester2 = "sem2"
        timeslot2 -= 4

    while True:

        # pick a random course in that block. Does not select courses with requirements for blocking and sequencing
        course2, students2 = random.choice(list(timetable[semester2][timeslot2].items()))

        # check for blocking/sequencing requirements, and that course2 does not already run in timeslot1, and that course1 does not already run in timeslot2
        if course_info[course2]['Prereqs'] or course_info[course2]['Postreqs'] or course_info[course2]['Simultaneous'] or course_info[course2]['NotSimultaneous']:
            continue

        if course2 in timetable[semester1][timeslot1] or course1 in timetable[semester2][timeslot2]:
            continue

        break


    # swap the courses (and their students)

    timetable[semester1][timeslot1][course2] = students1
    timetable[semester2][timeslot2][course1] = students2

    timetable[semester1][timeslot1].pop(course1)
    timetable[semester2][timeslot2].pop(course2)

    return timetable



with open('course.json') as f:
        course_info = json.load(f)
with open('student_requests.json') as f:
        student_info = json.load(f)
print(course_info)