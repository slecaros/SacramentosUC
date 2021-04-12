import csv
from unidecode import unidecode

############## CHANGE THIS LINES ##############
# Catechized data positioning
catechized_file = '1_sem_2021/sacramentados.tsv'
catechized_gender = 2
catechized_name = 0
catechized_schedule = 6
# Catechist data positioning
catechists_file = '1_sem_2021/catequistas.tsv'
catechists_gender = 2
catechists_name = 0
catechists_schedule = 6
# Monitor data positioning
monitors_file = '1_sem_2021/asesores.tsv'
monitors_gender = 2
monitors_name = 1
monitors_schedule = 6
###############################################

campuses = {'San Joaquin': 0,
    'Casa Central':1,
    'Lo Contador': 2,
    'Oriente': 3}

modules = {'8:30-9:50': 0,
    '10:00-11:20': 1,
    '11:30-12:50': 2,
    '14:00-15:20': 3,
    '15:30-16:50': 4,
    '17:00-18:20': 5,
    '18:30-19:50': 6}

weekdays = {'Lunes': 0,
    'Martes': 1,
    'Miércoles': 2,
    'Jueves': 3,
    'Viernes': 4}


def get_availability(file_, name_column, schedule_column):
    availability = dict()
    with open(file_) as f:
        f = csv.reader(f,delimiter="\t", quotechar='"')
        next(f)    
        for line in f:
            person_name = f"{unidecode(line[name_column])} {unidecode(line[name_column + 1])}"
            availability[person_name] = dict()
            for campus in range(4):
                av_modules = [0 for _ in range(35)]
                module_number = 0
                for module in line[(schedule_column+(7*campus)): (schedule_column+(7*(campus+1)))]:
                    # print(f"file: '{file_}'\tmodulo: '{module}'")
                    for day in module.split(', '):
                        if day != '':
                            day_module_pos = weekdays[day]*7 + module_number
                            av_modules[day_module_pos] = 1
                    module_number += 1
                availability[person_name][campus] = av_modules
    return availability

def get_gender (file_, gender_column, name_column):
    male = []
    female = []
    with open(file_) as f:
        f = csv.reader(f,delimiter="\t", quotechar='"')
        next(f)    
        for line in f:
            person_name = f"{unidecode(line[name_column])} {unidecode(line[name_column + 1])}"
            if (line[gender_column] == 'Masculino'):
                male.append(person_name)
            else:
                female.append(person_name)
    return male, female


catechized_av = get_availability(catechized_file, catechized_name, catechized_schedule)
catechists_av = get_availability(catechists_file, catechists_name, catechists_schedule)
monitors_av = get_availability(monitors_file, monitors_name, monitors_schedule)

male_catechists, female_catechists = get_gender(catechists_file, catechists_gender, catechists_name)
# female_catechists = ['Isabel Lea-Plaza', 'Sofia Calvimontes', 'Jesu Vidal', 'Florencia Soto', 'Maria Ignacia Valdes', 'Alicia Ibanez', 'Catalina Ramirez', 'Camila Kellemen', 'Maria Gracia Barros Rosemary', 'Miriam Lopez']
# male_catechists = ['Tomas Munoz Fenner', 'Juan de Dios Alamos', 'Juan Pablo Claude', 'Andres Lagos', 'Ignacio Barros', 'Ignacio Parodi', 'Thomas Quiroga']

print(f"Standarized:")
print(f"\tCatechized: {len(catechized_av)}")
print(f"\tCatechists: {len(catechists_av)}")
print(f"\tMonitors: {len(monitors_av)}\n")
# print(f"monitores: {monitors_av}\n")
# print(f"catequistas: {catechists_av}\n")
# print(f"confirmandos: {catechized_av}\n")

'''
Expected return:
dict(person_name: dict(campus: [modules availables]) )
'''
