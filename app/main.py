import os
import json
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from SerialClient import Message
from Serial2EventConnector import Serial2EventConnector, EventHandler

FIREBASE_SECRET_PATH = os.environ['FIREBASE_SECRET_PATH']
FIREBASE_DATABASE_URL = os.environ['FIREBASE_DATABASE_URL']

TEAMS_NOTIFICATION_URL = os.environ.get('TEAMS_NOTIFICATION_URL')
TEAMS_BUTTON_URL = os.environ.get('TEAMS_BUTTON_URL')

DOOR_MESSAGE_TITLE = os.environ.get('DOOR_MESSAGE_TITLE', 'DoorState Notification')
DOOR_OPENED_MESSAGE_TEXT = os.environ.get('DOOR_OPENED_MESSAGE_TEXT', 'door opened')
DOOR_CLOSED_MESSAGE_TEXT = os.environ.get('DOOR_CLOSED_MESSAGE_TEXT', 'door closed')

NOW_BUTTON_MESSAGE_TEXT = os.environ.get('NOW_BUTTON_MESSAGE_TEXT', 'now button pressed')
WAIT_BUTTON_MESSAGE_TEXT = os.environ.get('WAIT_BUTTON_MESSAGE_TEXT', 'wait button pressed')



cred = credentials.Certificate(FIREBASE_SECRET_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DATABASE_URL,
})

sensor_ref = db.reference('sensor')
now_button_ref = sensor_ref.child('now_button')
wait_button_ref = sensor_ref.child('wait_button')
door_ref = sensor_ref.child('door')
environment_ref = sensor_ref.child('environment')

session = requests.Session()
session.timeout = 3.0

def post_teams(incoming_url, text, title=None):
    if not incoming_url:
        return

    data = {}
    if title:
        data['title'] = title
    data['text'] = text

    body = json.dumps(data)
    
    session.post(TEAMS_INCOMING_WEBHOOK_URL, data=body, headers={
        'Content-Type': 'application/json',
    })


class MyEventHandler(EventHandler):
    def on_door_opened(self, msg: Message):
        print('door open')
        door_ref.update({
            'isOpen': True,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
        
        post_teams(TEAMS_NOTIFICATION_URL, DOOR_OPENED_MESSAGE_TEXT, title=DOOR_MESSAGE_TITLE)
    
    def on_door_closed(self, msg: Message):
        print('door closed')
        door_ref.update({
            'isOpen': False,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
        
        post_teams(TEAMS_NOTIFICATION_URL, DOOR_CLOSED_MESSAGE_TEXT, title=DOOR_MESSAGE_TITLE)

    def on_now_button_pressed(self, msg: Message):
        print('now button pressed')
        
        now_button_ref.update({
            'isPressed': True,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
    
    def on_now_button_released(self, msg: Message):
        print('now button released')
        
        now_button_ref.update({
            'isPressed': False,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
        
        post_teams(TEAMS_BUTTON_URL, NOW_BUTTON_MESSAGE_TEXT)
        
        play_sound('/sounds/now_button.mp3')
    
    def on_wait_button_pressed(self, msg: Message):
        print('wait button pressed')
        
        wait_button_ref.update({
            'isPressed': True,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })

    def on_wait_button_released(self, msg: Message):
        print('wait button released')
        
        wait_button_ref.update({
            'isPressed': False,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
        
        post_teams(TEAMS_BUTTON_URL, WAIT_BUTTON_MESSAGE_TEXT)
        
        play_sound('/sounds/wait_button.mp3')
 
    def on_sensor_update(self, msg: Message):
        # TODO: light on, off detection
        pass

    def on_sensor_post(self, msg: Message):
        print(msg)
        environment_ref.push({
            'light': msg.light,
            'temperature': msg.temperature,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })

if __name__ == '__main__':
    handler = MyEventHandler()
    connector = Serial2EventConnector(
        handler=handler,
    )

    connector.start()

