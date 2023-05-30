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



# modifies the course_schedule dictionary:
# it ignores all courses with <=5 students requesting it
# let X = the available number of section of a course, then this course code appears in the dictionary X times
# its supposed to make sure that no 2 of the same courses appear in the same block in the same semester
# all simultaneous courses are one element of the list, each course code in that simultaneous bunch is seperated with a '*'
# rn as of May 26, it does not give a shit baout whether students would fill the course or not. its only going off of the available sections of each course
# for band and PE: band 9 and band 10 are both in sem 1, and their corresponding PE class is in sem 2 of the same block
# for Outside timetable courses they are all in 'OT' key of sem 1
def generate_course_schedule():

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

        if int(all_courseblock_codes[course_block]) > 8:
            all_courseblock_codes[course_block] = 8

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
            rand_block = return_rando_block(current_used_blocks).split(' ')                    # [semester#, block#]
            course_schedule['sem' + rand_block[0]][letter_to_num(rand_block[1])].append(course_block)      # put this course into the randomized 
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
    
# takes roughly 20 seconds to generate schedule
# generates a timetable with the schedule passed in
# paramater must be formatted as a dictionary with key A,B,C,D therefore use course sequence 2
# output schedule will have the same courses in each block as original passed in schedule but different order within blocks 
# ie schedule passed in has order 1234 in block A, the returned scheudle might have 2431 in block A
# all simultaneous courses are one element of the list, each course code in that simultaneous bunch is seperated with a '*'
# not sim courses are counted as 2 courses one in sem 1 and one in sem 2
# currently no way to determine order of two non simultaneous courses
# doesn't care about if a class has only a small amount of students
# code will run slower towards the end since students need to test more for which course they can take
def generate_timetable(schedule):
    student_courses = {}
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
        "sem1" : {
            'A':{},
            'B':{},
            'C':{},
            'D':{}
        },
        
        'sem2' : {
            'A':{},
            'B':{},
            'C':{},
            'D':{}
        },
        'outside_timetable' : {}
    }
    
    # empty list for all courses, following schedule
    # sem 1
    for c in schedule['sem1']['A']:
        timetable['sem1']['A'].setdefault(c, [])
   
    for c in schedule['sem1']['B']:
        timetable['sem1']['B'].setdefault(c, [])

    for c in schedule['sem1']['C']:
        timetable['sem1']['C'].setdefault(c, [])
    
    for c in schedule['sem1']['D']:
        timetable['sem1']['D'].setdefault(c, [])
    
    # sem 2
    for c in schedule['sem2']['A']:
        timetable['sem2']['A'].setdefault(c, [])
   
    for c in schedule['sem2']['B']:
        timetable['sem2']['B'].setdefault(c, [])

    for c in schedule['sem2']['C']:
        timetable['sem2']['C'].setdefault(c, [])
    
    for c in schedule['sem2']['D']:
        timetable['sem2']['D'].setdefault(c, [])
   
    # outside time table
    for c in schedule['sem1']['OT']: # why is ot under sem1???
        timetable['outside_timetable'].setdefault(c, [])
    
    
  
    # inside timetable courses
    # go through student info one student at a time
    iteration_count = 0
    for student in student_info:
        iteration_count += 1

        # Print something once every 20 students have been added to all their courses
        if iteration_count % 20 == 0:
            #print('added courses of 20 students') 
            pass 
        
        # keeps track of which blocks already have courses in sem 1, 2 and ot (ot not really used)
        blocks = {
            'sem1' : [],
            'sem2' : [],
            'outside' :[]
        }

        num_courses = 0 # number of courses this student already have (used later to determine how many extra random courses needed)
        
        courses_taking = [None for _ in range(8)] # list of courses already taking, initilize as 8 so that courses can be inserted at certain blocks

        num_alt = 0 # track how many alt courses needed (not really used, but can be used to see how successful this schedule is?)

        # create a dictionary of the courses choosen by the student, key as courses name and value as the priority of that course
        not_sorted_courses = student_info[student]
        course_priority = {}
        
        # create a dictionary 'course_name' : priority
        for course in not_sorted_courses:
            
            priority = course_info[course].get("Priority") # not sure how to determine if course is alternate, once determined add 5 to nonalt courses to prioritize it
            
            course_priority.setdefault(course, priority)

        # Sort their courses by priority (sort by value of a dictionary with 'course_name' : priority)
        sorted_courses = sorted(course_priority.items(), key=lambda item: item[1])
        sorted_courses =  [item[0] for item in sorted_courses]
            
        # Start with most prioritized courses
        length = len(sorted_courses)

        # go through all courses of the student
        for i in range(length):
           
            has_not_sim = False
          
            if len(sorted_courses) != 0:
                course = sorted_courses[0] # the current course being checked is the first in the list (will be removed when done so the next course will be pushed up)
            else:
                break # no more courses

            if num_courses > 8:
                break # number of courses reached max, ot courses do not add to num_courses
            
            # check if it is outside time table, if it is automatically add it and don't change the number of courses
            if (course_info[course]['Outside Timetable'] == True):
                if add_student('outside_timetable', course, timetable, schedule, student, blocks, False, False) != -1:
                    timetable = add_student('outside_timetable', course, timetable, schedule, student, blocks, False, True)
                    blocks['outside'].append(course)
                    courses_taking = add_course_list('outside_timetable', 'none', course, courses_taking)
                    sorted_courses.remove(course)
                else: 
                    sorted_courses.remove(course)
                    num_alt = num_alt + 1
            
            # Check if student meets blocking and seq
            # compares the pre req requirments with the other courses in list if more than 2, cannot do (cannot take cs 11, 12 and ap cs in a year)
            # if 1 pre req, keeps track of it
            num_pre_req = 0
           

            if len(course_info[course]['Pre Req']) != 0 or len(course_info[course]['Not Simultaneous']) != 0 or len(course_info[course]['Post Req']) != 0:
                for c in sorted_courses:
                    if c in course_info[course]['Pre Req']:
                        num_pre_req = num_pre_req + 1
                        pre_req = c
                    # checks if there are non sim courses and keeps track of it
                    if c in course_info[course]['Not Simultaneous']:
                        has_not_sim = True
                        not_sim = c
                    if c in course_info[course]['Post Req']: # moves post req course to the end and go through other courses so will deal with pre req first
                        sorted_courses.remove(course)
                        sorted_courses.append(course)
                        continue
                
                

            if num_pre_req > 1:

                # doesn't work, keep track to add an alt
                sorted_courses.remove(course)
                # i = i - 1
                num_alt = num_alt + 1
                continue
        
        
            # find course in schedule that does not contridict with student's current schedule and check if course is at max enrollment
            # deal with non generic scenarios first (not sim and pre req)

            # pre req
            if num_pre_req == 1:

                #check if both courses can be added correctly
                if add_student('sem1', pre_req, timetable, schedule, student, blocks, False, False) != -1:
                    if add_student('sem2', course, timetable, schedule, student, blocks, False, False) != -1:
                        
                        #add pre req in sem 1
                        timetable = add_student('sem1', pre_req, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem1', pre_req, timetable, schedule, student, blocks, True, False)
                        blocks['sem1'].append(block_added)   
                        courses_taking  = add_course_list('sem1', block_added, pre_req, courses_taking)
                        
                        # add this course (post req) in sem 2
                        timetable = add_student('sem2', course, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem2', course, timetable, schedule, student, blocks, True, False)
                        blocks['sem2'].append(block_added)    
                        courses_taking  = add_course_list('sem2', block_added, course, courses_taking)
                        
                        sorted_courses.remove(pre_req)
                        sorted_courses.remove(course)
                        num_courses = num_courses + 2
                        continue

                    # if cannot add both, check if can just add prereq in first sem
                    timetable = add_student('sem1', pre_req, timetable, schedule, student, blocks, False, True)
                    block_added = add_student('sem1', pre_req, timetable, schedule, student, blocks, True, False)
                    blocks['sem1'].append(block_added)    
                    sorted_courses.remove(pre_req)
                    courses_taking  = add_course_list('sem1', block_added, pre_req, courses_taking)
                    num_courses = num_courses + 1
                    continue

                # if doesn't work check just adding prereq in 2
                elif add_student ('sem2', pre_req, timetable, schedule, student, blocks, False, False) != -1:
                    timetable = add_student ('sem2', pre_req, timetable, schedule, student, blocks, False, True)
                    block_added = add_student('sem2', pre_req, timetable, schedule, student, blocks, True, False)
                    blocks['sem2'].append(block_added)    
                    courses_taking  = add_course_list('sem2', block_added, pre_req, courses_taking)  
                    sorted_courses.remove(pre_req)
                    num_courses = num_courses + 1
                    continue

                else:
                    sorted_courses.remove(pre_req)
                    sorted_courses.remove(course)
              
                    num_alt = num_alt + 2
                    continue # move to next course

            

            # deal with not sim courses
            if has_not_sim:
                # not sim courses (band and pe) are linear with band in sem 1 and pe in sem 2, going to put student in both courses
                if add_student('sem1', course, timetable, schedule, student, blocks, False, False) != -1:
                    if add_student('sem2', not_sim, timetable, schedule, student, blocks, False, False) != -1:
                        timetable = add_student('sem1', course, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem1', course, timetable, schedule, student, blocks, True, False)
                        blocks['sem1'].append(block_added)    
                        courses_taking  = add_course_list('sem1', block_added, course, courses_taking)

                        timetable = add_student('sem2', not_sim, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem2', not_sim, timetable, schedule, student, blocks, True, False)
                        blocks['sem2'].append(block_added)    
                        sorted_courses.remove(not_sim)
                        sorted_courses.remove(course)  
                        courses_taking  = add_course_list('sem2', block_added, not_sim, courses_taking)
                        
                        num_courses = num_courses + 2
                        continue
                elif add_student('sem2', course, timetable, schedule, student, blocks, False, False) != -1:
                    if add_student('sem1', not_sim, timetable, schedule, student, blocks, False, False) != -1:
                        timetable = add_student('sem2', course, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem2', course, timetable, schedule, student, blocks, True, False)
                        blocks['sem2'].append(block_added) 
                        courses_taking  = add_course_list('sem2', block_added, course, courses_taking)
                        
                        timetable = add_student('sem1', not_sim, timetable, schedule, student, blocks, False, True)
                        block_added = add_student('sem1', not_sim, timetable, schedule, student, blocks, True, False)
                        blocks['sem1'].append(block_added) 
                        sorted_courses.remove(not_sim)
                        sorted_courses.remove(course)
                        courses_taking  = add_course_list('sem1', block_added, not_sim, courses_taking)

                        num_courses = num_courses + 2
                        continue
                
                else: # no spots in one of the sim courses, remove both
                    sorted_courses.remove(course)
                    sorted_courses.remove(not_sim)
                    num_alt = num_alt + 2
                    continue
           
            # see if linear course, if linear add to both sem1 and sem 2 and this course takes 2 spots
            if course_info[course]['Base Terms/Year'] == '1' and course_info[course]['Covered Terms/Year'] == '1':
                if add_student('sem1', course, timetable, schedule, student, blocks, False, False) != -1 and add_student('sem2', course, timetable, schedule, student, blocks, False, False) != -1:
                    timetable = add_student('sem1', course, timetable, schedule, student, blocks, False, True)
                    block_added = add_student('sem1', course, timetable, schedule, student, blocks, True, False)
                    blocks['sem1'].append(block_added) 
                    courses_taking  = add_course_list('sem1', block_added, course, courses_taking)

                    timetable = add_student('sem2', course, timetable, schedule, student, blocks, False, True)
                    block_added = add_student('sem2', course, timetable, schedule, student, blocks, True, False)
                    blocks['sem2'].append(block_added) 
                    courses_taking  = add_course_list('sem2', block_added, course, courses_taking)
                    sorted_courses.remove(course)
               
                    num_courses = num_courses + 2
                    continue

                elif add_student('outside_timetable', course, timetable, schedule, student, blocks, False, False) != -1:
                    timetable = add_student('outside_timetable', course, timetable, schedule, student, blocks, False, True)
                    blocks['outside'].append(course)
                    courses_taking  = add_course_list('outside_timetable', 'none', course, courses_taking)

                    continue
                    
                else: 
                    
                    sorted_courses.remove(course)
                    continue
            
           
            # add students regularly, no sim, no prereq 
            if add_student('sem1', course, timetable, schedule, student, blocks, False, False) != -1:
                timetable = add_student('sem1', course, timetable, schedule, student, blocks, False, True) 
                block_added = add_student('sem1', course, timetable, schedule, student, blocks, True, False)
                blocks['sem1'].append(block_added) 
                sorted_courses.remove(course)
                courses_taking  = add_course_list('sem1', block_added, course, courses_taking)

                num_courses = num_courses + 1
                continue

            # if sem1 doesn't have space check sem 2
            elif add_student('sem2', course, timetable, schedule, student, blocks, False, False) != -1:
                timetable = add_student('sem2', course, timetable, schedule, student, blocks, False, True) 
                block_added = add_student('sem2', course, timetable, schedule, student, blocks, True, False)
                blocks['sem2'].append(block_added) 
                sorted_courses.remove(course)
                num_courses = num_courses + 1
                courses_taking  = add_course_list('sem2', block_added, course, courses_taking)

                continue
            else: # cannot add course
                sorted_courses.remove(course)
                num_alt = num_alt + 1
                continue
                    
        # need to deal with alt?

        # assign random course if the courses student assigned is not avaliable
        # assigns the next course and relatively not priorizted course (p > 20)
        
        for course in course_info:
            is_post_req = False
            if num_courses == 8:
                break

            
            if course not in courses_taking:
                    if course_info[course]['Outside Timetable'] == False:
                        if len(course_info[course]['Pre Req']) == 0:
                            if len(course_info[course]['Not Simultaneous']) == 0:
                                if course_info[course]['Base Terms/Year'] != '1' and course_info[course]['Covered Terms/Year'] != '1':
                                    if add_student('sem1', course, timetable, schedule, student, blocks, False, False) != -1:
                                    
                                        timetable = add_student('sem1', course, timetable, schedule, student, blocks, False, True)
                                        block_added = add_student('sem1', course, timetable, schedule, student, blocks, True, False)
                                        blocks['sem1'].append(block_added) 
                                        
                                        courses_taking  = add_course_list('sem1', block_added, course, courses_taking)
                                        num_courses = num_courses + 1
                                    elif add_student('sem2', course, timetable, schedule, student, blocks, False, False) != -1:
                                        timetable = add_student('sem2', course, timetable, schedule, student, blocks, False, True)
                                        block_added = add_student('sem2', course, timetable, schedule, student, blocks, True, False)
                                        blocks['sem2'].append(block_added) 
                                        
                                        courses_taking  = add_course_list('sem2', block_added, course, courses_taking)
                                        num_courses = num_courses + 1
            
        if iteration_count > 700:
            print('')

        student_courses.setdefault(student, courses_taking)
    
    with open('timetable.json', 'w') as out_file:
     json.dump(timetable, out_file)

    # format table to correct list style
    formatted_timetable = {
        "sem1": [
            timetable['sem1']['A'], # A
            timetable['sem1']['B'], # B
            timetable['sem1']['C'], # C
            timetable['sem1']['D'] # D
            
        ],
        "sem2" : [
            timetable['sem2']['A'], # A
            timetable['sem2']['B'], # B
            timetable['sem2']['C'], # C
            timetable['sem2']['D'] # D
        ],

        "outside_timetable": timetable['outside_timetable']           
    }
    return formatted_timetable, student_courses
def add_course_list (sem, block, course, list):
    if sem == 'sem1':
        if block == 'A':
            list [0] = course
        elif block == 'B':
            list [1] = course
        elif block == 'C':
            list [2] = course
        elif block == 'D':
            list [3] = course
    elif sem == 'sem2':
        if block == 'A':
            list [4] = course
        elif block == 'B':
            list [5] = course
        elif block == 'C':
            list [6] = course
        elif block == 'D':
            list[7] = course
    elif sem == 'outside_timetable':
        list.append(course)
    
    return list
        
# finds the avaliable course in a semester and attempts to add student to the course
# if no avaliable course, return -1
# if parameter is_find_block = true, returns the block this student is being added to
# method ordered and the way it is called ensures that student will be only added at the right time
# always use this method so that check if courses are avaliable first (!= -1)
# if avaliable then add student or get block
# be careful not to accidently add student two times since this method is used for multiple things
# deals with simultaneous courses by replacing the timetable original timetable key that has * with the single course name being used (CS11*CS12  ---> CS11) and at the end of the method switch the keys back for both schedule and dictionary
# if sim course, the order of the dictionary will change ([1, 2, CS11*CS12, 3, 4]  -----> [1, 2, 3, 4, CS11*CS12])
def add_student (sem, course, timetable, schedule, student, blocks, is_find_block, is_append):
    
    can_add = False # can this student be added (are they already taking this course and is max enrollment reached)
    max_enroll = int(course_info[course]['Max Enrollment'])

    # for sim courses
    switch_a = False 
    switch_b = False
    switch_c = False
    switch_d = False
    original_key = ''
    
    # switch keys for sim courses
    if sem != 'outside_timetable':
        for x in range(1):
            for i in range (len(schedule[sem]['A'])):
                if course + '*' in schedule[sem]['A'][i] or '*' + course in schedule[sem]['A'][i]:
                    original_key = schedule[sem]['A'][i]
                    
                    timetable[sem]['A'][course] = timetable[sem]['A'].pop(original_key)
                    schedule[sem]['A'].remove(original_key)
                    schedule[sem]['A'].append(course)
                    
                    switch_a = True
                    break
            if switch_a :
                break
            for i in range (len(schedule[sem]['B'])):
                if course + '*' in schedule[sem]['B'][i] or '*' + course in schedule[sem]['B'][i]:
                    original_key = schedule[sem]['B'][i]
                   
                    timetable[sem]['B'][course] = timetable[sem]['B'].pop(original_key)
                    schedule[sem]['B'].remove(original_key)
                    schedule[sem]['B'].append(course)
                   
                    switch_b = True
                    break
            if switch_b :
                break
            for i in range (len(schedule[sem]['C'])):
                if course + '*' in schedule[sem]['C'][i] or '*' + course in schedule[sem]['C'][i]:
                    original_key = schedule[sem]['C'][i]
                    
                    timetable[sem]['C'][course] = timetable[sem]['C'].pop(original_key)
                    schedule[sem]['C'].remove(original_key)
                    schedule[sem]['C'].append(course)
                    switch_c = True
                    break
            if switch_c :
                break
            for i in range (len(schedule[sem]['D'])):
                if course + '*' in schedule[sem]['D'][i] or '*' + course in schedule[sem]['D'][i]:
                    original_key = schedule[sem]['D'][i]
                    
                    timetable[sem]['D'][course] = timetable[sem]['D'].pop(original_key)
                    schedule[sem]['D'].remove(original_key)
                    schedule[sem]['D'].append(course)
                    switch_d = True
                    break
    
    
    # return correct block if student already enrolled in this class
    if sem == 'outside_timetable':
        
        if course in timetable[sem]:
            if len(timetable[sem][course]) < max_enroll:
                can_add = True

    elif course in schedule[sem]['A']:
        if student in timetable[sem]['A'][course]:
            block = 'A'
    elif course in schedule[sem]['B']:
        if student in timetable[sem]['B'][course]:
            block = 'B'
    elif course in schedule[sem]['C']:
        if student in timetable[sem]['C'][course]:
            block = 'C'
    elif course in schedule[sem]['D']:
         if student in timetable[sem]['D'][course]:
            block = 'D'



    # see if student fits or add student or return block
    if sem != 'outside_timetable':
        if course in schedule[sem]['A'] and 'A' not in blocks[sem]:
            block = 'A'
            if len(timetable[sem]['A'][course]) < max_enroll:
                can_add = True 
                
                if is_append:
                    if(student not in timetable[sem]['A'][course]):
                        timetable[sem]['A'][course].append(student) 

        elif course in schedule[sem]['B'] and 'B' not in blocks[sem]:
            block = 'B'
            if len(timetable[sem]['B'][course]) < max_enroll:
                
                can_add = True 
                
                if is_append:
                    if(student not in timetable[sem]['B'][course]):
                        timetable[sem]['B'][course].append(student)                  

        elif course in schedule[sem]['C'] and 'C' not in blocks[sem]:
            block = 'C'
            if len(timetable[sem]['C'][course]) < max_enroll:
            
                can_add = True 
                
                if is_append:
                    if(student not in timetable[sem]['C'][course]):
                        timetable[sem]['C'][course].append(student)                  

        elif course in schedule[sem]['D'] and 'D' not in blocks[sem]:
            block = 'D'
            if len(timetable[sem]['D'][course]) < max_enroll:
                can_add = True 
                if is_append:
                    if(student not in timetable[sem]['D'][course]):
                        timetable[sem]['D'][course].append(student) 

    # if switched for sim, switch back
    if switch_a:
        timetable[sem]['A'][original_key] = timetable[sem]['A'].pop(course)
        schedule[sem]['A'].remove(course)
        schedule[sem]['A'].append(original_key)
    elif switch_b:
        timetable[sem]['B'][original_key] = timetable[sem]['B'].pop(course)
        schedule[sem]['B'].remove(course)
        schedule[sem]['B'].append(original_key)
    elif switch_c:
        timetable[sem]['C'][original_key] = timetable[sem]['C'].pop(course)
        schedule[sem]['C'].remove(course)
        schedule[sem]['C'].append(original_key)
    elif switch_d:
        timetable[sem]['D'][original_key] = timetable[sem]['D'].pop(course)
        schedule[sem]['D'].remove(course)
        schedule[sem]['D'].append(original_key)
                
    if is_find_block:
        return block
    
    if can_add:
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
            for student in block[course]:

                if student in student_schedules:
                    student_schedules[student].append(course)
                else:
                    student_schedules[student] = [course]
    
    for block in timetable["sem2"]:
        for course in block:
            for student in block[course]:

                if student in student_schedules:
                    student_schedules[student].append(course)
                else:
                    student_schedules[student] = [course]

    for course in timetable["outside_timetable"]:
        for student in timetable["outside_timetable"][course]:

            if student in student_schedules:
                student_schedules[student].append(course)
            else:
                student_schedules[student] = [course]

    return student_schedules



# return the proportion of students who received all of their desired courses
def score(student_schedules):

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

    s1A = [course_info[course_code]['course name'] for full_code in timetable["sem1"][0].keys() for course_code in full_code.split('*')]
    s1B = [course_info[course_code]['course name'] for full_code in timetable["sem1"][1].keys() for course_code in full_code.split('*')]
    s1C = [course_info[course_code]['course name'] for full_code in timetable["sem1"][2].keys() for course_code in full_code.split('*')]
    s1D = [course_info[course_code]['course name'] for full_code in timetable["sem1"][3].keys() for course_code in full_code.split('*')]
    s2A = [course_info[course_code]['course name'] for full_code in timetable["sem2"][0].keys() for course_code in full_code.split('*')]
    s2B = [course_info[course_code]['course name'] for full_code in timetable["sem2"][1].keys() for course_code in full_code.split('*')]
    s2C = [course_info[course_code]['course name'] for full_code in timetable["sem2"][2].keys() for course_code in full_code.split('*')]
    s2D = [course_info[course_code]['course name'] for full_code in timetable["sem2"][3].keys() for course_code in full_code.split('*')]

    print("SEMESTER 1 A BLOCK:\n" + ", ".join(s1A) + "\n")
    print("SEMESTER 1 B BLOCK:\n" + ", ".join(s1B) + "\n")
    print("SEMESTER 1 C BLOCK:\n" + ", ".join(s1C) + "\n")
    print("SEMESTER 1 D BLOCK:\n" + ", ".join(s1D) + "\n")
    print("SEMESTER 2 A BLOCK:\n" + ", ".join(s2A) + "\n")
    print("SEMESTER 2 B BLOCK:\n" + ", ".join(s2B) + "\n")
    print("SEMESTER 2 C BLOCK:\n" + ", ".join(s2C) + "\n")
    print("SEMESTER 2 D BLOCK:\n" + ", ".join(s2D) + "\n")



def get_student_timetable(student_id, timetable):

    print(get_student_schedules(timetable)[student_id])

# course_schedule only stores the courses, it doesn't give a shit about students
course_schedule = {}
course_schedule['sem1'] = [[],[],[],[]]
course_schedule['sem2'] = [[],[],[],[]]
course_schedule['outside_timetable'] = []

# initialize the blocks that have less than 42 blocks in them
available_blocks = ['1 A', '1 B', '1 C', '1 D', '2 A', '2 B', '2 C', '2 D']


#print(course_schedule)
with open('student_requests.json') as f:
        student_request = json.load(f)


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

s = generate_course_schedule()

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

with open('courses.json') as f:
    course_info = json.load(f)

timetable, schedules = generate_timetable(course_schedule2)
#print(timetable)

print_timetable(timetable)

student_id = str(random.randint(1000, 1837))
print(student_id)

print([course_info[course_code]["course name"] for course_code in schedules[student_id]])



print(score(schedules))

'''
# generate initial guess
initial_timetable = generate_timetable(course_schedule2)
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


print(initial_timetable)



print(score(initial_timetable))
print(final_timetable)
print(score(final_timetable))

'''