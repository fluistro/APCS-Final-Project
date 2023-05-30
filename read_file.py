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
student_requests = {}
student_alternates = {}

'''
{1000: [course list]
 1001: []
 ...
 }
'''

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
        'Sections': sections,
        'Students': [],
        'Pre Req' : [],
        'Post Req': [],
        'Simultaneous' : [],
        'Not Simultaneous': [],
        'Term Blocking' : [],
        'Outside Timetable' : False
    }

# read Cleaned Student Requests
current_student_id = 0
skip_header_line = False
current_line_splitted = ""
with open('Cleaned Student Requests.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
        
        # if current line is the start of a new student
        if (len(row) == 2):
            skip_header_line = True
            current_student_id = row[1]

        # if current line is not the start of a new student
        else:

            # if its the header line
            if (skip_header_line == True):
                skip_header_line = False
                continue

            # if the course requested is NOT THERE!!!!
            if not row[0] in course_info:
                if (row[0] == 'XLEAD09---'):
                        course_info['XLEAD09---'] = {
                            'course name': 'Leadership 9',
                            'Base Terms/Year': 1,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 200,
                            'PPC': 2,
                            'Priority': 50,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }

                if (row[0] == 'MEFWR10---'):
                        course_info['MEFWR10---'] = {
                            'course name': 'EFP Literary Studies 10',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 24,
                            'PPC': 2,
                            'Priority': 20,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                
                if (row[0] == 'MGE--12' or row[0] == 'MGE--11'):
                        course_info['MGE--12'] = {
                            'course name': 'German 12',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        course_info['MGE--11'] = {
                            'course name': 'German 11',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }

                if (row[0] == 'MKOR-10---' or row[0] == 'MKOR-11---' or row[0] == 'MKOR-12---'):
                        # this course is not in the csv file
                        # guess of the specifications of this course:
                        course_info['MKOR-10---'] = {
                            'course name': 'Korean 10',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        course_info['MKOR-11---'] = {
                            'course name': 'Korean 11',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        course_info['MKOR-12---'] = {
                            'course name': 'Korean 12',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }

                if (row[0] == 'MIT--12---'):
                        # this course is not in the csv file
                        # guess of the specifications of this course: (based from website)
                        course_info['MIT--12---'] = {
                            'course name': 'Italian 12',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        # https://mountdougcourses.sd61.bc.ca/courses/italian-12/      

                if (row[0] == 'YESFL1AX--'):
                        # this course is not in the csv file
                        # guess of the specifications of this course: (based from website)
                        course_info['YESFL1AX--'] = {
                            'course name': 'ELL 11 & 12 Support',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 24,
                            'PPC': 2,
                            'Priority': 10,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        # https://mountdougcourses.sd61.bc.ca/courses/ell-support-blocks-learning-strategies/       

                if (row[0] == 'MSPLG11---'):
                        course_info['MSPLG11---'] = {
                            'course name': 'SPOKEN LANGUAGE 11',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 24,
                            'PPC': 2,
                            'Priority': 10,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }  

                if (row[0] == 'MJA--10---' or row[0] == 'MJA--11---' or row[0] == 'MJA--12---'):
                        course_info['MJA--10---'] = {
                            'course name': 'Japanese 10',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        course_info['MJA--11---'] = {
                            'course name': 'Japanese 11',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
                        course_info['MJA--12---'] = {
                            'course name': 'Japanese 12',
                            'Base Terms/Year': 2,
                            'Covered Terms/Year': 1,
                            'Max Enrollment': 29,
                            'PPC': 2,
                            'Priority': 15,
                            'Sections': 1,
                            'Students': [],
                            'Pre Req' : [],
                            'Post Req': [],
                            'Simultaneous' : [],
                            'Not Simultaneous': [],
                            'Term Blocking' : [],
                            'Outside Timetable' : False
                        }
            
            course_info[row[0]]['Students'].append(current_student_id)

            if current_student_id in student_requests:
                student_requests[current_student_id].append(row[0])
            else:
                student_requests[current_student_id] = [row[0]]

            if row[11] == "Y":
                if current_student_id in student_alternates:
                    student_alternates[current_student_id].append(row[0])
                else:
                    student_alternates[current_student_id] = [row[0]]


# read Course Blocking Rules
# need to read file twice, one time for sim, one time for not sim since not sim depends on the read info of sim
with open('Course Blocking Rules.csv', 'r') as file:
    reader = csv.reader(file)
    sim = {}

    counter = 0
    sim_courses_list = []
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


            sim_courses_list = [value.strip() for value in sim]
         
            # create key Post Req with value list post_req
            for c in set(sim_courses_list):
                if c not in course_info[course]['Simultaneous']:
                    course_info[course]['Simultaneous'].append(c)
                

            for i in sim:

                i = i.strip()
                if not(course.strip() in course_info[course]['Simultaneous']):
                    course_info[i]['Simultaneous'].append(course.strip())
                        
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
       
        if line [-26:] != "in a Simultaneous blocking" and line[-19:] != 'in a Terms blocking':  
            not_sim_courses = line [0: -30]
            not_sim = not_sim_courses.split(", ")
        
            not_sim_copy = []
        
            for string in not_sim:
                if not (string.strip() in course_info[course]["Simultaneous"] or string.strip() in course_info[course]['Not Simultaneous']):
                    
                    not_sim_copy.append(string)
            
            course_info[course]["Not Simultaneous"] = not_sim_copy
            if not_sim_copy[0] == '': continue
            #print(not_sim_copy)
            for i in not_sim_copy:
                i = i.strip()
                course_info[i]['Not Simultaneous'].append(course.strip())
        
    course_info['MSPLG10--L']['Term Blocking'].append('YESFL0AX-L')
    course_info['YESFL0AX-L']['Term Blocking'].append('MSPLG10--L')              

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
                for c in post_req:
                    course_info[id]["Post Req"].append(c)
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
# add key to keep track of outside timetable courses
# grade 9
course_info['XC---09--L']['Outside Timetable'] = True
course_info['MDNC-09C-L']['Outside Timetable'] = True
course_info['MDNC-09M-L']['Outside Timetable'] = True
course_info['XBA--09J-L']['Outside Timetable'] = True
course_info['XLDCB09S-L']['Outside Timetable'] = True


# grade 10
course_info['YCPA-0AX-L']['Outside Timetable'] = True
course_info['MMUCC10--L']['Outside Timetable'] = True
course_info['MDNC-10--L']['Outside Timetable'] = True
course_info['MDNCM10--L']['Outside Timetable'] = True
course_info['YCPA-0AXE-']['Outside Timetable'] = True
course_info['MIDS-0C---']['Outside Timetable'] = True
course_info['YED--0BX-L']['Outside Timetable'] = True
course_info['MMUOR10S-L']['Outside Timetable'] = True
course_info['MMUJB10--L']['Outside Timetable'] = True

# grade 11
course_info['MDNC-11--L']['Outside Timetable'] = True
course_info['MDNCM11--L']['Outside Timetable'] = True
course_info['MGMT-12L--']['Outside Timetable'] = True
course_info['MCMCC11--L']['Outside Timetable'] = True
course_info['MIMJB11--L']['Outside Timetable'] = True
course_info['MMUOR11S-L']['Outside Timetable'] = True
course_info['YCPA-1AX-L']['Outside Timetable'] = True
course_info['YCPA-1AXE-']['Outside Timetable'] = True
course_info['MGRPR11--L']['Outside Timetable'] = True
course_info['YED--1EX-L']['Outside Timetable'] = True
course_info['MWEX-2A--L']['Outside Timetable'] = True
course_info['MWEX-2B--L']['Outside Timetable'] = True

# grade 12
course_info['MDNC-12--L']['Outside Timetable'] = True
course_info['MDNCM12--L']['Outside Timetable'] = True
course_info['MGMT-12L--']['Outside Timetable'] = True
course_info['MIMJB12--L']['Outside Timetable'] = True
course_info['MMUOR12S-L']['Outside Timetable'] = True
course_info['YCPA-2AXE-']['Outside Timetable'] = True
course_info['YED--2DX-L']['Outside Timetable'] = True
course_info['YED--2FX-L']['Outside Timetable'] = True
course_info['MWEX-2A--L']['Outside Timetable'] = True
course_info['MWEX-2B--L']['Outside Timetable'] = True
course_info['MCMCC12--L']['Outside Timetable'] = True
course_info['YCPA-2AX-L']['Outside Timetable'] = True
course_info['MGRPR12--L']['Outside Timetable'] = True

# write course_info to txt file


with open('courses.json', 'w') as out_file:
     json.dump(course_info, out_file)


with open('student_requests.json', 'w') as out_file:
     json.dump(student_requests, out_file)

with open('student_alternates.json', 'w') as out_file:
     json.dump(student_alternates, out_file)

