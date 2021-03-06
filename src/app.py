#!./env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, logging, render_template
from database import Database
from datetime import datetime
import yaml
import os
import json
import logging
import config
import extractor

# logger start
if not os.path.exists("logs"):
        os.mkdir('logs')
filename = 'logs/serverLog' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')
logging.info("Starting Olympiad Tracker API")

# loading keys
KEY = ""
try:
    with open('keys.json', 'r') as file:
        data = json.load(file)
        KEY = data['api']
except:
    logging.critical('File with API keys was not found, shutdown server')
    exit(0)
logging.info("API key was loaded")


# init database
db = None
try:
    db = Database()
except:
    logging.critical('Can not initialize database, shutdown server')
    exit(0)

logging.info("Connected to database")

# --HTTP server--
logging.info("Starting HTTP server...")

app = Flask(__name__, static_url_path='/static')

@app.route('/updateUser', methods=['POST'])
def updateUser():
    data = request.get_json()
    logging.info("Received data: " + json.dumps(data))
    key = data['key']
    token = data['token']
    subject = data['subject']
    flag = data['flag']
    if key != KEY:
        logging.info("Key was invalid. Skip it.")
        return jsonify({'result': 'Invalid key'})

    if flag == 'true':
        flag = True
    else:
        flag = False
    
    db.update_data(token, subject, flag)
    logging.info("Table was updated.")
    
    return jsonify({'result': 'ok'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
    
@app.route('/')
def info():
    return render_template('index.html')

@app.route('/getNext')
def get():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    stage = request.args.get('stage')
    data = extractor.extract_data_next(schclass, subject, stage)
    return jsonify(data)

@app.route('/getCurrent')
def getCurrent():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    stage = request.args.get('stage')
    data = extractor.extract_data_current(schclass, subject, stage)
    return jsonify(data)

# server startup
logging.info("HTTP Server started")
app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)