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
modifies the course_schedule dictionary:
it ignores all courses with <=5 students requesting it
let X = the available number of section of a course, then this course code appears in the dictionary X times
its supposed to make sure that no 2 of the same courses appear in the same block in the same semester
all simultaneous courses are one element of the list, each course code in that simultaneous bunch is seperated with a '*'
rn as of May 26, it does not give a shit baout whether students would fill the course or not. its only going off of the available sections of each course
for band and PE: band 9 and band 10 are both in sem 1, and their corresponding PE class is in sem 2 of the same block
for Outside timetable courses they are all in 'OT' key of sem 1
'''
def generate_course_schedule():
    
    schedule = [
            # A 
            ["MMA--09---","MEN--09E--","MCMPS10---","MMAP-11---", "XBA--09B-L*MPHE-09--L*XBA--09C-L*MPHE-09B-L*MPHE-09G-L","MMA--09H--","MLTST12---","MEN--09---","MWBDV10IT-*MADIT09---","MFMP-10---","MCH--11---","MSS--09---","MPREC12H--","MEN--09---","MENST12---","MPH--12---","MCTWR10---","MPREC11---","MEPSS11---","MPHE-09---*MPHED10---","MNMD-11---","MPH--11---","MCMCL12---","MCMPS10C--","MCLE-10---","MADGE09D--*MTEXP10D--*YMIS-1DD--*YMIS-2DD--","MEPSS11C--","MDNC-09F--*MDCF-10---*MDCF-11---*MDCF-12---","MAE--09---*MVAST10---", "MLFSC11---","MFOOD11---*MFOOD12---","MSS--10---","MADW-09---*MWWK-10---*MWWK-11---*MWWK-12---","MEVSC12C--","MPREC12---","MACLV11G--*MACLV12G--","MSC--10---","MMACS11---*MMACS12---","MATPH12---","MMEDD10---*MMEDD11---*MMEDD12---", "MADGE09I--"],

            # B
            ["MMUCB10--L*MPHED10B-L*MPHED10G-L","MCALC12---", "MSPLG10--L","MIMCB11--L*MIMCB12--L","MPREC11---","MEPSS11---","MSP--09---*MSP--10---","MPREC12---","MSC--09---","MCTWR10---","MSTAT12---","MFMP-10---","MLST-12---","MPH--11---","MSS--10---","MCMPS11---","MFMP-10C--","MCMCL12---","MATPH12---","MAC--11---","YESFL1CX--","YESFL0AX--","MADD-09---*MTDRF12---*MTDRF10---","MTDRF11---","MACLV11---*MACLV12---","YPA--1CX--*YPA--0CX--*MPHE-09Y--*YPA--2CX--","MCLE-10---","MFOOD11---*MFOOD12---","MFR--09---","MTAUT11---*MTAUT12---*MTEAD12---","MMA--09---","MMA--09C--","MFMP-10H--","MPHE-09G--*MPHED10G--","MSC--09---","MCLE-10---","MMACS12---","MCH--12---","MCTWR11---", "MMACS11---*MMACS12---"],

            # C 
            ["MCMPR12W--*MCMPR11W--", "MMUGT10---*MIMG-12---*MIMG-11---","MPREC12---","MPHE-09B--*MPHED10B--","MLTST11---","MWBDV10IT-*MADIT09---","MSC--10---","MEVSC11---","MWH--12---","MBIT-11","MIT--11---","MPREC11H--","MENST12---","MPH--12---","MMA--09---","MEPSS11---","MPH--11---","MNMD-11---","MFMP-10C--","MATPH12---","AELC-12---","MCLE-10---","MNMD-10---","MADD-09---*MTDRF10---","MTDRF11---*MTDRF12---","MSS--09---","MSS--09C--","MVAPH10---*MVAPH11---*MVAPH12---","MCH--11---","MADFS09---*MFOOD10---","MFR--11---","MFR--12---","XLDCE09NM-","MMA--09C--","YPSYC1AX--","MPHE-09---*MPHED10---", "MWPM-10---", "MMACS11---","MCH--12---","MTEAR10---*MTROB11---*MTROB12---*MADER09---", "MLTST11C--"],

            # D 
            ["MCTWR11---", "MSPLG10--L","MPREC12---","MLST-12---","MEN--09---","MFMP-10---","MSC--09---","MSP--11---","MCMPS11---","APHM-12---","MENFP12---","MFOM-11---","MLST-12---","MCH--11---","YLAW-2CX--","MPREC11---","MSC--10---","MATPH12---","MCMPS10C--","MADEM10---","MEN--09---","MPHE-09B--*MPHED10B--","MSS--09C--","MVAST10---*MAE--09---","MVAST11---*MVAST12---","MLFSC11---","MADFS09---*MFOOD10---","MSS--10---","MFR--10---","XLDCB09M--*MTPOW10---","MEVSC12C--","MWPM-11---","YPSYC1AX--","MPHE-09G--*MPHED10G--","MCLE-10---", "MCH--11---","MTEAR10---*MTROB11---*MTROB12---*MADER09---","MDRM-11---*MDRM-12---", "MWPM-11---", "MWWK-12---","YPSYC1AX--"],

            # A
            ["MENT-12---", "XBA--09B-L*MPHE-09--L*XBA--09C-L*MPHE-09B-L*MPHE-09G-L","MINST12C--","MECOM12---","MDNC-09H--*MDNCN11---*MDNCN12---*MIDS-0B---","MCALC12---","MCMPS11---","MWBDV10IT-*MADIT09---","MMA--09---","MCH--11---","MEPSS11---","MSP--09---","MENFP12---","MFMP-10---","MLST-12---","YLAW-2CX--","MWH--12---","MSC--10---","AELC-12---", "MENT-12---", "MFOM-11---","MADD-09---*MTDRF12---*MTDRF10---","MTDRF11---","MEPSS11C--", "MLFSC11---","MADFS09---*MFOOD10---","MCMCL12---", "MNMD-10---","XLDCB09M--*MTPOW10---","MPREC11---","MATPH12---","YPSYC1AX--","MPHE-09G--*MPHED10G--", "MSC--10---","MMACS11---*MMACS12---","MCH--12---","MTEAR10---*MTROB11---*MTROB12---*MADER09---","MEN--09C--",'MSC--10C--', "MPH--12---"],

            # B
            ["YESFL0AX-L","MCSTU10---*MDCOM11C--*MDMD-12D--","MMUCB10--L*MPHED10B-L*MPHED10G-L","MCMPS10---", "MINST12---","MIMCB11--L*MIMCB12--L","MCMPR12W--","ACAL-12---","MLST-12---","MWBDV10IT-*MADIT09---","MSC--09---","MSS--09---","MADEM10---","MSP--10---","MENST12---","MPH--12---","MCTWR10---","MPH--11---","MSS--10---", "MCLE-10---","MSC--09C--","MWH--12---","MSC--10C--","MAC--11---*MACC-12---","MADD-09---*MTDRF10---","MTDRF11---*MTDRF12---","MPHE-09B--*MPHED10B--","MDNC-09PT-*MDNTP10---*MDNTP11---*MDNTP12---","MLFSC11---","MFOOD11---*MFOOD12---","MFR--11---", "MTAUT11---*MTAUT12---*MTEAD12---","MPREC11---","MCH--12---","MFTCD11---*MFTCD12---","MSC--10---","MSTX-0A---*MSTX-1A---*MSTX-2A---","MCH--11---","MMEDD10---*MMEDD11---*MMEDD12---", "MDR--09---*MDRM-10---", "MMACS12---"],

            # C
            ["XLEAD09---","MIT--12---","MEFWR10---","MIMG-11---*MIMG-12---*MMUGT10---","XBA--09G--", "MPHE-09---*MPHED10---", "MLTST11C--", "MSC--10---", "MSS--10---", "MCH--11---", "MSS--09---", "MCLE-10---", "MPREC12---", "MCMPS11---", "MCALC12---", "MENFP12---", "MLST-12---", "MPH--11---", "YLAW-2CX--", "MNMD-10---", "MSC--09C--", "MENST12C--", "MAC--11---", "MODED11---*MODED12---*YPR--0BX--", "MACLV11---*MACLV12---", "MSS--10C--", "MVAST10---*MAE--09---","MVAST11---*MVAST12---", "MLFSC11---", "MFOOD11---*MFOOD12---", "MFR--09---", "MPREC11---", "MFMP-10---", "MSC--09---", "MWPM-11---", "MADW-09---*MWWK-10---*MWWK-11---*MWWK-12---", "MPGEO12---", "MCH--12---","MEN--09---","MENST12--Y"
            ],

            # D
            ["YESFL0AX-L","MSPLG11---","MSTX-0AI--*MSTX-1AI--*MSTX-2AI--","MINST12C--","MENFP12--Y","MPHE-09B--*MPHED10B--","MEN--09---","MMACS11---","MSC--10---","MSS--10---","MEVSC11---","MCLE-10---","MSS--10---","MSP--11---*MSP--12---","MCH--12---","MENFP12---","MPH--12---","MCTWR10---","MPREC11---","MEPSS11---","MVAPH10---*MVAPH11---*MVAPH12---","MCTWR11---", "MPH--11---", "MATPH12---", "MCMPS11---", "MENT-12---", "MSS--09---", "MSS--10C--", "MAE--09---*MVAST10---", "MCH--11---", "MFR--11---","MFR--12---", "MTAUT11---*MTAUT12---*MTEAD12---", "MPREC12---", "MPHE-09G--*MPHED10G--", "MADW-09---*MWWK-10---*MWWK-11---*MWWK-12---", "ACSC-2A---", "MTDRF10---*MTDRF12---*MADD-09---", "MTDRF11---", "MEN--09C--", "MENST12--Y"
            ],

            ["MCMCC11--L", "MCMCC12--L", "MDNC-09C-L", "MDNC-09M-L", "MDNC-10--L", "MDNC-11--L", "MDNC-12--L", "MDNCM10--L", "MDNCM11--L", "MDNCM12--L", "MGMT-12L--", "MGRPR11--L", "MGRPR12--L", "MIDS-0C---", "MIMJB11--L", "MIMJB12--L", "MMUCC10--L", "MMUJB10--L", "MMUOR10S-L", "MMUOR11S-L", "MMUOR12S-L", "MWEX-2A--L", "MWEX-2B--L", "XBA--09J-L", "XC---09--L", "XLDCB09S-L", "YCPA-0AX-L", "YCPA-0AXE-", "YCPA-1AX-L", "YCPA-1AXE-", "YCPA-2AX-L", "YCPA-2AXE-", "YED--0BX-L", "YED--1EX-L", "YED--2DX-L", "YED--2FX-L"]

    ]
    '''
    for block in [0,1,2,3]:
        for course in schedule[block]:

            courses = []

            if '*' in course:
                courses = course.split('*')
            else:
                courses.append(course)

            for i in courses:
                if course_info[i]["Base Terms/Year"] == 1:
                    print(i)
    '''
    '''                
    if len(course_info[courses[i]]['Pre Req']) != 0:

        if courses[i] not in schedule[4] and courses[i] not in schedule[5] and courses[i] not in schedule[6] and courses[i] not in schedule[7]:
            print(courses[i])
    '''
    '''                    
    for pre_req in course_info[courses[i]]['Pre Req']:
        if pre_req not in schedule[0] and pre_req not in schedule[1] and pre_req not in schedule[2] and pre_req not in schedule[3]:
            print("block: " + str(block) + " " + str(courses))
    '''

    print ('1 a', len(schedule[0]))
    print ('1 b', len(schedule[1]))
    print ('1 c', len(schedule[2]))
    print ('1 d', len(schedule[3]))
    print ('2 a', len(schedule[4]))
    print ('2 b', len(schedule[5]))
    print ('2 c', len(schedule[6]))
    print ('2 d', len(schedule[7]))
    
    '''
    for block in range(len(schedule)):
        for course in schedule[block]:
            pr = False
            courses = []
            if '*' in course:
                courses = course.split('*')
                for i in range(1, len(courses)):
                    if courses[i] not in course_info[courses[0]]['Simultaneous']:
                        print(courses[i] + " ")
                        pr = True
                if pr:
                    print()
                    pr = False

    ''' 

    with open('master_schedule.json', 'w') as fp:
        json.dump(schedule, fp)
        
    """    

    for course in course_info:
        counter = 0
        section = int(course_info[course]['Sections'])
        
        for c in schedule['sem1'][0]:
            if course in c:
                counter += 1
        for c in schedule['sem1'][1]:
            if course in c:
                counter += 1
        for c in schedule['sem1'][2]:
            if course in c:
                counter += 1
        for c in schedule['sem1'][3]:
            if course in c:
                counter += 1
        for c in schedule['sem2'][0]:
            if course in c:
                counter += 1
        for c in schedule['sem2'][1]:
            if course in c:
                counter += 1
        for c in schedule['sem2'][2]:
            if course in c:
                counter += 1
        for c in schedule['sem2'][3]:
            if course in c:
                counter += 1

        if counter != section:
            if len(course_info[course]['Students']) > 5 and not course_info[course]['Outside Timetable']:
              print( 'course:', course, course_info[course]['course name'], 'sections needed:', section, 'sections have:', counter)

    print ('1 a', len(schedule['sem1'][0]))
    print ('1 b', len(schedule['sem1'][1]))
    print ('1 c', len(schedule['sem1'][2]))
    print ('1 d', len(schedule['sem1'][3]))
    print ('2 a', len(schedule['sem2'][0]))
    print ('2 b', len(schedule['sem2'][1]))
    print ('2 c', len(schedule['sem2'][2]))
    print ('2 d', len(schedule['sem2'][3]))
    """
    '''
    all_courseblock_codes = {}      # doesn't store OT courses
    course_info_modify = course_info.copy()

    # contains key as course codes, value is the corresponding number of sections left for that course / combination of courses:
    # if this block of course is simultaneous with another, they all appear with * seperating them

    for course in course_info_modify:

        #print('Looking at: ' + course_info_modify[course]['course name'])

        # skip if we have already looked at this course
        if course_info_modify[course]['Sections'] == 0:
            continue

        # Outside timetable (OT) courses
        if course_info_modify[course]['Outside Timetable'] == True:
            course_schedule['outside_timetable'].append(course)
            continue

        list_of_sim_courses = course_info_modify[course]['Simultaneous']

        # if no course is sim with this course
        if len(list_of_sim_courses) == 0:
            all_courseblock_codes[course] = course_info_modify[course]['Sections']
        
        # if there are > 0 course sim with this one
        else:

            # count the maximum amount of simultaneous blocks that can appear
            max_simblock_sections = course_info_modify[course]['Sections']

            for sim_course in list_of_sim_courses:
                if int(course_info_modify[sim_course]['Sections']) < int(max_simblock_sections):
                    max_simblock_sections = course_info_modify[sim_course]['Sections']

            # generate a string, which is the course code of these simultaneous courses, sperated with a *
            cur_sim_courses_codes = course
            for sim_course in list_of_sim_courses:
                cur_sim_courses_codes = cur_sim_courses_codes + "*" + sim_course

            # put the simultaneous blocks into all blocks
            all_courseblock_codes[cur_sim_courses_codes] = max_simblock_sections

            # minus the used up sections of these courses
            cur_sections = course_info_modify[course]['Sections']
            new_sections = int(cur_sections) - int(max_simblock_sections)
            course_info_modify[course]['Sections'] = new_sections               # the course itself
            for sim_course in list_of_sim_courses:                              # the sim courses w/ tis course
                cur_sections = course_info_modify[sim_course]['Sections']
                new_sections = int(cur_sections) - int(max_simblock_sections)
                course_info_modify[sim_course]['Sections'] = new_sections

            # now deal with the possible extra available sections of the sim courses

            # current course
            if course_info_modify[course]['Sections'] == 0:
                continue
            else:
                all_courseblock_codes[course] = course_info_modify[course]['Sections']

            # all the sim courses
            for sim_course in list_of_sim_courses:
                if course_info_modify[sim_course]['Sections'] == 0:
                    continue
                else:
                    all_courseblock_codes[sim_course] = course_info_modify[sim_course]['Sections']
                    course_info_modify[sim_course]['Sections'] = 0

    for course_block in all_courseblock_codes:
        current_used_blocks = []                                            # to store all the blocks this course takes up

        # deal with blocks with sections > 8
        if int(all_courseblock_codes[course_block]) > 8:
            extra_sections = int(all_courseblock_codes[course_block]) - 8
            current_used_blocks = []
            for i in range(extra_sections):

                # put the extra sections into course_schedule first
                rand_block = return_rando_block(current_used_blocks).split(' ')                    # [semester#, block#]
                course_schedule['sem' + rand_block[0]][letter_to_num(rand_block[1])].append(course_block)      # put this course into the randomized 
                current_used_blocks.append(rand_block[0] + ' ' + rand_block[1])
                all_courseblock_codes[course_block] = 8
            current_used_blocks = []

        if not '*' in course_block:
            if course_info_modify[course_block]['Outside Timetable'] == True:
                continue

        # take care of stupid(not) BANDDDDD and PEEEEEEE

        if 'MPHED10G-L' in course_block or 'MPHED10B-L' in course_block or 'MPHE-09B-L' in  course_block or 'MPHE-09G-L' in course_block:
            continue
        if 'XBA--09B-L' in course_block:
            rand_block = return_rando_block(['2 A', '2 B', '2 C', '2 D' ]).split(' ') 
            course_schedule['sem1'][letter_to_num(rand_block[1])].append(course_block)    # put band 9 into a sem 1 block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09B-L')    # put boys pe in sem 2 same block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHE-09G-L')    # girls ''
        if 'MMUCB10--L' in course_block :
            rand_block = return_rando_block(['2 A', '2 B', '2 C', '2 D' ]).split(' ') 
            course_schedule['sem1'][letter_to_num(rand_block[1])].append(course_block)    # put band 10 into a sem 1 block
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHED10B-L')
            course_schedule['sem2'][letter_to_num(rand_block[1])].append('MPHED10G-L')
            continue

        # the NORMAL courses
        for j in range(int(all_courseblock_codes[course_block])):                # goes through all available sections of this course
            rand_block = return_rando_block(current_used_blocks).split(' ')                                # [semester#, block#]
            course_schedule['sem' + rand_block[0]][letter_to_num(rand_block[1])].append(course_block)      # put this course into the randomized 
            current_used_blocks.append(rand_block[0] + ' ' + rand_block[1])
        

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

