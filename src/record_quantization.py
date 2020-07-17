from __future__ import with_statement

import sys
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *

IS_MOMENTARY=True

class record_quantization(ControlSurface): # create a class element 
    
    def __init__(self, c_instance):                #initialize the record_quantization class as a ControleSurface
        ControlSurface.__init__(self,c_instance)   #import the components of a ControlSurface
        with self.component_guard():
            self.__c_instance = c_instance

            self.labels = ["None", "1/4", "1/8", "1/8T", "1/8 + 1/8T", "1/16", "1/16T", "1/16 + 1/16T", "1/32"]

            self.ButtonMoveDown=ButtonElement(not IS_MOMENTARY, MIDI_CC_TYPE, 0, 60) # 0,60 = channel 1, cc 60 # identifies ButtonMoveDown as a ButtonElement. IS_MOMENTARY is true if the button send a message on being released
            self.ButtonMoveDown.add_value_listener(self.rq_movedown,identify_sender=False) #adda value listener that will lauch the method rq_moveup when the button is pressed
            self.ButtonMoveUp=ButtonElement(not IS_MOMENTARY, MIDI_CC_TYPE, 0, 61) # 0,61 = channel 1, cc 61 # identifies ButtonMoveUp as a ButtonElement. IS_MOMENTARY is true if the button send a message on being released
            self.ButtonMoveUp.add_value_listener(self.rq_moveup,identify_sender=False) # value listener that will lauch the method rq_moveup when the button is pressed


    def rq_movedown(self,status):  #create the movedown fuction (with the self argument, live uderstand that this function belong to the ControleSurface object, created from the record_quantization class)
        if status == 127:  ## Only execute is the CC state message value is 127
            current = self.song().midi_recording_quantization.numerator
            if current == 0: # Quantize is already set to 0 (meaning it is turned off)
                self.show_message('Record Quantization is already set to ' + self.labels[current])
            else: 
                new = current - 1
                self.song().midi_recording_quantization = new
                self.show_message('Record Quantization set to '+ self.labels[new])

    def rq_moveup(self,status):  #create moveup fuction 
        if status == 127:
            current = self.song().midi_recording_quantization.numerator
            if current == 8: # Quantize is already set to 8 (meaning it is set to 1/32 and can't move up anymore)
                self.show_message('Record Quantization is already set to ' + self.labels[current])
            else: 
                new = current + 1
                self.song().midi_recording_quantization = new
                self.show_message('Record Quantization set to ' + self.labels[new])
