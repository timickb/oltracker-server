from flask import Flask, jsonify, request, logging
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

def find_data_current(schclass, subject, oltype):
    result = []
    try:
        schclass = int(schclass)
    except:
        schclass = -1
    try:
        subject = matches['subjects'][subject]
    except:
        subject = -1
    
    if oltype not in matches['types-olru']:
        oltype = -1
    
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
        if (isClass) and (subject in item['subjects'] or subject == -1):
            result.append(item)

    return result

def find_data(class_, subject, date):
    result = []
    if class_ == -1: class_ = None
    if subject == -1: subject = None
    if date == -1: date = None

    try:
        subject = matches['subjects-mo'][subject]
    except:
        subject = None
    
    try:
        date = matches['months'][date]
    except:
        date = None

    db = open('database_next.json', 'r', encoding='utf-8')
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

@app.route('/getCurrent')
def getCurrent():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    oltype = request.args.get('type')
    print(schclass, subject, oltype)
    return jsonify(find_data_current(schclass, subject, oltype))

app.run(host=config['host'], port=config['port'], debug=True)