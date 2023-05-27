import json
import random

# make course_info json info global
with open('courses.json') as f:
        course_info = json.load(f)

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

    Fill 42 courses max in each block
    '''
    all_courseblock_codes = {}
    i = 0

    # contains key as course codes, value is the corresponding number of sections left for that course / combination of courses:
        # if this block of course is simultaneous with another, they all appear with * seperating them
    # if 
    for course in course_info:
        pass

    while True:
        current_used_blocks = []                                            # to store all the blocks this course takes up
        for j in range(all_courseblock_codes[i]):                           # goes through all sections of this course
            rand_block = return_rando_block().split(' ')                    # [semester#, block#]
            course_schedule['sem ' + rand_block[0]][rand_block[1]] = i      # put this course into the randomized 
            current_used_blocks.append(rand_block[0] + ' ' + rand_block[1])
        


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

# takes in a list of unvailable blocks, and spits out a random block among the available blocks
def return_rando_block(not_these_blocks):

    current_available_blocks = available_blocks.copy()

    for blocks in not_these_blocks:
        current_available_blocks.pop(blocks)
    
    if len(current_available_blocks) == 0:
        return -1

    rand = random.randInt(0, len(current_available_blocks)-1)

    return current_available_blocks[rand]

def generate_timetable(schedule):
    with open('courses.json') as f:
        course_info = json.load(f)

    with open('student_requests.json') as f:
        student_request = json.load(f)

    # randomize student order in student info json so that each run will generate different schedules
    keys = list(student_request.keys())
    random.shuffle(keys)

    # Create a new dictionary with shuffled keys
    student_info = {key: student_request[key] for key in keys}

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
        num_courses = 0
        courses_taking = []
        # create a dictionary of the courses choosen by the student, key as courses name and value as the priority of that course
        not_sorted_courses = student_info[student]
        course_priority = {}
        num_alt = 0 # track how many alt courses needed
        for course in not_sorted_courses:
            
            priority = course_info[course].get("Priority") # not sure how to determine if course is alternate, once determined add 5 to nonalt courses to prioritze it
            
            course_priority.setdefault(course, priority)

        # Sort their courses by priority
        sorted_courses = sorted(course_priority.items(), key=lambda item: item[1])
        
        # Start with most prioritized courses
        length = len(sorted_courses)
        for i in range(length):
            has_not_sim = False
           
            course, _  = sorted_courses[i]

            if num_courses > 8:
                break

            # check if it is outside time table, if it is automatically add it and don't change the number of courses
            if (course_info[course]['Outside Timetable'] == True):
                if add_student('outside_timetable', course, timetable, schedule, student) != -1:
                    timetable = add_student('outside_timetable', timetable, schedule, student)
                    i = i - 1
                    courses_taking.append(course)
                    sorted_courses.remove(course)
            else: 
                sorted_courses.remove(course)
                i = i - 1
                num_alt = num_alt + 1

            # Check if student meets blocking and seq
            num_pre_req = 0
            for c in sorted_courses:
                if c in course_info[course]['Pre Req']:
                    num_pre_req = num_pre_req + 1
                    pre_req = c
                if c in course_info[course]['Not Simultaneous']:
                    has_not_sim = True
                    not_sim = c
                   
            if num_pre_req > 1:

                # doesn't work, keep track to add an alt
                sorted_courses.remove(course)
                i = i - 1
                num_alt = num_alt + 1
                continue
           
           
            # find course in schedule that does not contridict with student's current schedule and check if course is at max enrollment
            # deal with non generic scenarios first (not sim and pre req)

            # pre req
            if num_pre_req == 1:
                if add_student('sem1', pre_req, timetable, schedule, student) != -1:
                    if add_student('sem2', course, timetable, schedule, student) != -1:
                        timetable = add_student('sem1', pre_req, timetable, schedule, student)
                        timetable = add_student('sem2', course, timetable, schedule, student)
                        sorted_courses.remove(pre_req)
                        sorted_courses.remove(course)
                        courses_taking.append(course)
                        courses_taking.append(pre_req)
                        i = i - 2
                        num_courses = num_courses + 2
                        continue
                    timetable = add_student('sem1', pre_req, timetable, schedule, student)
                    sorted_courses.remove(pre_req)
                    courses_taking.append(pre_req)
                    i = i - 1
                    num_courses = num_courses + 1
                    continue

                
                elif add_student ('sem2', pre_req, timetable, schedule, student) != -1:
                    timetable = add_student ('sem2', pre_req, timetable, schedule, student)
                    sorted_courses.remove(pre_req)
                    courses_taking.append(pre_req)
                    i = i - 1
                    num_courses = num_courses + 1
                    continue

                else:
                    # add what if pre req is offered in second sem
                    sorted_courses.remove(pre_req)
                    sorted_courses.remove(course)
                    i = i - 2
                    num_alt = num_alt + 2
                    continue # move to next course

            

            # deal with not sim courses
            if has_not_sim:
                # not sim courses (band and pe) are linear with band in sem 1 and pe in sem 2, going to put student in both courses
                if add_student('sem1', course, timetable, schedule, student) != -1:
                    if add_student('sem2', not_sim, timetable, schedule, student) != -1:
                        timetable = add_student('sem1', course, timetable, schedule, student)
                        timetable = add_student('sem2', not_sim, timetable, schedule, student)
                        sorted_courses.remove(not_sim)
                        sorted_courses.remove(course)  
                        courses_taking.append(course)
                        courses_taking.append(not_sim)
                        i = i - 2
                        num_courses = num_courses + 2
                        continue
                elif add_student('sem2', course, timetable, schedule, student) != -1:
                    if add_student('sem1', not_sim, timetable, schedule, student) != -1:
                        timetable = add_student('sem2', course, timetable, schedule, student)
                        timetable = add_student('sem1', not_sim, timetable, schedule, student)
                        sorted_courses.remove(not_sim)
                        sorted_courses.remove(course)
                        courses_taking.append(course)
                        courses_taking.append(not_sim)
                        i = i - 2
                        num_courses = num_courses + 2
                        continue
                   
                else: # no spots in one of the sim courses
                    sorted_courses.remove[course]
                    sorted_courses.remove[not_sim]
                    i = i - 2
                    num_alt = num_alt + 2
                    continue

            # see if linear course, if linear add to both sem1 and sem 2 and this course takes 2 spots
            if course_info[course]['Base Terms/Year'] == 1 and course_info[course]['Covered Terms/Year'] == 1:
                if add_student('sem1', course, timetable, schedule, student) != -1 and add_student('sem2', course, timetable, schedule, student) != -1:
                    timetable = add_student('sem1', course, timetable, schedule, student)
                    timetable = add_student('sem2', course, timetable, schedule, student)
                    i = i - 2
                    courses_taking.append(course)
                    sorted_courses.remove(course)
                    num_courses = num_courses + 2
                    continue
                else: 
                    i = i - 1
                    sorted_courses.remove(course)
                    continue
            

            # add students regularly, no sim, no prereq 
            if add_student('sem1', course, timetable, schedule, student) != -1:
                timetable = add_student('sem1', course, timetable, schedule, student) 
                sorted_courses.remove(course)
                i = i - 1
                courses_taking.append(course)
                num_courses = num_courses + 1
                continue

            # if sem1 doesn't have space check sem 2
            elif add_student('sem2', course, timetable, schedule, student) != -1:
                timetable = add_student('sem2', course, timetable, schedule, student) 
                sorted_courses.remove(course)
                i = i - 1
                num_courses = num_courses + 1
                courses_taking.append(course)
                continue
            else: # cannot add course
                sorted_courses.remove(course)
                i = i - 1
                num_alt = num_alt + 1
                continue
                    
               
                # give alts to those that have courses that did not work out

                # if al alts are used, give random courses
        # assign random course if the courses student assigned is not avaliable
        # assigns the next course and relatively not priorizted course (p > 20)
        while num_courses < 8:
            num_rand_course = 8 - num_courses
            for course in course_info:
                if course not in courses_taking:
                    if course_info[course]['Priority'] > 20:
                        if course_info[course]['Outside Timetable']:
                            if len(course_info[course]['Pre Req']) == 0:
                                if len(course_info[course]['Not Simultaneous']) == 0:
                                    if add_student('sem1', course, timetable, schedule, student) != -1:
                                        timetable = add_student('sem1', course, timetable, schedule, student)
                                        num_courses = num_courses + 1
                                        courses_taking.append(course)
                                    elif add_student('sem2', course, timetable, schedule, student) != -1:
                                        timetable = add_student('sem2', course, timetable, schedule, student)
                                        num_courses = num_courses + 1
                                        courses_taking.append(course)




# finds the avaliable course in a semester and attempts to add student to the course
# if no avaliable course, return -1
def add_student (sem, course, timetable, schedule, student):
    isAdded = False
    max_enroll = course_info[course]['Max Enrollment']
    if course in schedule[sem][0]:
        if len(timetable [sem][0][course]) < max_enroll:
            timetable[sem][0][course].append(student)
            isAdded = True    
    elif course in schedule[sem][1]:
        if len(timetable [sem][1][course]) < max_enroll:
            timetable[sem][1][course].append(student)
            isAdded = True 
    elif course in schedule[sem][2]:
        if len(timetable [sem][2][course]) < max_enroll:
            timetable[sem][2][course].append(student)
            isAdded = True
    elif course in schedule[sem][3]:
        if len(timetable [sem][3][course]) < max_enroll:
            timetable[sem][3][course].append(student)
            isAdded = True
    
    if isAdded:
        return timetable
    else: 
        return -1

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

            # get two different random courses in that timeslot
            course1 = random.choice(timetable[semester][timeslot])
            course2 = random.choice(timetable[semester][timeslot])

            if (course1 == course2):
                continue

            # get one student from each course
            student1 = random.choice(timetable[semester][timeslot][course1])
            student2 = random.choice(timetable[semester][timeslot][course2])

            if (student1 == student2):
                continue

            break


        # swap the two students in the timeslot

        timetable[semester][timeslot][course1].append(student2)
        timetable[semester][timeslot][course1].remove(student1)
        timetable[semester][timeslot][course2].append(student1)
        timetable[semester][timeslot][course2].remove(student2)
    
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

        # check that course1 does not run in every block
        if course1 in ['MCH--11---', 'MCLE-10---', 'MENST12---', 'MLTST10---', 'MLST-12---', 'MPREC11---', 'MSC--10---', 'MSS--10---', 'XLDCB09LS-', 'YED--0AX--', 'YED--1DX--', 'YED--2CX--', 'YED--2EX--']:
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


# prints the timetable in tabular form
def print_timetable(timetable):

    with open('courses.json') as f:
        course_info = json.load(f)

    s1A = [course_info[course_code]['course name'] for course_code in timetable["sem1"][0].keys()]
    s1B = [course_info[course_code]['course name'] for course_code in timetable["sem1"][1].keys()]
    s1C = [course_info[course_code]['course name'] for course_code in timetable["sem1"][2].keys()]
    s1D = [course_info[course_code]['course name'] for course_code in timetable["sem1"][3].keys()]
    s2A = [course_info[course_code]['course name'] for course_code in timetable["sem2"][0].keys()]
    s2B = [course_info[course_code]['course name'] for course_code in timetable["sem2"][1].keys()]
    s2C = [course_info[course_code]['course name'] for course_code in timetable["sem2"][2].keys()]
    s2D = [course_info[course_code]['course name'] for course_code in timetable["sem2"][3].keys()]

    print("s1A: " + (course + ", " for course in s1A))
    print("s1B: " + (course + ", " for course in s1B))
    print("s1C: " + (course + ", " for course in s1C))
    print("s1D: " + (course + ", " for course in s1D))
    print("s2A: " + (course + ", " for course in s2A))
    print("s2B: " + (course + ", " for course in s2B))
    print("s2C: " + (course + ", " for course in s2C))
    print("s2D: " + (course + ", " for course in s2D))



def get_student_timetable(student_id, timetable):

    print(get_student_schedules(timetable)[student_id])

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

# initialize the blocks that have less than 42 blocks in them
available_blocks = ['1 A', '1 B', '1 C', '1 D', '2 A', '2 B', '2 C', '2 D']


#print(course_schedule)
with open('student_requests.json') as f:
        student_request = json.load(f)


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
