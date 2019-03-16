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

def ban_ip(ip):
    f = open('banned_ips.json', 'r', encoding='utf-8')
    data = json.load(f)
    data.append(ip)
    f.close()
    f = open('banned_ips.json', 'w', encoding='utf-8')
    json.dump(data, f)
    f.close()
    print('Banned IP: ' + str(ip))

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

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    url = request.url
    try:
        f = open('banned_ips.json', 'r', encoding='utf-8')
        banned_list = json.load(f)
    except:
        banned_list = []

    if request.remote_addr in banned_list:
        return 'Your IP is banned'
    if 'php' in request.url:
        ban_ip(request.remote_addr)
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


debug = config['debug']
if debug == 'True' or debug == 'true' or debug == 'on' or debug > 0:
    debug = True
else:
    debug = False

app.run(host=config['host'], port=config['port'], debug=debug)