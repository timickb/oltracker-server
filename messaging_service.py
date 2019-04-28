import requests
import json
import yaml

class MessagingService():
    def __init__(self):
        self.URL = "https://fcm.googleapis.com/fcm/send"
        self.KEY = ""
        try:
            with open('keys.json', 'r') as f:
                data = json.load(f)
                self.KEY = data['fcm']
        except:
            print('Error: file with API keys was not found.')
            raise
        
        self.config = None
        with open('config.yml', 'r') as file:
            try:
                self.config = yaml.load(file)
            except:
                print('Error: config file was not found')
                raise
    
    def send_notification(self, user_token, data):
        payload = {
            'to': user_token,
            'notification': {
                'body': data,
                'title': self.config['notification_title']
            }
        }
        headers = {
            'Authorization': 'key='+self.KEY,
            'Content-Type': 'application/json'
        }

        res = requests.post(self.URL, json=payload, headers=headers)
        print("[Messaging Service] Notification was sent to '{}' with code {}".format(user_token, res.status_code))




