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
def generate_course_schedule():
    '''
    # remove all courses from course_info if:
        # there are less than 5 students requesting it
        # but courses like learning strategies are kept

    removed_courses = []

    for key in list(course_info.keys()):
        if len(course_info[key]['Students']) <= 5:
            num_of_students = course_info[key]['Students']
            for sim_course in course_info[key]['Simultaneous']:

                # put all students signed up to each simultaeous course into num_of_students
                for students in course_info[sim_course]['Students']:
                    num_of_students.append(students)

            if len(num_of_students) <= 7:
                removed_courses.append(key)
                print(course_info[key]['course name'], num_of_students)
                num_of_students = []
    
    for rem_key in removed_courses:
        
        if rem_key in course_info[rem_key]['Simultaneous']:
            course_info[rem_key]['Simultaneous'].pop(rem_key)

        if rem_key in course_info[rem_key]['Not Simultaneous']:
            course_info[rem_key]['Not Simultaneous'].pop(rem_key)

        course_info.pop(rem_key)
    '''
    '''
    prec11 (1/2)
    prec12 (1+2)
    calc12 (2)
    apcalc (2)

    APCS   (2)
    CS12   (1/2)

    APPHY  (1)
    Phy12  (1/2)
    Phy11   (1/2)

    chem11 (1/2)
    chem12 (1/2)

    
    '''


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
    with open('courses.json') as f:
        course_info = json.load(f)

    with open('student_requests.json') as f:
        student_info = json.load(f)

    # create timetable with all courses
    timetable = {
        "sem1" : {},
        'sem2' : {},
        'outside_timetable' : {}
    }
  
  # sem 1
    for c in schedule['sem1'][0]:
        timetable['sem1'].setdefault(c, [])
   
    for c in schedule['sem1'][1]:
        timetable['sem1'].setdefault(c, [])

    for c in schedule['sem1'][2]:
        timetable['sem1'].setdefault(c, [])
    
    for c in schedule['sem1'][3]:
        timetable['sem1'].setdefault(c, [])
    
    # sem 2
    for c in schedule['sem2'][0]:
        timetable['sem2'].setdefault(c, [])
   
    for c in schedule['sem2'][1]:
        timetable['sem2'].setdefault(c, [])

    for c in schedule['sem2'][2]:
        timetable['sem2'].setdefault(c, [])
    
    for c in schedule['sem2'][3]:
        timetable['sem2'].setdefault(c, [])
    
    # outside time table
    
    for c in schedule['outside_timetable']:
        timetable['outside_timetable'].setdefault(c, [])
    # inside timetable courses
        # go through student info one student at a time
    for student in student_info:

        # create a dictionary of the courses choosen by the student, key as courses name and value as the priority of that course
        not_sorted_courses = student_info[student]
        course_priority = {}
        num_alt = 0 # track how many alt courses needed
        for course in not_sorted_courses:
            priority = course_info[course].get("Priority")
            course_priority.setdefault(course, priority)

        # Sort their courses by priority
        sorted_courses = sorted(course_priority.items(), key=lambda item: item[1])
        
        # Start with most prioritized courses
        for i in range(len(sorted_courses)):
            has_not_sim = False
           
            course, _  = sorted_courses[i]
            max_enroll = course_info[course]['Max Enrollment']
        

            # Check if student meets blocking and seq

            num_pre_req = 0
            for c in sorted_courses:
                if c in course_info[course]['Pre Req']:
                    num_pre_req = num_pre_req + 1
                    pre_req = c
                if c in course_info[course]['Not Simultaneous']:
                    has_not_sim = True
                    not_sim = c
                    max_enroll_not_sim = course_info[c]['Max Enrollment']
                
            if num_pre_req > 1:

                # doesn't work, keep track to add an alt
                sorted_courses.remove(course)
                num_alt = num_alt + 1
                continue
           
           
            # find course in schedule that does not contridict with student's current schedule and check if course is at max enrollment
            # deal with non generic scenarios first (not sim and pre req)

            # pre req
            if num_pre_req == 1:
                max_enroll_pre_req = course_info[pre_req]['Max Enrollment']
                if len(timetable['sem1'][0][pre_req]) < max_enroll_pre_req:
                    timetable['sem1'][0][pre_req].append(student)
                    sorted_courses.remove(pre_req)

                elif len(timetable['sem1'][1][pre_req]) < max_enroll_pre_req:
                    timetable['sem1'][1][pre_req].append(student) 
                    sorted_courses.remove(pre_req)


                elif len(timetable['sem1'][2][pre_req]) < max_enroll_pre_req:
                    timetable['sem1'][2][pre_req].append(student) 
                    sorted_courses.remove(pre_req)


                elif len(timetable['sem1'][3][pre_req]) < max_enroll_pre_req:
                    timetable['sem1'][3][pre_req].append(student) 
                    sorted_courses.remove(pre_req)

                else:
                    # cannot fit student into any blocks for pre req in sem1, cannot take prereq and post req course

                    # add what if pre req is offered in second sem
                    sorted_courses.remove(pre_req)
                    sorted_courses.remove(course)
                    num_alt = num_alt + 2
                    continue # move to next course
                
            
            # deal with not sim courses
            if has_not_sim:
                   # not sim courses (band and pe) are linear with band in sem 1 and pe in sem 2, going to put student in both courses
                    if course in schedule['sem1'][0]:
                        if len(timetable ['sem1'][0][course]) < max_enroll:
                            timetable['sem1'][0][course].append(student)
                            if len(timetable['sem2'][0][not_sim]) < max_enroll_not_sim:
                                timetable['sem2'][0][not_sim].append(student)
                                continue
                        else:
                            sorted_courses.remove[course]
                            sorted_courses.remove[not_sim]
                            num_alt = num_alt + 2
                    elif course in schedule['sem1'][0]:
                        if len(timetable ['sem1'][0][course]) < max_enroll:
                            timetable['sem1'][0][course].append(student)
                            if len(timetable['sem2'][0][not_sim]) < max_enroll_not_sim:
                                timetable['sem2'][0][not_sim].append(student)
                                continue
                        else:
                            sorted_courses.remove[course]
                            sorted_courses.remove[not_sim]
                            num_alt = num_alt + 2
                        

                # add students regularly, no sim, no prereq
                    # if there is no space in any of the schedule for this course
                        # Skip this course and go onto the next prioritized one (assuming that there will always be enough space for required courses)
                # If doesn't meet sequencing / pre req
                    # Skip this course and go onto the next prioritized one (assuming student will always have required courses with right sequence and pre req ex. no english 9, 10, 11)

                # give alts to those that have courses that did not work out

                # if al alts are used, give random courses

                
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

    # swap n pairs of students
    for i in range(n):

        # find some way to select students such that switching them is good
        # currently chooses randomly
        # does not yet check for spares

        timeslot = random.randint(0,7)
        semester = ""
        if (0 <= timeslot <= 3):
            semester = "sem1"
        else:
            semester = "sem2"
            timeslot -= 4

        while True:

            course1 = random.choice(timetable[semester][timeslot])
            course2 = random.choice(timetable[semester][timeslot])

            if (course1 == course2):
                continue

            student1 = random.choice(timetable[semester][timeslot][course1])
            student2 = random.choice(timetable[semester][timeslot][course2])

            if (student1 == student2):
                continue

            break

        student_schedules = get_student_schedules(timetable)

        if (semester == "sem2"):
            timeslot += 4

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

