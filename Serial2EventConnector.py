import time
import datetime
from datetime import datetime as dt
from dataclasses import dataclass
from SerialClient import SerialClient, Message


class EventHandler:
    def on_door_opened(self, msg: Message):
        pass
    
    def on_door_closed(self, msg: Message):
        pass

    def on_now_button_pressed(self, msg: Message):
        pass
    
    def on_wait_button_pressed(self, msg: Message):
        pass
    
    def on_sensor_update(self, msg: Message):
        pass


@dataclass
class Serial2EventConnector:
    prev_msg: Message = None
    prev_post: dt = None
    prev_door_event: dt = None
    local_door_is_open: bool = False
    handler: EventHandler = None

    def start(self):
        self.ser = SerialClient()
        self.ser.connect()
        
        for msg in self.ser.read():
            self.on_message(msg)
            self.prev_msg = msg
    
    def on_message(self, msg):
        prev_msg = self.prev_msg
        prev_post = self.prev_post
        prev_door_event = self.prev_door_event
        local_door_is_open = self.local_door_is_open
        handler = self.handler

        if prev_msg is None:
            return
        
        interval = datetime.timedelta(milliseconds=500)
        if prev_door_event is None or msg.timestamp - prev_door_event > interval:
            if not local_door_is_open and msg.door_is_open:
                self.prev_door_event = msg.timestamp
                
                if handler is not None:
                    handler.on_door_opened(msg)

            if local_door_is_open and not msg.door_is_open:
                self.prev_door_event = msg.timestamp
                
                if handler is not None:
                    handler.on_door_closed(msg)

            self.local_door_is_open = msg.door_is_open

        if prev_msg.now_button_pressed and not msg.now_button_pressed:
            if handler is not None:
                handler.on_now_button_pressed(msg)

        if prev_msg.wait_button_pressed and not msg.wait_button_pressed:
            if handler is not None:
                handler.on_wait_button_pressed(msg)

        interval = datetime.timedelta(seconds=5)
        if prev_post is None or msg.timestamp - prev_post > interval:
            if handler is not None:
                handler.on_sensor_update(msg)

            self.prev_post = msg.timestamp

if __name__ == '__main__':
    connector = Serial2EventConnector()
    connector.start()