# takes in a list of unvailable blocks, and spits out a random block among the available blocks
def return_rando_block(not_these_blocks):

    current_available_blocks = available_blocks.copy()

    for blocks in not_these_blocks:
        current_available_blocks.remove(blocks)
    
    if len(current_available_blocks) == 0:
        return -1

    rand = random.randint(0, len(current_available_blocks)-1)

    return current_available_blocks[rand]


def letter_to_num(letter):
    if letter == 'A':
        return 0
    elif letter == 'B':
        return 1
    elif letter == 'C':
        return 2
    else:
        return 3
    
"""
takes roughly 20 seconds to generate schedule
generates a timetable with the schedule passed in
paramater must be formatted as a dictionary with key A,B,C,D therefore use course sequence 2
output schedule will have the same courses in each block as original passed in schedule but different order within blocks 
ie schedule passed in has order 1234 in block A, the returned scheudle might have 2431 in block A
all simultaneous courses are one element of the list, each course code in that simultaneous bunch is seperated with a '*'
not sim courses are counted as 2 courses one in sem 1 and one in sem 2
currently no way to determine order of two non simultaneous courses
doesn't care about if a class has only a small amount of students
code will run slower towards the end since students need to test more for which course they can take
"""
def generate_timetable(schedule):
     
    timetable = schedule_to_empty_timetable(schedule)

    student_ids = [str(i) for i in range(1000, 1838)]
    random.shuffle(student_ids)

    student_schedules = {}

    for student in student_ids:

        requests = student_requests[student]
        alternates = []
        if student in student_alternates:
            alternates = student_alternates[student]

        student_schedule = []
        for i in range(9):
            student_schedule.append([])

        for alternate in alternates:
            if alternate in requests:
                requests.remove(alternate)

        sorted_requests = sort_requests(requests, alternates)

        for request in sorted_requests:

            if len(student_schedule) == 8:
                break

            add(timetable, student, student_schedule, request)
        
        fill_random(timetable, student, student_schedule)

        student_schedules[student] = student_schedule

    return timetable

