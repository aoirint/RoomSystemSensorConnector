
from SerialClient import Message
from Serial2EventConnector import Serial2EventConnector, EventHandler

class MyEventHandler(EventHandler):
    def on_door_opened(self, msg: Message):
        print('door opened')
        pass
    
    def on_door_closed(self, msg: Message):
        print('door closed')
        pass

    def on_now_button_pressed(self, msg: Message):
        print('now')
        pass
    
    def on_wait_button_pressed(self, msg: Message):
        print('wait')
        pass
 
    def on_sensor_update(self, msg: Message):
        print(msg)
        pass

if __name__ == '__main__':
    handler = MyEventHandler()
    connector = Serial2EventConnector(
        handler=handler,
    )

    connector.start()

