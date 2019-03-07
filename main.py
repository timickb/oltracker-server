from flask import Flask, jsonify, request
from threading import Thread
import yaml
import os
import json

#----------------------------------------------------------

config = None
with open('config.yml', 'r') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

#----------------------------------------------------------

def find_data(class_, subject, date):
<<<<<<< HEAD
    result = []
    db = open('database.json', 'r', encoding='utf-8')
    data = json.load(db)
    for item in data:
        if (class_ in item['classes'] or class_ == None) and (string_in_list(subject, item['subjects']) or subject == None) and (date == item['date_start'] or date == None):
            result.append(item)
    return result

def string_in_list(string, list0):
    for item in list0:
        if item == string:
            return True
    return False
=======
    with open('database.json', 'r', encoding='utf-8') as db:
        data = json.load(db)
        return data
>>>>>>> 55457e7269407e438bf5a10f3adaa7710b824528

#----------------------------------------------------------

app = Flask(__name__)

@app.route('/')
def info():
    return 'API for Olympiad Tracker'

@app.route('/get')
def get():
    class_ = request.args.get('class')
    subject = request.args.get('subject')
    date = request.args.get('date')

    answer = jsonify(find_data(class_, subject, date))
    return answer

#----------------------------------------------------------

app.run(port=config['port'])