# fills any empty blocks with random courses
def fill_random(timetable, student, student_schedule):
    
    free_blocks = [] # indices of free blocks

    for i in range(0,8):
        if not student_schedule[i]:
            free_blocks.append(i)

    for index in free_blocks:
        block = get_block(index, timetable)
        while True:
            random_course = random.choice(list(block.keys()))
            single_course = random_course.split("*")[0]
            if len(block[random_course]) < int(course_info[single_course]["Max Enrollment"]) and not course_info[single_course]["Pre Req"] and not course_info[single_course]["Post Req"]:
                block[random_course].append(student)
                student_schedule[index].append(random_course)
                return


# attempts to give a requested course to a student
def add(timetable, student, student_schedule, request):
    
    # automatically give the course if it's outside the timetable
    if course_info[request]["Outside Timetable"] == "true":
        timetable["outside_timetable"][request].append(student)
        student_schedule[8].append(request)
        return
    
    free_blocks = [] # indices of free blocks
    s1 = False
    s2 = False

    # course must be in s2
    if course_info[request]["Pre Req"]:
        for prerequisite in course_info[request]["Pre Req"]:
            if prerequisite in student_requests[student]:
                s2 = True
                break

    # course must be in s1
    if course_info[request]["Post Req"]:
        for postrequisite in course_info[request]["Post Req"]:
            if postrequisite in student_requests[student]:
                s1 = True
                break

    if s1:
        for i in range(0,4):
            if not student_schedule[i]:
                free_blocks.append(i)
    elif s2:
        for i in range(4,8):
            if not student_schedule[i]:
                free_blocks.append(i)
    else:
        for i in range(0,8):
            if not student_schedule[i]:
                free_blocks.append(i)

    random.shuffle(free_blocks)

    # linear course
    if course_info[request]["Base Terms/Year"] == "1":
        for index in range(4):
            if index in free_blocks and (index + 4) in free_blocks:
                block_1 = get_block(index, timetable)
                block_2 = get_block(index + 4, timetable)
                if request in block_1 and request in block_2:
                    if len(block_1[request]) < int(course_info[request]["Max Enrollment"]) and len(block_2[request]) < int(course_info[request]["Max Enrollment"]):
                        block_1[request].append(student)
                        block_2[request].append(student)
                        student_schedule[index].append(request)
                        student_schedule[index + 4].append(request)
                        return
        return
                
    
    for index in free_blocks:
        block = get_block(index, timetable)
        if request in block:
            if len(block[request]) < int(course_info[request]["Max Enrollment"]):
                block[request].append(student)
                student_schedule[index].append(request)
                return
    
