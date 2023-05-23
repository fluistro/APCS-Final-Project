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

def generate_timetable():
    
  
    with open('courses.json') as f:
        course_info = json.load(f)

    with open('student_requests.json') as f:
        student_info = json.load(f)

   
    
    
    # inside timetable courses
        # go through student info one student at a time
    for student in student_info:

        # create a dictionary of the courses choosen by the student, key as courses name and value as the priority of that course
        not_sorted_courses = student_info[student]
        course_priority = {}
        for course in not_sorted_courses:
            priority = course_info[course].get("Priority")
            course_priority.setdefault(course, priority)

        # Sort their courses by priority
        sorted_courses = sorted(course_priority.items(), key=lambda item: item[1])
        
        # Start with most prioritized courses
        for i in range(len(sorted_courses)):
            course, _  = sorted_courses[i]
            print(course)

            # Check if student meets sequencing
            if "Pre Req" in course_info[course]:

            # and pre req if have two courses that have order
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
                return 0

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

    for i in range(n):

        # find some way to select students such that switching them is good

        timeslot = 0
        student1 = 1000
        student2 = 1001


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
    pass

with open('courses.json') as f:
        course_info = json.load(f)
with open('student_requests.json') as f:
        student_info = json.load(f)

generate_timetable()