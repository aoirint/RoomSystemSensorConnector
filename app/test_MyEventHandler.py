from MyEventHandler import MyEventHandler

if __name__ == '__main__':
    handler = MyEventHandler()

    handler.on_door_opened(msg=None)
    handler.on_door_closed(msg=None)

    handler.on_now_button_pressed(msg=None)
    handler.on_now_button_released(msg=None)

    handler.on_wait_button_pressed(msg=None)
    handler.on_wait_button_released(msg=None)

