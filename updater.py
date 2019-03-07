from datetime import datetime
from parsers import MoeObr
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

while(True):
    if (datetime.now().hour == config['updateHour']) and (last_update_day != datetime.now().day):
        print('Fetching data...')
        last_update_day = datetime.now().day
        data = parser.get_list()
        with open('database.json', 'w', encoding='utf-8') as db:
            json.dump(data, db, ensure_ascii=False)
            print('Information updated.')