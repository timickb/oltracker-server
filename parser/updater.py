from datetime import datetime
from engine import OlympiadaRu
import json
import yaml
import logging
import os
import sys

if __name__ == "__main__":
    update_now = False
    update_hour = 3
    last_update_day = None
    parser = None
    matches = None

    try:
        if sys.argv[1] == "-u" or sys.argv[1] == "--update":
            update_now = True
    except:
        pass
    try:
        if sys.argv[2] == "-h" or sys.argv[2] == "--hour":
            update_hour = int(sys.argv[3])
    except:
        pass

    # logger start
    if not os.path.exists("logs"):
        os.mkdir('logs')
    filename = 'logs/log' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')

    logging.info("Starting Updater")

    with open('matches.yml', 'r', encoding='utf-8') as file:
        try:
            matches = yaml.load(file, Loader=yaml.SafeLoader)
        except:
            logging.critical("Can not open matches.yml, shutdown updater")
            exit(101)
    try:
        parser = OlympiadaRu(matches)
    except:
        logging.critical("Can not start parser, shutdown updater")
        exit(1)
    fetched = False
    while(True):
        if ((datetime.now().hour == update_hour) and (last_update_day != datetime.now().day)) or (update_now and not fetched):
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