def get_block(index, timetable):
    if index <= 3:
        return timetable["sem1"][index]
    return timetable["sem2"][index - 4]

def sort_requests(requests, alternates):

    sorted_list = []

    temp = {request : int(course_info[request]["Covered Terms/Year"]) for request in requests}
    sorted_dict = dict(sorted(temp.items(), key=lambda x:x[1]))


    for request in sorted_dict:
        sorted_list.append(request)

    for alternate in alternates:
        sorted_list.append(alternate)

    return sorted_list


def schedule_to_empty_timetable(schedule):

    timetable = {
        "sem1":[{}, {}, {}, {}],
        "sem2":[{}, {}, {}, {}],
        "outside_timetable":{}
    }

    for course in schedule["sem1"]["A"]:
        timetable["sem1"][0][course] = []
    for course in schedule["sem1"]["B"]:
        timetable["sem1"][1][course] = []
    for course in schedule["sem1"]["C"]:
        timetable["sem1"][2][course] = []
    for course in schedule["sem1"]["D"]:
        timetable["sem1"][3][course] = []
    for course in schedule["sem2"]["A"]:
        timetable["sem2"][0][course] = []
    for course in schedule["sem2"]["B"]:
        timetable["sem2"][1][course] = []
    for course in schedule["sem2"]["C"]:
        timetable["sem2"][2][course] = []
    for course in schedule["sem2"]["D"]:
        timetable["sem2"][3][course] = []
    for course in schedule["sem1"]["OT"]:
        timetable["outside_timetable"][course] = []
    
    return timetable

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



