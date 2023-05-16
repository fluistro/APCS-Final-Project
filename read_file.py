import csv
import json

'''

with open('Course Sequencing Rules.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))

{
    'course code 1': {
        'course name': "",
        'Base Terms/Year': 0,
        'Covered Terms/Year': 0,
        'Max Enrollment': 0,
        'PPC': 0,
        'Priority': 0,
        'Sections': 0,
        'Prereqs': [courses],
        'Postreqs': [courses],
        'Simultaneous': [courses], 
        'NotSimultaneous': [courses],
        'Students': [student ID list]
    },
    'course2': {...}
    ...
}
'''

# dictionary
course_info = {}

# read Course Information
f = open("Course Information.csv", "r")

while True:

    # check if end of file reached
    line = f.readline()
    if (line == ""):
        break

    # skip past page headers
    if (line == "Greater Victoria,,,,,,,,,,,,,Mount Douglas Secondary,,,,,\n"):
        f.readline()
        f.readline()
        f.readline()
        continue

    line = line.split(",")

    id = line[0]
    name = line[2]
    base_terms = line[7]
    covered_terms = line[8]
    max_enrollment = line[9]
    ppc = line[10]
    priority = line[12]
    sections = line[14]

    course_info[id] = {
        'course name': name,
        'Base Terms/Year': base_terms,
        'Covered Terms/Year': covered_terms,
        'Max Enrollment': max_enrollment,
        'PPC': ppc,
        'Priority': priority,
        'Sections': sections
    }


'''

# read Cleaned Student Requests
current_student_id = 0
skip_header_line = False
current_line_splitted = ""
with open('Cleaned Student Requests.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        current_line_splitted = row.split(",")
        
        # if current line is the start of a new student
        if (len(current_line_splitted) == 2):
            skip_header_line = True
            current_student_id = current_line_splitted[1]

        # if current line is not the start of a new student
        else:
            # if its the header line
            if (skip_header_line == True):
                continue

            skip_header_line = False
            course_info[current_line_splitted[0]]['Students'].append(current_student_id)




'''

# read Course Blocking Rules
# need to read file twice, one time for sim, one time for not sim since not sim depends on the read info of sim
with open('Course Blocking Rules.csv', 'r') as file:
    reader = csv.reader(file)
    sim = {}

    counter = 0
    for row in reader:

        counter = counter + 1
        # skip no info lines
        if (counter == 1 or counter == 2 or counter == 3 or counter == 4 or counter == 5 or counter == 38 or counter == 39 or counter == 40 or counter == 41 or counter == 42 or counter == 43):
            continue

        # getting course name
        r = row[2]
        course = r [9:]
        course = course[:course.index(",")]
      
        # getting sim courses
        line = r[r.index(",") + 2:]
        
        if line [-26:] == "in a Simultaneous blocking":
            sim_courses = line [0: -26]
            sim = sim_courses.split(", ")


            # strip for space
            for str in sim:
                str = str.strip()

            for id in course_info:
             
                # remove whitespace and compare
                if id == course:
            
                    # create key Post Req with value list post_req
                    course_info[id].setdefault('Simultaneous', sim)
                    
with open('Course Blocking Rules.csv', 'r') as file:
    reader = csv.reader(file)
    not_sim = {}

    counter = 0
    for row in reader:

        counter = counter + 1
        # skip no info lines
        if (counter == 1 or counter == 2 or counter == 3 or counter == 4 or counter == 5 or counter == 38 or counter == 39 or counter == 40 or counter == 41 or counter == 42 or counter == 43):
            continue

        # getting course name
        r = row[2]
        course = r [9:]
        course = course[:course.index(",")]
      
        # getting sim courses
        line = r[r.index(",") + 2:]
        
        if line [-26:] != "in a Simultaneous blocking":   
            not_sim_courses = line [0: -30]
            not_sim = not_sim_courses.split(", ")
            is_run = False
            for id in course_info:
             
                # remove whitespace and compare
                if id == course:
            
                    # create key Post Req with value list post_req
                    # remove from not sim if sim already exists
                    for str in not_sim:
                        str = str.strip()
                        if "Simultaneous" in course_info[id]:
                            if str in course_info[id]["Simultaneous"]:
                                continue
                            
                            course_info[id].setdefault('Not Simultaneous', not_sim.remove(str))
                            is_run = True
                          
                        
                   
                    if not is_run:
                         course_info[id].setdefault('Not Simultaneous', not_sim)
                        # print ( course_info[id])
                        

print(course_info)                       
'''
        else:
            not_sim_courses = line [0: -30]
            not_sim = not_sim_courses.split(", ")
            for id in course_info:
             
                # remove whitespace and compare
                if id == course:
            
                    # create key Post Req with value list post_req
                    # remove from not sim if sim already exists
                    for str in not_sim:
                        if "Simultaneous" in course_info[id]:
                            if course_info[id]["Simultaneous"] == course:
                                continue
                        course_info[id].setdefault('Not Simultaneous', not_sim)
                        print(course_info[id])



        post = course [course.index("before") + 7 :]
        course = course[:course.index("before")]
        post_req = post.split(", ")



        # find correct course and update info
        for id in course_info:
             
             # remove whitespace and compare
             if id.strip() == course.strip():

                # remove space before and after course before storing
                for str in post_req:
                    str.strip()

                # create key Post Req with value list post_req
                course_info[id].setdefault('Post Req', post_req)
                #print(course_info[id])
        
        # update pre req
        pre_req = []
        for post_req_str in post_req:
            for id in course_info:
                if post_req_str.strip() == id.strip():
                    if "Pre Req" in course_info[id]:
                        if course.strip() not in course_info[id]["Pre Req"]:
                            course_info[id]["Pre Req"].append(course.strip())
            
            if course.strip() not in pre_req:
                pre_req.append(course.strip())
                course_info[id]["Pre Req"] = pre_req

        '''
       
# read Course Sequencing Rules

with open('Course Sequencing Rules.csv', 'r') as file:
    reader = csv.reader(file)
    post_req = {}
    counter = 0
    for row in reader:

        counter = counter + 1
        # skip no info lines
        if (counter == 1 or counter == 2 or counter == 3 or counter == 4 or counter == 5 or counter == 43 or counter == 44 or counter == 45 or counter == 46 or counter == 47):
            continue

        # getting course name
        r = row[2]
        course = r [8:]
        post = course [course.index("before") + 7 :]
        course = course[:course.index("before")]
        post_req = post.split(", ")



        # find correct course and update info
        for id in course_info:
             
             # remove whitespace and compare
             if id.strip() == course.strip():

                # remove space before and after course before storing
                for str in post_req:
                    str.strip()

                # create key Post Req with value list post_req
                course_info[id].setdefault('Post Req', post_req)
                #print(course_info[id])
        
        # update pre req
        pre_req = []
        for post_req_str in post_req:
            for id in course_info:
                if post_req_str.strip() == id.strip():
                    if "Pre Req" in course_info[id]:
                        if course.strip() not in course_info[id]["Pre Req"]:
                            course_info[id]["Pre Req"].append(course.strip())
            
            if course.strip() not in pre_req:
                pre_req.append(course.strip())
                course_info[id]["Pre Req"] = pre_req

# write course_info to txt file
'''
with open('courses.txt', 'w') as convert_file:
     convert_file.write(json.dumps(course_info))
'''
