# OlympiadNotifier REST API source code
# Copyright by Timur Batrutdinov

from flask import Flask
from parser import Parser
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

app = Flask(__name__)
parser = Parser()

@app.route('/')
def info():
    db.Query("SELECT * FROM users")
    print(parser.getOlympiadsList())
    return 'OlympiadNotifier Server'

app.run(port=config['port'], debug=True)