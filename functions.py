import json
import yaml

matches = None
with open('parser/matches.yml', 'r', encoding='utf-8') as file:
    try:
        matches = yaml.load(file, Loader=yaml.SafeLoader)
    except yaml.YAMLError as ex:
        logging.critical(ex)
        logging.critical('Can not load matches.yml, shutdown server')
        exit(0)

def find_data_next(schclass, subject, stage):
    result = []
    try:
        schclass = int(schclass)
    except:
        schclass = -1
    try:
        subject = matches['subjects'][subject]
    except:
        subject = -1
    
    if stage != 'final' and stage != 'selection':
        stage = -1
    
    if (schclass not in range(5, 12)) and schclass != -1:
        return result
    
    db = open('parser/database_next.json', 'r', encoding='utf-8')
    data = json.load(db)

    for item in data:
        isClass = False
        try:
            isClass = schclass in item['classes'] or schclass == -1
        except:
            isClass = False
        isStage = True
        try:
            isStage = stage == item['stage'] or stage == -1
        except:
            isStage = True
        if (isClass) and (subject in item['subjects'] or subject == -1) and (isStage):
            result.append(item)

    return result

def find_data_current(schclass, subject, stage):
    result = []
    try:
        schclass = int(schclass)
    except:
        schclass = -1
    try:
        subject = matches['subjects'][subject]
    except:
        subject = -1
    
    if stage != 'final' and stage != 'selection':
        stage = -1

    if (schclass not in range(5, 12)) and schclass != -1:
        return result
    
    db = open('parser/database_current.json', 'r', encoding='utf-8')
    data = json.load(db)

    for item in data:
        isClass = False
        try:
            isClass = schclass in item['classes'] or schclass == -1
        except:
            isClass = False
        if (isClass) and (subject in item['subjects'] or subject == -1) and (stage == item['stage'] or stage == -1):
            result.append(item)

    return result