import serial
import pyautogui
import vgamepad as vg

gamepad = vg.VX360Gamepad()

pyautogui.PAUSE = 0

ser = serial.Serial("COM14", 19200)

buttonMapping = {'up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    'down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    'left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    'right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    'back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    'l3': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    'r3': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    'l2': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'r2': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    'guid': vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
    'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y}

buttons = []

with open('buttons.txt') as f:
    for line in f:
        button = line.strip().split('=')[-1]
        buttons.append(buttonMapping[button])

while True:
    data = str(ser.readline())
    data = data.replace('\'', '').replace('b', '').replace('\\r\\n', '').split(':')
    x = y = 0
    try:
        print(data)
        x = int((int(data[0]) / 1024.0) * 65535 - 32768)
        y = int((int(data[1]) / 1024.0) * 65535 - 32768)
        btn1 = int(data[2])
        btn2 = int(data[3])
        gamepad.left_joystick(x_value=y, y_value=x)
        if btn1 == 0:
            gamepad.press_button(button=buttons[0])
        else:
            gamepad.release_button(button=buttons[0])
        if btn2 == 0:
            gamepad.press_button(button=buttons[1])
        else:
            gamepad.release_button(button=buttons[1])
        gamepad.update()
    except:
        pass
