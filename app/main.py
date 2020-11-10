from Serial2EventConnector import Serial2EventConnector
from MyEventHandler import MyEventHandler

if __name__ == '__main__':
    handler = MyEventHandler()
    connector = Serial2EventConnector(
        handler=handler,
    )

    connector.start()

