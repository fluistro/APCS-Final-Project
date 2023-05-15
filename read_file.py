import csv
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

print(course_info)


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






# read Course Blocking Rules



# read Course Sequencing Rules
