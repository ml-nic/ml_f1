#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)
# inspired by https://github.com/moozer/CameraBot/blob/master/src/deviceinfo.py

import pygame
import os
import time

# make sure pygame doesn't try to open an output window
MAX_STEERING_ANGLE = 250
os.environ["SDL_VIDEODRIVER"] = "dummy"

DEBUG = True
WHEEL = "Logitech G25 Racing Wheel USB"
axis_mode = 1


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

steering_angle = 0  # -1 (left) to 1 (right)
accelerator = 1     # 1 no acceleration to -1 full acceleration
brake = 1           # 1 no brake to -1 full brake
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
                print("steering angle", event.value)
                steering_angle = event.value
            elif event.axis == 2 and axis_mode == 1:
                print("accelerator", event.value)
                accelerator = event.value
            elif event.axis == 3:
                print("brake", event.value)
                brake = event.value
    except Exception as e:
        print(e)
    return [steering_angle, accelerator, brake]

def accelerate():
    pass

if __name__ == "__main__":
    while(True):
        print(get_key_values())
        time.sleep(1)
