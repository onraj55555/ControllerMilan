import serial
import pyautogui
import vgamepad as vg
import math

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

def xyToCircle(x: int, y: int) -> tuple:
    r = math.sqrt(x*x + y*y)
    r = min(r, 512)
    theta = math.atan2(y, x)
    xN = min(r * math.cos(theta) + 512, 1023)
    yN = min(r * math.sin(theta) + 512, 1023)
    return (xN, yN)

def convertInput(arduinoInput: str) -> tuple:
    data = str(ser.readline())
    data = data.replace('\'', '').replace('b', '').replace('\\r\\n', '').split(':')
    x = int(data[0])
    y = int(data[1])
    x, y = xyToCircle(x, y)
    x = int(x / 1024.0 * 65535 - 32768)
    y = int(y / 1024.0 * 65535 - 32768)
    btn1 = int(data[2])
    btn2 = int(data[3])
    buttonsToPress = []
    buttonsToRelease = []
    if btn1 == 0:
        buttonsToPress.append(buttons[0])
    else:
        buttonsToRelease.append(buttons[0])
    if btn1 == 1:
        buttonsToPress.append(buttons[1])
    else:
        buttonsToRelease.append(buttons[1])
    return (x, y, buttonsToPress, buttonsToRelease)

while True:
    data = str(ser.readline())
    #data = data.replace('\'', '').replace('b', '').replace('\\r\\n', '').split(':')
    #x = y = 0
    try:
        print(data)
        x, y, buttonsToPress, buttonsToRelease = convertInput(data)
        
        gamepad.left_joystick(x_value=y, y_value=x)
        
        for button in buttonsToPress:
            gamepad.press_button(button = button)
        
        for button in buttonsToRelease:
            gamepad.release_button(button = button)

        gamepad.update()
    except:
        pass
