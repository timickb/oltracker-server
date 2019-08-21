import requests
import json
import yaml
import logging
import os.path
from database import Database

class MessagingService():
    def __init__(self):
        self.URL = "https://fcm.googleapis.com/fcm/send"
        self.KEY = ""
        try:
            with open('keys.json', 'r') as f:
                data = json.load(f)
                self.KEY = data['fcm']
        except:
            raise
        
        self.matches = None
        with open(os.path.dirname(__file__) + '../matches.yml', 'r') as file:
            try:
                self.matches = yaml.load(file)
            except:
                raise
        
        self.db = Database()
    
    def send_event_notifications(self, subjects, url):
        tokens = []
        for subject in subjects:
            try:
                subject = self.matches['subjects-reversed'][subject]
            except:
                subject = '-1'
            current_tokens = self.db.get_user_token_by_subject(subject)
            tokens += current_tokens
        tokens = set(tokens)
        for token in tokens:
            self.send_notification(token, url)
    
    def send_notification(self, user_token, data):
        payload = {
            'to': user_token,
            'notification': {
                'body': data,
                'title': 'New event'
            }
        }
        headers = {
            'Authorization': 'key='+self.KEY,
            'Content-Type': 'application/json'
        }
        res = requests.post(self.URL, json=payload, headers=headers)
        print("[Messaging Service] Notification was sent to '{}' with code {}".format(user_token, res.status_code))