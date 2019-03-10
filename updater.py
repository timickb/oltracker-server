from datetime import datetime
from parsers import MoeObr, OlympiadaRu
import json
import yaml

config = None
with open('config.yml', 'r') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

last_update_day = None
parser = MoeObr()
parser1 = OlympiadaRu()

while(True):
    if (datetime.now().hour == config['updateHour']) and (last_update_day != datetime.now().day):
        print('Fetching data...')
        last_update_day = datetime.now().day
        #data_next = parser.get_list()
        data_current = parser1.get_current_events()
        #with open('database_next.json', 'w', encoding='utf-8') as db:
        #    json.dump(data_next, db, ensure_ascii=False)
        with open('database_current.json', 'w', encoding='utf-8') as db:
            json.dump(data_current, db, ensure_ascii=False)
            
        print('Information updated.')