# return the proportion of students who received all of their desired courses
def score(timetable, to_print):

    """if not is_timetable_valid(timetable):
        return 0"""

    student_schedules = get_student_schedules(timetable)

    total_requests = 0
    total_alternates = 0
    successful_requests = 0
    successful_alternates = 0
    
    successful_students = 0
    success1 = True
    
    successful_students_alternates = 0
    success2 = True
    
    total_students = 0

    for student in student_requests:

        requested = student_requests[student]
        assigned = []
        
        for block in student_schedules[student]:
            for course in block:
                assigned.append(course)
        
        if student in student_alternates:
            alternates = student_alternates[student]
        else:
            alternates = []

        for course in requested:

            if course in alternates:
                total_alternates += 1
                for assigned_course in assigned:
                    if course in assigned_course.split("*"):
                        successful_alternates += 1
                        break
            
            # if not an alternate
            else:
                total_requests += 1
                for assigned_course in assigned:
                    if course in assigned_course.split("*"):
                        successful_requests += 1
                        break
                    
        for assigned_course in assigned:
            if (assigned_course not in alternates) and (assigned_course in requested):
                continue
            success1 = False
            if (assigned_course in alternates):
                continue
            success2 = False
            
        if len(assigned) < 8:
            success1 = False
            success2 = False   
                    
        if success1:
            successful_students += 1
        if success2:
            successful_students_alternates += 1
            
        success1 = True
        success2 = True
        total_students += 1
            
    #print("total requests: " + str(total_requests))
    
    if to_print:
        print("# requested courses placed / # requested courses: " + str(successful_requests / total_requests))
        print("# requested or alternate courses placed / # requested or alternate courses: " + str((successful_requests + successful_alternates) / (total_requests + total_alternates)))
        print("percent students with 8/8 courses (requested only): " + str(successful_students / total_students))
        print("percent students with 8/8 courses (requested or alternate): " + str(successful_students_alternates / total_students))
        print("weighted score: " + str((successful_requests + 0.5 * successful_alternates) / (total_requests + total_alternates)))
    return (successful_requests + 0.5 * successful_alternates) / (total_requests + total_alternates)

# make a small change to the timetable by moving around students. return a new valid timetable.
# does not shuffle students in outside timetable courses.
def shuffle_students(original_timetable):
    
    timetable = copy.deepcopy(original_timetable)

    n = 100

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

            #print("shuffle_students loop")

            # get two different random courses in that timeslot
            course1 = random.choice(list(timetable[semester][timeslot].keys()))
            course2 = random.choice(list(timetable[semester][timeslot].keys()))

            if (course1 == course2) or len(timetable[semester][timeslot][course1]) == 0 or len(timetable[semester][timeslot][course2]) == 0:
                continue

            # get one student from each course
            
            student1 = timetable[semester][timeslot][course1][0]
            student2 = timetable[semester][timeslot][course2][0]
            
            for student in timetable[semester][timeslot][course1]:
                if course1 not in student_requests[student]:
                    student1 = student
                    
            for student in timetable[semester][timeslot][course2]:
                if course2 not in student_requests[student]:
                    student2 = student

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

