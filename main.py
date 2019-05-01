# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, logging
from database import Database
from datetime import datetime
import yaml
import os
import json
import logging

# --start logger--
filename = 'logs/serverLog' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')
logging.info("Starting Olympiad Tracker API")

# --import configs--

KEY = ""
try:
    with open('keys.json', 'r') as file:
        data = json.load(file)
        KEY = data['api']
except:
    logging.critical('File with API keys was not found, shutdown server')
    exit(0)
logging.info("API key was loaded")

config = None
with open('config.yml', 'r', encoding='utf-8') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        logging.critical(ex)
        logging.critical('Can not load config.yml, shutdown server')
        exit(0)

matches = None
with open('matches.yml', 'r', encoding='utf-8') as file:
    try:
        matches = yaml.load(file)
    except yaml.YAMLError as ex:
        logging.critical(ex)
        logging.critical('Can not load matches.yml, shutdown server')
        exit(0)
logging.info("Config was loaded")

# --initializing database--
try:
    db = Database()
except:
    logging.critical('Can not initialize database, shutdown server')
    exit(0)

logging.info("Connected to database")

# --important functions--

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
    
    db = open('database_next.json', 'r', encoding='utf-8')
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
    
    db = open('database_current.json', 'r', encoding='utf-8')
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


# --HTTP server--
logging.info("Starting HTTP server...")

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # just protection
    if 'php' in request.url:
        return 'what are you doing little hacker?'
    return 'Not found'

@app.errorhandler(404)
def page_not_found(e):
    return 'Not found'
    
@app.route('/')
def info():
    html = open('index.html', 'r', encoding='utf-8').read()
    return html

@app.route('/getNext')
def get():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    stage = request.args.get('stage')
    return jsonify(find_data_next(schclass, subject, stage))

@app.route('/getCurrent')
def getCurrent():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    stage = request.args.get('stage')
    return jsonify(find_data_current(schclass, subject, stage))

@app.route('/updateUser', methods=['POST'])
def updateUser():
    api_key = request.body['key']
    if api_key != KEY:
        return 'Invalid key'

    user_token = request.body['token']
    subject = request.body['subject']
    flag = request.body['flag']

    db.update_data(user_token, subject, flag)

    return 'ok'

# --server startup--

debug = config['debug']
if debug == 'True' or debug == 'true' or debug == 'on' or debug > 0:
    debug = True
else:
    debug = False

logging.info("HTTP Server started")
app.run(host=config['host'], port=config['port'], debug=debug)