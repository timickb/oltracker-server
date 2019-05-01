from datetime import datetime
from parsers import OlympiadaRu
import json
import yaml
import logging

# --start logger--
filename = 'logs/updaterLog' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')
logging.info("Starting Updater")

r = input('Flag: ')

config = None
with open('config.yml', 'r') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

last_update_day = None
try:
    parser = OlympiadaRu()
except:
    logging.critical("Can not start parser, shutdown updater")
fetched = False
while(True):
    if ((datetime.now().hour == config['updateHour']) and (last_update_day != datetime.now().day)) or r == 'Now' and not fetched:
        fetched = True
        logging.info('Fetching data...')
        last_update_day = datetime.now().day

        data_next = parser.get_next_events()
        with open('database_next.json', 'w', encoding='utf-8') as db:
            json.dump(data_next, db, ensure_ascii=False)

        data_current = parser.get_current_events()
        with open('database_current.json', 'w', encoding='utf-8') as db:
            json.dump(data_current, db, ensure_ascii=False)
            
        logging.info('Information updated.')