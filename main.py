import time
import datetime
from datetime import datetime as dt
from dataclasses import dataclass
from SerialClient import SerialClient, Message

@dataclass
class Connector:
    prev_msg: Message = None
    prev_post: dt = None
    prev_door_event: dt = None
    local_door_is_open: bool = False

    def __init__(self):
        self.ser = SerialClient()
    
    def start(self):
        self.ser.connect()
        
        for msg in self.ser.read():
            self.on_message(msg)
            self.prev_msg = msg
    
    def on_message(self, msg):
        prev_msg = self.prev_msg
        prev_post = self.prev_post
        prev_door_event = self.prev_door_event
        local_door_is_open = self.local_door_is_open

        if prev_msg is None:
            return
        
        interval = datetime.timedelta(milliseconds=500)
        if prev_door_event is None or msg.timestamp - prev_door_event > interval:
            if not local_door_is_open and msg.door_is_open:
                self.prev_door_event = msg.timestamp
                print('door opened!')

            if local_door_is_open and not msg.door_is_open:
                self.prev_door_event = msg.timestamp
                print('door closed!')

            self.local_door_is_open = msg.door_is_open

        if prev_msg.now_button_pressed and not msg.now_button_pressed:
            print('now button pressed!')
        
        if prev_msg.wait_button_pressed and not msg.wait_button_pressed:
            print('wait button pressed!')

        interval = datetime.timedelta(seconds=5)
        if prev_post is None or msg.timestamp - prev_post > interval:
            print(msg)
            self.prev_post = msg.timestamp

if __name__ == '__main__':
    connector = Connector()
    connector.start()

