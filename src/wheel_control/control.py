#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)
# inspired by https://github.com/moozer/CameraBot/blob/master/src/deviceinfo.py

import pygame
import math
import os
import urllib
from urllib.request import urlopen
from http.cookiejar import CookieJar

# make sure pygame doesn't try to open an output window
MAX_STEERING_ANGLE = 250
os.environ["SDL_VIDEODRIVER"] = "dummy"

DEBUG = True
WHEEL = "Logitech G25 Racing Wheel USB"
gear_lever_positions = {
    -1: "reverse",
    0: "neutral",
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth"
}

status_buttons = {
    10: "parking_brake_status",
    1: "headlamp_status",
    3: "high_beam_status",
    2: "windshield_wiper_status"
}

gear_lever_position = 0
parking_brake_status = False
headlamp_status = False
high_beam_status = False
windshield_wiper_status = False
axis_mode = 1


def send_data(name, value):
    url = 'http://localhost:50000/_set_data'
    # print(name,value)
    post_data = urllib.urlencode([('name', name), ('value', value)])
    print(post_data)
    try:
        req = urlopen(url, post_data)
    except Exception as ex:
        print(ex)
        exit(-1)

def stop():
    send_data("ignition_status", "off")
    urlopen("http://localhost:50000/stop", "")

def old_main():
    pygame.init()

    try:
        res = urlopen("http://localhost:50000/")
    except Exception as e:
        print(e)
    except Exception as e:
        print(e)

    try:
        wheel = None
        for j in range(0, pygame.joystick.get_count()):
            print(pygame.joystick.Joystick(j).get_name())
            if pygame.joystick.Joystick(j).get_name() == WHEEL:
                wheel = pygame.joystick.Joystick(j)
                wheel.init()
                print("Found", wheel.get_name())

        if not wheel:
            print("No G27 steering wheel found")
            exit(-1)

        start()

        while True:
            for event in pygame.event.get(pygame.QUIT):
                exit(0)
            for event in pygame.event.get(pygame.JOYAXISMOTION):
                if DEBUG:
                    print("Motion on axis: ", event.axis)
                    print("event.value: ", event.value)
                    print("axis_mode", axis_mode)
                if event.axis == 0:
                    print("steering angle", event.value * MAX_STEERING_ANGLE)
                elif event.axis == 2 and axis_mode == 1:
                    print("accelerator", event.value * -100)
                elif event.axis == 3:
                    print("brake", event.value * -100)
            """
            for event in pygame.event.get(pygame.JOYBUTTONUP):
                if DEBUG:
                    print("Released button is", event.button)
                if (event.button >= 12 and event.button <= 17) or event.button == 22:
                    gear = 0
                    print("gear_lever_position", gear_lever_positions[gear])
            for event in pygame.event.get(pygame.JOYBUTTONDOWN):
                if DEBUG:
                    print("Pressed button is", event.button)
                if event.button == 0:
                    print("pressed button 0 - bye...")
                    stop()
                    exit(0)
                elif event.button == 11:
                    print("ignition_status", "start")
                elif event.button >= 12 and event.button <= 17:
                    gear = event.button - 11
                    print("gear_lever_position", gear_lever_positions[gear])
                elif event.button == 22:
                    gear = -1
                    print("gear_lever_position", gear_lever_positions[gear])
                elif event.button in status_buttons:
                    vars()[status_buttons[event.button]] = not vars()[status_buttons[event.button]]
                    print(status_buttons[event.button], str(vars()[status_buttons[event.button]]).lower())
            """
    except Exception as e:
        print(e)

pygame.init()
wheel = None
for j in range(0, pygame.joystick.get_count()):
    print(pygame.joystick.Joystick(j).get_name())
    if pygame.joystick.Joystick(j).get_name() == WHEEL:
        wheel = pygame.joystick.Joystick(j)
        wheel.init()
        print("Found", wheel.get_name())

if not wheel:
    print("No G27 steering wheel found")
    exit(-1)

steering_angle = 0
accelerator = -100
brake = -100
def get_key_values():
    global steering_angle, accelerator, brake
    try:
        for event in pygame.event.get(pygame.QUIT):
            exit(0)
        for event in pygame.event.get(pygame.JOYAXISMOTION):
            if DEBUG:
                print("Motion on axis: ", event.axis)
                print("event.value: ", event.value)
                print("axis_mode", axis_mode)
            if event.axis == 0:
                print("steering angle", event.value * MAX_STEERING_ANGLE)
                steering_angle = event.value * MAX_STEERING_ANGLE
            elif event.axis == 2 and axis_mode == 1:
                print("accelerator", event.value * -100)
                accelerator = event.value * -100
            elif event.axis == 3:
                print("brake", event.value * -100)
                brake = event.value * -100
    except Exception as e:
        print(e)
    return [steering_angle, accelerator, brake]