import pandas as pd

df = pd.read_csv('Course Information.csv')

for line in df:
    print(line)
'''
{
    'course1': {
        'Base Terms/Year': 0,
        'Covered Terms/Year': 0,
        'Max Enrollment': 30,
        'PPC': 0,
        'Priority': 0,
        'Sections': 0,
        'Prereqs': 0,
        'Postreqs': 0,
        'Sim With this course': 0, 
        'no sim With this course': 0,
        'Selected by students': 0,
    },
    ...
}


'''