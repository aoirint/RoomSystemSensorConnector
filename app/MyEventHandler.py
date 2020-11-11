import os
import json
import subprocess
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

SENSOR_MESSAGE_ENABLED = os.environ.get('SENSOR_MESSAGE_ENABLED', '0') == '1'
SENSOR_MESSAGE_TITLE = os.environ.get('SENSOR_MESSAGE_TITLE')

DOOR_MESSAGE_TITLE = os.environ.get('DOOR_MESSAGE_TITLE')
DOOR_OPENED_MESSAGE_TEXT = os.environ.get('DOOR_OPENED_MESSAGE_TEXT', 'door opened')
DOOR_CLOSED_MESSAGE_TEXT = os.environ.get('DOOR_CLOSED_MESSAGE_TEXT', 'door closed')

BUTTON_MESSAGE_TITLE = os.environ.get('BUTTON_MESSAGE_TITLE')
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
    
    session.post(incoming_url, data=body, headers={
        'Content-Type': 'application/json',
    })

def play_sound(path):
    subprocess.run([ 'play', path ])

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
        
        post_teams(TEAMS_BUTTON_URL, NOW_BUTTON_MESSAGE_TEXT, title=BUTTON_MESSAGE_TITLE)
        
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
        
        post_teams(TEAMS_BUTTON_URL, WAIT_BUTTON_MESSAGE_TEXT, title=BUTTON_MESSAGE_TITLE)
        
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

        if SENSOR_MESSAGE_ENABLED:
            text = ''
            text += f'Brightness: {msg.light}\n\n'
            text += f'Temperature: {msg.temperature}\n\n'
            text += f'Timestamp: {msg.timestamp.isoformat()}\n\n'

            post_teams(TEAMS_NOTIFICATION_URL, text, title=SENSOR_MESSAGE_TITLE)

