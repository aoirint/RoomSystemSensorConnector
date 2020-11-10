import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from SerialClient import Message
from Serial2EventConnector import Serial2EventConnector, EventHandler


FIREBASE_SECRET_PATH = os.environ['FIREBASE_SECRET_PATH']
FIREBASE_DATABASE_URL = os.environ['FIREBASE_DATABASE_URL']

cred = credentials.Certificate(FIREBASE_SECRET_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DATABASE_URL,
})

sensor_ref = db.reference('sensor')
now_button_ref = sensor_ref.child('now_button')
wait_button_ref = sensor_ref.child('wait_button')
door_ref = sensor_ref.child('door')
environment_ref = sensor_ref.child('environment')


class MyEventHandler(EventHandler):
    def on_door_opened(self, msg: Message):
        print('door opened')
        door_ref.update({
            'isOpen': True,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })
    
    def on_door_closed(self, msg: Message):
        print('door closed')
        door_ref.update({
            'isOpen': False,
            'timestamp': {
                '.sv': 'timestamp',
            },
        })

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
 
    def on_sensor_update(self, msg: Message):
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

