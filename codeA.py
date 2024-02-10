import serial
import pyautogui
import time
import binascii

pyautogui.PAUSE = 0

prevKey = "p"

allKeys = ["z", "q", "s", "d"]
decoder = {
    "z": "z",
    "q": "q",
    "s": "s",
    "d": "d",
    "b": "zq",
    "a": "zd",
    "c": "qs",
    "e": "sd",
}
keys = {"z": False, "q": False, "s": False, "d": False}

# Define the serial port and baud rate.
# Make sure the 'COM#' and 'BAUD_RATE' values are correct for your system.
ser = serial.Serial("COM4", 9600)


def allUp():
    for i in allKeys:
        pyautogui.keyUp(i)


def keyController(keys):
    for i in keys:
        pyautogui.keyDown(i)


while True:
    # Read data from the serial monitor.
    data = ser.readline().decode()#.strip()  # .decode().strip()
    # data = ser.read(1)
    #print(data)
    print(ord(data[0]))
    # Print the binary representation of the data.
    # binary_data = bin(int.from_bytes(data, byteorder="big"))[2:].zfill(8)
    if "p" == data:
        allUp()
    else:  # data != prevKey:
        allUp()
        #keyController(decoder[data])
        prevKey = data
