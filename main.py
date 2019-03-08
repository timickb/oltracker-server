from flask import Flask, jsonify, request
from threading import Thread
import yaml
import os
import json

# --import configs--

config = None
with open('config.yml', 'r', encoding='utf-8') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

matches = None
with open('matches.yml', 'r', encoding='utf-8') as file:
    try:
        matches = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

# --important functions--

def find_data(class_, subject, date):
    result = []
    if class_ == -1: class_ = None
    if subject == -1: subject = None
    if date == -1: date = None

    try:
        subject = matches['subjects'][subject]
    except:
        subject = None
    
    try:
        date = matches['months'][date]
    except:
        date = None

    db = open('database.json', 'r', encoding='utf-8')
    data = json.load(db)
    for item in data:
        if (class_ in item['classes'] or class_ == None) and (subject in item['subjects'] or subject == None) and (date == item['date_start'] or date == None):
            result.append(item)
    return result

# --HTTP server--

app = Flask(__name__)

@app.route('/')
def info():
    html = open('index.html', 'r', encoding='utf-8').read()
    return html

@app.route('/get')
def get():
    class_ = request.args.get('class')
    subject = request.args.get('subject')
    date = request.args.get('date')
    return jsonify(find_data(class_, subject, date))

app.run(host=config['host'], port=config['port'])