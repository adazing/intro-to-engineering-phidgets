# phidget libraries
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *

# other libraries
import time
import random

# text to speech library, docs: https://pyttsx3.readthedocs.io/en/latest/index.html
import pyttsx4

# set up engine for text to speech
engine = pyttsx4.init()

# starting number of colors
list_length = 4

# set up ports for Phidget
greenButton = DigitalInput()
redButton = DigitalInput()

redLED = DigitalOutput()
greenLED = DigitalOutput()

redButton.setHubPort(0)
redButton.setIsHubPortDevice(True)
redLED.setHubPort(1)
redLED.setIsHubPortDevice(True)
greenButton.setHubPort(5)
greenButton.setIsHubPortDevice(True)
greenLED.setHubPort(4)
greenLED.setIsHubPortDevice(True)

greenButton.openWaitForAttachment(1000)
redButton.openWaitForAttachment(1000)
redLED.openWaitForAttachment(1000)
greenLED.openWaitForAttachment(1000)

# blinks colors given list of LEDs to blink
def blink_colors(list_of_colors):
    for LED in list_of_colors:
        LED.setState(True)
        time.sleep(0.5)
        LED.setState(False)
        time.sleep(0.5)

red_was_on_high=False
green_was_on_high=False

while(True):
    # print onto screen
    print("Press red button to start!")
    # say text aloud (pauses the code until it finishes)
    engine.say("Press red button to start!")
    engine.runAndWait()
    # wait until red button is pressed
    while(redButton.getState()==False):
        continue
    while(True):
        # list comprehension: makes list of random LEDs that are the same length of list_length
        list_of_colors = [random.choice([redLED, greenLED]) for x in range(list_length)]
        # prints the level onto screen
        print("Level",list_length,"Playing colors...")
        # say text aloud (pauses the code until it finishes)
        engine.say("Level "+str(list_length)+" Playing colors.")
        engine.runAndWait()
        # delay until actually start playing LEDs
        time.sleep(1)
      
        # blink the LEDs
        blink_colors(list_of_colors)
      
        list_of_player_colors = []
        # continue until player pushes number of buttons equivalent to list_length
        while True:
            # append colors to list_of_player_colors
            if(greenButton.getState()==False and green_was_on_high):
                list_of_player_colors.append(greenLED)
                green_was_on_high=False
            elif greenButton.getState():
                green_was_on_high=True
            if(redButton.getState()==False and red_was_on_high):
                list_of_player_colors.append(redLED)
                red_was_on_high=False
            elif redButton.getState():
                red_was_on_high=True
            # check if won
            if (list_of_player_colors==list_of_colors):
                print("Success")
                engine.say("Success. Press red button to continue to next level!")
                engine.runAndWait()
                print("Press red button to continue to next level!")
                while(redButton.getState()==False):
                    continue
            # check if lost
            elif any([list_of_player_colors[led]!=list_of_colors[led] for led in range(len(list_of_player_colors))]):
                print("Failure")
                print("Restarting...")
                engine.say("Failure...Restarting!")
                engine.runAndWait()
                break
            list_length+=1
