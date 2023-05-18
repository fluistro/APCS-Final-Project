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
        'Sections': sections,
        'Students': [],
        'Simultaneous' : [],
        'Not Simultaneous': []
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
            if (row[0] == 'XLEAD09---'):
                continue

            if (row[0] == 'MEFWR10---'):
                continue

            if (row[0] == 'MGE--12' or row[0] == 'MGE--11'):
                continue

            if (row[0] == 'MKOR-10---' or row[0] == 'MKOR-11---' or row[0] == 'MKOR-12---'):
                continue 

            if (row[0] == 'MIT--12---'):
                continue           

            if (row[0] == 'YESFL1AX--'):
                continue         

            if (row[0] == 'MSPLG11---'):
                continue    

            if (row[0] == 'MJA--10---' or row[0] == 'MJA--11---' or row[0] == 'MJA--12---'):
                continue   
            
            course_info[row[0]]['Students'].append(current_student_id)

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
       
        if line [-26:] != "in a Simultaneous blocking":  
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
#for a in course_info:
 #  print(a, course_info[a]['Simultaneous'], course_info[a]['Not Simultaneous'])
            #print(course_info)
print(course_info.keys())    

print (course_info)
                 



# write course_info to txt file

with open('courses.txt', 'w') as convert_file:
     convert_file.write(json.dumps(course_info))

