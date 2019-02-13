# OlympiadNotifier REST API source code

from flask import Flask
from parsers import MoeObr
import yaml
import os

#----------------------------------------------------------

config = None
with open('config.yml', 'r') as file:
    try:
        config = yaml.load(file)
    except yaml.YAMLError as ex:
        print(ex)
        exit()

#----------------------------------------------------------

#app = Flask(__name__)

parser = MoeObr()
parser.getList()

#@app.route('/')
#def info():
#    return 'OlympiadNotifier Server'
#
#app.run(port=config['port'])