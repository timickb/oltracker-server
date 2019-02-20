# OlympiadNotifier REST API source code

from flask import Flask, jsonify
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
    out = parser.getList()
    return jsonify(out)

app.run(port=config['port'])