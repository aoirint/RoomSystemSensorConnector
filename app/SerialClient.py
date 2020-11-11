import time
import json
import traceback
import serial
from datetime import datetime as dt
import pytz
from dataclasses import dataclass

@dataclass
class Message:
    type: str
    light: int
    temperature: int
    temperature_celsius: float
    now_button_pressed: bool
    wait_button_pressed: bool
    door_is_open: bool
    timestamp: dt

class SerialClient:
    def connect(self):  
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=0.1,
        )
        print('connecting')

        while True:
            ret = ser.read()
            print('.', flush=True, end='')
            if ret != 0:
                break

        print()
        print('connected')
        
        self.ser = ser

    def read(self):
        while True:
            line = self.ser.readline()
            timestamp = dt.now(pytz.utc)
          
            try:
                line = line.decode('ascii').strip()
            except UnicodeDecodeError:
                print(traceback.format_exc())
                continue

            try:
                serial_data = json.loads(line)
            except json.JSONDecodeError:
                print(traceback.format_exc())
                continue

            msg = Message(
                type=serial_data.get('type'),
                light=serial_data.get('light'),
                temperature=serial_data.get('temperature'),
                temperature_celsius=serial_data.get('temperatureCelsius'),
                now_button_pressed=serial_data.get('nowButtonPressed'),
                wait_button_pressed=serial_data.get('waitButtonPressed'),
                door_is_open=serial_data.get('doorIsOpen'),
                timestamp=timestamp,
            )

            yield msg


if __name__ == '__main__':
    ser = SerialClient()
    ser.connect()

    for msg in ser.read():
        print(msg)