# return true if valid
def is_timetable_valid(timetable):
    schedule = get_schedule()
    return is_timetable_courses_valid(timetable) and is_timetable_students_valid(timetable, schedule)


def get_schedule(timetable):
    schedule = {}

    for i in range(1000, 1838):
        schedule.setdefault(str(i), [])

    for sem in timetable:

        if sem == 'outside_timetable':
            for course_name in timetable[sem]:
                for student in timetable[sem][course_name]:
                    schedule[student].append(course_name)
        else:
            for i in range(4):
                for course_name in timetable[sem][i]:
                    for student in timetable[sem][i][course_name]:
                        schedule[student].append(course_name)
    
    with open('new_sch', 'w') as out_file:
        json.dump(schedule, out_file)
        
    return schedule

def is_timetable_courses_valid(timetable):
    
    for block in timetable:

        if '*' in block:    # if its a sim block

            all_courses_this_block = block.split('*')

            # check that all courses in this block are simultaneous with the first course
            for i in range(1, len(all_courses_this_block)):
                if all_courses_this_block[i] not in course_info[all_courses_this_block[0]]["Simultaneous"]:
                    print(all_courses_this_block[i] + " and " + all_courses_this_block[0] + " are not sim with each other")
                    return False

            max_capacity = course_info[all_courses_this_block[0]]["Max Enrollment"]
        else:
            max_capacity = course_info[block]["Max Enrollment"]

        # check that all courses is below max enrollment
        if len(timetable[block]) > max_capacity:
            print(timetable[block] + " exceeds max capacity")
            return False
        
    return True
        
def is_timetable_students_valid(timetable, student_schedules):
    # for all courses in a students' timetable for all students
    # for every course, check if it has pre req, then check if the prereq is before it
    # check for <= 8 total ocurses
    # for every not sim: check if in both sems
    # same for linear

    for student in student_schedules:
        if len(student_schedules[student]) < 8:
            return False

        for course in student_schedules[student]:

            # prereq
           
            if len(course_info[course]['Pre Req']) > 0:
                if course_info[course]['Pre Req'][0] in student_schedules[student]:
                    p = course_info[course]['Pre Req'][0]
                    # check in correct sem
                    if student_schedules[student].index(course_info[course]['Pre Req'][0]) < 4 and (student_schedules[student].index(course) >= 4 and student_schedules[student].index(course) <= 7):
                        # check didn't have prereq
                        if p in student_requests[student] and p not in student_schedules[student]:
                            return False
                    else: 
                        return False
            if len(course_info[course]['Not Simultaneous']) > 0:
                ns = course_info[course]['Not Simultaneous'][0]
                # check both not sim courses in sem1 and sem2 and same block
                if student_schedules[student].index(course) < 4 and student_schedules[student].index(ns) == student_schedules[student].index(course) + 4:
                    pass
                elif student_schedules[student].index(ns) < 4 and student_schedules[student].index(course) == student_schedules[student].index(ns) + 4:
                    pass
                else:
                    return False
                
            # linear course
            if course_info[course]['Base Terms/Year'] == '1':
                # check same course in both sem
                try:
                    second_occurrence = student_schedules[student](course, student_schedules[student].index(1) + 1)
                except ValueError:
                    second_occurrence = -1
                if student_schedules[student].index(course) < 4 and second_occurrence > 4:
                    pass
                else: return False
            
            # check no repeated course
            if course_info[course]['Base Terms/Year'] != '1':
                if student_schedules[student].count(course) > 1:
                    return False # multiple of the same course and not linear

                    
    return True

def who_got_8_courses(schedule):
    ans = []
    append = True

    for student in schedule:
        for course in schedule[student]:

            if course not in student_requests[student]:
                append = False
                break

            if student in student_alternates:
                if course in student_alternates[student]:
                    append = False
                    break

        if append: ans.append(student)
        append = True


    return ans

# takes in a timetable
# if any block is over max capacity, remove the students who didn't request for it
# if everyone in the overloaded block requested for that course, remove random student
# remove until the count is below max capacity
def remove_badstudents_from_overloaded_blocks(timetable):
    for sem in timetable:

        if sem == 'outside_timetable':
            for course_block in timetable[sem]:
                    while len(timetable[sem][course_block]) > int(course_info[course_block]['Max Enrollment']):
                        print("removed randomly from outside timetable course: " + course_block)
                        timetable[sem][course_block].pop(random.randint(0, len(timetable[sem][course_block])-1))
        else:
            for i in range(0, 4):
                for course_block in timetable[sem][i]:
                    courses = course_block.split('*')
                    while len(timetable[sem][i][course_block]) > int(course_info[courses[0]]['Max Enrollment']):
                        remove_a_student_from_this_block(sem, i, course_block, timetable)

def remove_a_student_from_this_block(sem, block, course_block, timetable):

    for student in timetable[sem][block][course_block]:

        courses = course_block.split("*")

        # remove people who just doesn't this course
        if all(course not in student_requests[student] for course in courses):
            print("removed: " + str(student) + " from " + sem + " block #" + str(block) + " course: " + course_block)
            timetable[sem][block][course_block].remove(student)
            return
        
        # next return people who has this course as alt
        if student in student_alternates:
            for course in courses:
                if  course in student_alternates[student]:
                    print("removed: " + str(student) + "from " + sem + " block #" + str(block) + " course: " + course_block)
                    timetable[sem][block][course_block].remove(student)
                    return
    
    # if everyone here is requested 8, remove random person
    timetable[sem][block][course_block].pop(random.randint(0, len(timetable[sem][block][course_block])-1))
    print("removed randomly from outside timetable course: " + course_block)