# course_schedule only stores the courses, it doesn't give a shit about students
course_schedule = {}
course_schedule['sem 1'] = {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
    }
course_schedule['sem 2'] = {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
    }

with open('courses_trimmed.json') as f:
        course_info = json.load(f)
with open('student_requests.json') as f:
        student_info = json.load(f)
#print(course_schedule)
generate_course_schedule()

#print(course_info['ASTA-12---']['Students'])




# actual code


'''
# generate initial guess
schedule = generate_course_schedule()
initial_timetable = generate_timetable(schedule)
final_timetable = initial_timetable
current_timetable = initial_timetable

# check 10 possible schedules
for i in range(10):

    # make 100 small changes to students, each of which is an improvement
    for i in range(100):

        current_score = score(current_timetable)
        best_timetable = current_timetable
        max_score = current_score

        counter = 0

        # generate 50 better timetables and choose the best one
        while counter < 50:

            new_timetable = shuffle_students(current_timetable)
            new_score = score(new_timetable)

            if new_score > current_score:

                counter += 1

                if max_score < new_score:
                    max_score = new_score
                    best_timetable = new_timetable

        current_timetable = best_timetable

    if score(current_timetable) > score(final_timetable):
        final_timetable = current_timetable

    # make small change to course schedule, then repeat
    current_timetable = shuffle_courses(current_timetable)
'''
'''
print(initial_timetable)
print(score(initial_timetable))
print(final_timetable)
print(score(final_timetable))
'''
