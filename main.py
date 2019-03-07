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
    with open('database.json', 'r', encoding='utf-8') as db:
        data = json.load(db)
        return data

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