# prints the timetable in tabular form
def print_timetable(timetable):

    

    s1A = [course_info[course_code]['course name'] for full_code in timetable["sem1"][0].keys() for course_code in full_code.split('*')]
    s1B = [course_info[course_code]['course name'] for full_code in timetable["sem1"][1].keys() for course_code in full_code.split('*')]
    s1C = [course_info[course_code]['course name'] for full_code in timetable["sem1"][2].keys() for course_code in full_code.split('*')]
    s1D = [course_info[course_code]['course name'] for full_code in timetable["sem1"][3].keys() for course_code in full_code.split('*')]
    s2A = [course_info[course_code]['course name'] for full_code in timetable["sem2"][0].keys() for course_code in full_code.split('*')]
    s2B = [course_info[course_code]['course name'] for full_code in timetable["sem2"][1].keys() for course_code in full_code.split('*')]
    s2C = [course_info[course_code]['course name'] for full_code in timetable["sem2"][2].keys() for course_code in full_code.split('*')]
    s2D = [course_info[course_code]['course name'] for full_code in timetable["sem2"][3].keys() for course_code in full_code.split('*')]
    outside = [course_info[course_code]['course name'] for course_code in timetable["outside_timetable"].keys()]

    print("SEMESTER 1 A BLOCK:\n" + "\n".join(s1A) + "\n")
    print("SEMESTER 1 B BLOCK:\n" + "\n".join(s1B) + "\n")
    print("SEMESTER 1 C BLOCK:\n" + "\n".join(s1C) + "\n")
    print("SEMESTER 1 D BLOCK:\n" + "\n".join(s1D) + "\n")
    print("SEMESTER 2 A BLOCK:\n" + "\n".join(s2A) + "\n")
    print("SEMESTER 2 B BLOCK:\n" + "\n".join(s2B) + "\n")
    print("SEMESTER 2 C BLOCK:\n" + "\n".join(s2C) + "\n")
    print("SEMESTER 2 D BLOCK:\n" + "\n".join(s2D) + "\n")
    print("OUTSIDE TIMETABLE:\n" + "\n".join(outside) + "\n")

    s1A.insert(0, "SEMESTER 1 A BLOCK")
    s1B.insert(0, "SEMESTER 1 B BLOCK")
    s1C.insert(0, "SEMESTER 1 C BLOCK")
    s1D.insert(0, "SEMESTER 1 D BLOCK")
    s2A.insert(0, "SEMESTER 2 A BLOCK")
    s2B.insert(0, "SEMESTER 2 B BLOCK")
    s2C.insert(0, "SEMESTER 2 C BLOCK")
    s2D.insert(0, "SEMESTER 2 D BLOCK")
    outside.insert(0, "OUTSIDE TIMETABLE")

    data = [s1A, s1B, s1C, s1D, s2A, s2B, s2C, s2D, outside]

    file = open('timetable.csv', 'w+', newline ='')
 
    # writing the data into the file
    with file:   
        write = csv.writer(file)
        write.writerows(data)

    



# course_schedule only stores the courses, it doesn't give a shit about students
course_schedule = {}
course_schedule['sem1'] = [[],[],[],[]]
course_schedule['sem2'] = [[],[],[],[]]
course_schedule['outside_timetable'] = []

# initialize the blocks that have less than 42 blocks in them
available_blocks = ['1 A', '1 B', '1 C', '1 D', '2 A', '2 B', '2 C', '2 D']


#print(course_schedule)


def print_schedule(sem, block):
    
    # print schedule
    print(sem + str(block) + ':' )
    for a_class_code in course_schedule[sem][block]:

        print_line = ""

        if '*' in a_class_code:
            split = a_class_code.split('*')
            for course in split:
                print_line = print_line + course_info[course]['course name'] + " * "
        
        else:
            print_line = course_info[a_class_code]['course name']

        print(print_line)
    print(len(course_schedule[sem][block]))


def print_student(student_id, schedules):

    course_name = []
    spare_count = 0

    for i in range (len(schedules[student_id])):
        if schedules[student_id][i] is None:
            schedules[student_id][i] = "Spare"
            spare_count = spare_count + 1
            course_name.append("")
        else:
            course_name.append(course_info[schedules[student_id][i]]['course name'])

    print("Student id:  " + student_id)
    print("Sem 1 Block A:   " + schedules[student_id][0] + "    "  + course_name[0])
    print("Sem 1 Block B:   " + schedules[student_id][1] + "    "  + course_name[1])
    print("Sem 1 Block C:   " + schedules[student_id][2] + "    "  + course_name[2])
    print("Sem 1 Block D:   " + schedules[student_id][3] + "    "  + course_name[3])
    print("Sem 2 Block A:   " + schedules[student_id][4] + "    "  + course_name[4])
    print("Sem 2 Block B:   " + schedules[student_id][5] + "    "  + course_name[5])
    print("Sem 2 Block C:   " + schedules[student_id][6] + "    "  + course_name[6])
    print("Sem 2 Block D:   " + schedules[student_id][7] + "    "  + course_name[7])

    if len(schedules[student_id]) > 8:
        print("Outside Timetable:  " + schedules[student_id][8] + "    "  + course_name[8])

    return spare_count


