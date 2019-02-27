# OlympiadNotifier REST API source code

from flask import Flask, jsonify, request
from parsers import MoeObr
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

app = Flask(__name__)

parser = MoeObr()

@app.route('/')
def info():
    return 'OlympiadNotifier Server'

@app.route('/get')
def get():
    class_ = request.args.get('class')
    subject = request.args.get('subject')
    date = request.args.get('date')

    if class_== None: class_ = -1
    if subject == None: subject = "all"
    if date == None: date = -1
    out = parser.getList(class_=class_, subject=subject, date=date)
    if out == 0: 
        answer = jsonify([])
    else:
        answer = jsonify(out)
    print(answer)
    return answer

app.run(port=config['port'])