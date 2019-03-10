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

def find_data_next(schclass, subject, oltype):
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
    
    db = open('database_next.json', 'r', encoding='utf-8')
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


# --HTTP server--

app = Flask(__name__)

@app.route('/')
def info():
    html = open('index.html', 'r', encoding='utf-8').read()
    return html

@app.route('/getNext')
def get():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    oltype = request.args.get('type')
    return jsonify(find_data_next(schclass, subject, oltype))

@app.route('/getCurrent')
def getCurrent():
    schclass = request.args.get('class')
    subject = request.args.get('subject')
    oltype = request.args.get('type')
    return jsonify(find_data_current(schclass, subject, oltype))


debug = config['debug']
if debug == 'True' or debug == 'true' or debug == 'on' or debug > 0:
    debug = True
else:
    debug = False

app.run(host=config['host'], port=config['port'], debug=debug)