# return a dictionary representing the course schedule (remove all students from timetable):
def get_course_schedule(timetable):
    
    schedule = copy.deepcopy(timetable)
    
    for block in schedule["sem1"]:
        for course in block:
            block[course].clear()
            
    for block in schedule["sem2"]:
        for course in block:
            block[course].clear()
    
    for course in schedule["outside_timetable"]:
        schedule["outside_timetable"][course].clear()
        
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
    
    best_students_1 = get_best_students(timetable_1)
    for student in best_students_1:
        student_ids.remove(student)
        dict_1[student] = student_schedules_1[student]
        
    best_students_2 = get_best_students(timetable_2)
    for student in best_students_2:
        if student in student_ids:
            student_ids.remove(student)
            dict_2[student] = student_schedules_2[student]
    
    while len(dict_1) < num_students:
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
        
    return new_timetable

# inserts a student into an existing timetable
def insert_student(timetable, student_id, student_schedule):
    
    for i in range(4):
        if student_schedule[i]:
            timetable["sem1"][i][student_schedule[i][0]].append(student_id)
    
    for i in range(4):
        if student_schedule[i + 4]:
            timetable["sem2"][i][student_schedule[i + 4][0]].append(student_id)
    
    for outside_timetable_course in student_schedule[8]:
        timetable["outside_timetable"][outside_timetable_course].append(student_id)
    

# returns a random timetable from a list, with a higher chance of choosing timetables with higher scores
def weighted_random_choice(timetables):

    fitness = [score(timetable, False) for timetable in timetables]
    total_score = 0

    for x in fitness:
        total_score += x

    prob_dist = [x / total_score for x in fitness]
    cumulative_dist = []
    sum = 0

    for i in range(len(prob_dist)):
        sum += prob_dist[i]
        cumulative_dist.append(sum)
    
    cumulative_dist.pop()
    cumulative_dist.append(1.0)

    rand = random.random()

    for i in range(0, len(timetables)):
        if rand < cumulative_dist[i]:
            return timetables[i]

# returns a list of all students with all requested or alternate courses  
def get_best_students(timetable):
    
    student_schedules = get_student_schedules(timetable)
    best_students = []
    num_missed = 0
    
    for student_id in student_requests:
        
        requested = student_requests[student_id]
        assigned = []

        for block in student_schedules[student_id]:
            for course in block:
                assigned = assigned + [x for x in course.split("*")]
                
        for course in requested:
            if course not in assigned:
                num_missed += 1
        
        if num_missed <= 2:
            best_students.append(student_id)
        
        num_missed = 1
        
    return best_students
                

'''
generate_course_schedule()

# create dictionary of dictionary version of course_schedule
# generate_timetable needs to use dis one
course_schedule2 = {}
course_schedule2['sem1'] = {
    'A': course_schedule['sem1'][0],
    'B': course_schedule['sem1'][1],
    'C': course_schedule['sem1'][2],
    'D': course_schedule['sem1'][3],
    'OT': course_schedule['outside_timetable']
}
course_schedule2['sem2'] = {
    'A': course_schedule['sem2'][0],
    'B': course_schedule['sem2'][1],
    'C': course_schedule['sem2'][2],
    'D': course_schedule['sem2'][3]
}

# genetic algorithm

def get_next_gen(current_gen):

    next_gen = []
    gen_size = len(current_gen)

    for i in range(3):
        timetable = get_best_timetable(current_gen)
        next_gen.append(timetable)
        current_gen.remove(timetable)

    for i in range(7):
        next_gen.append(generate_timetable(course_schedule2))

    while len(next_gen) < gen_size:

        parent_1 = weighted_random_choice(current_gen)
        parent_2 = weighted_random_choice(current_gen)

        if parent_1 == parent_2:
            continue

        child = cross(parent_1, parent_2)

        next_gen.append(child)

    return next_gen



def get_best_timetable(timetables):
    scores = [score(timetable, False) for timetable in timetables]

    max_index = scores.index(max(scores))

    return timetables[max_index]

gen_0 = []
for i in range(20):
    timetable = generate_timetable(course_schedule2)
    gen_0.append(timetable)

generations = [gen_0]

print("INITIAL POPULATION BEST TIMETABLE: ")
score(get_best_timetable(gen_0), True)
print()

num_generations = 6

for i in range(num_generations):
    generations.append([])

for i in range(1, 1 + num_generations):
    generations[i] = get_next_gen(generations[i - 1])
    print("GENERATION " + str(i) + " BEST TIMETABLE:")
    score(get_best_timetable(generations[i]), True)
    print()

best_timetable = get_best_timetable(generations[num_generations])

print("BEST TIMETABLE:")
score(best_timetable, True)
print()

with open('best_timetable.json', 'w') as fp:
    json.dump(best_timetable, fp)

not_overloaded_best_timetable = best_timetable
remove_badstudents_from_overloaded_blocks(not_overloaded_best_timetable)

print("NOT OVERLOADED BEST TIMETABLE:")
score(not_overloaded_best_timetable, True)
print()

with open('not_overlaaded_best_timetable.json', 'w') as fp:
    json.dump(not_overloaded_best_timetable, fp)

#print("INITIAL BEST TIMETABLE:")
#score(get_best_timetable(gen_0), True)



# print students with 8/8 requested

def print_perfect_students(timetable):
    
    print("8/8 students: ")
    student_schedules = get_student_schedules(timetable)
    success = True
    
    for student_id in student_requests:
        
        requested = student_requests[student_id]
        assigned = []

        for block in student_schedules[student_id]:
            for course in block:
                assigned = assigned + [x for x in course.split("*")]
                
        for course in requested:
            if course not in assigned:
                success = False

        if success:
            print(student_id + ": " + str(student_schedules[student_id]))

        success = True

#generate_course_schedule()


#print_perfect_students(best_timetable)




'''

generate_course_schedule()