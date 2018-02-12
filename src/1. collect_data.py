import numpy as np
from grabscreen import grab_screen
#import cv2
import time
#from getkeys import key_check
import os
from wheel_control import control


steering_angle = 0      #between -MAX_STEERING_ANGLE and MAX_STEERING_ANGLE
accelerator = -100      #between -100 (no accleration) and 100 (max accleration)
brake = -100            #between -100 (no brake) and 100 (max brake)

starting_value = 1
window_title_substring = 'Game'
while True:
    file_name = 'C:/Users/Nicolas/IdeaProjects/ml_f1/data/training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        break

def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    gesamt = 0
    anzahl = 0
    while(True):

        if not paused:
            screen = grab_screen(window_title=window_title_substring,
                                 region=(0,30,1680,987),
                                 scale=0.25)

            last_time = time.time()
            output = control.get_key_values()
            print("output", output)
            training_data.append([screen,output])
            duration = time.time()-last_time
            print('loop took {} seconds'.format(duration))
            try:
                print('fps:', 1/duration)
            except ZeroDivisionError as e:
                pass
            #time.sleep(0.001)
            #additional_sleep = 0.001 - duration
            #if additional_sleep > 0.00000:
            #    time.sleep(additional_sleep)
            gesamt += duration
            anzahl+=1
            print("avg ", gesamt/anzahl)
            last_time = time.time()


            if len(training_data) % 100 == 0:
                print(len(training_data))

            if len(training_data) == 500:
                np.save(file_name,training_data)
                print('SAVED')
                training_data = []
                starting_value += 1
                file_name = 'C:/Users/Nicolas/IdeaProjects/ml_f1/data/training_data-{}.npy'.format(starting_value)

        # TODO: implement pause
        """
        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
        """

main(file_name, starting_value)
