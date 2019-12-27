#!/usr/bin/env python3
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

import os
import sys
import time
import logging

from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MediumMotor

from agt import AlexaGadget

# set logger to display on both EV3 Brick and console
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
logger = logging.getLogger(__name__)

def red_adjust_value(input):
    #28/24 because 28 tooth and 24 tooth gears
    #Adjust this if you use different gears
    return input * (28/24)

class MindstormsGadget(AlexaGadget):
    """
    An Mindstorms gadget that will react to the Alexa wake word.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        self.leds = Leds()
        self.sound = Sound()

        self.blueMotor = MediumMotor(OUTPUT_A)
        self.redMotor = MediumMotor(OUTPUT_B)

    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        logger.info("Connected to Alexa")
        gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
        self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(360))
        self.blueMotor.on_for_degrees(speed=flagSpeed, degrees=360)

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        logger.info("Disconnected from Alexa")
        gadget.sound.play_song((('E5', 'e'), ('D4', 'e'), ('C4', 'q')))

    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        """
        Listens for the state changes and reacts
        :param directive: contains a payload with the updated state information from Alexa
        """
        color_list = ['BLACK', 'AMBER', 'YELLOW', 'GREEN']
        for state in directive.payload.states:
            if state.name == 'wakeword':
                if state.value == 'active':
                    print("Wake word active", file=sys.stderr)
                    self.sound.play_song((('A3', 'e'), ('C5', 'e')))
                    self.blueMotor.on_for_degrees(speed=flagSpeed, degrees=180)

                elif state.value == 'cleared':
                    print("Wake word cleared", file=sys.stderr)
                    self.sound.play_song((('C5', 'e'), ('A3', 'e')))
                    self.blueMotor.on_for_degrees(speed=flagSpeed, degrees=180)

            elif state.name == 'alarms':
                if state.value == 'active':
                    print("Alarm active", file=sys.stderr)
                    self.sound.play_song((('B3', 'e'), ('D5', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(90))
                elif state.value == 'cleared':
                    print("Alarm cleared", file=sys.stderr)
                    self.sound.play_song((('B5', 'e'), ('D3', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(270))
            
            elif state.name == 'timers':
                if state.value == 'active':
                    print("Timer active", file=sys.stderr)
                    self.sound.play_song((('C3', 'e'), ('E5', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(180))
                elif state.value == 'cleared':
                    print("Timer cleared", file=sys.stderr)
                    self.sound.play_song((('E5', 'e'), ('C3', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(180))

            elif state.name == 'reminders':
                if state.value == 'active':
                    print("Reminder active", file=sys.stderr)
                    self.sound.play_song((('D3', 'e'), ('F5', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(270))
                elif state.value == 'cleared':
                    print("Reminder cleared", file=sys.stderr)
                    self.sound.play_song((('F5', 'e'), ('D3', 'e')))
                    self.redMotor.on_for_degrees(speed=flagSpeed, degrees=red_adjust_value(90))

            elif state.name == 'timeinfo':
                print(state.value)
                logger.info(state.value)

            self.redMotor.off()
            self.blueMotor.off()

if __name__ == '__main__':

    gadget = MindstormsGadget()
    flagSpeed = 50

    # Set LCD font and turn off blinking LEDs
    os.system('setfont Lat7-Terminus12x6')
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")

    # Startup sequence
    gadget.sound.play_song((('C4', 'e3'), ('E5', 'e3')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('E5', 'e3'), ('C4', 'e3')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
