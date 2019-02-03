# OlympiadNotifier REST API source code
# Copyright by Timur Batrutdinov

from flask import Flask
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

@app.route('/')
def info():
    db.Query("SELECT * FROM users")
    return 'OlympiadNotifier Server'

app.run(port=config['port'], debug=True)