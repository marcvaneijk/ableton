from __future__ import with_statement

import sys
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *

IS_MOMENTARY=True

class record_quantization(ControlSurface):          # create a class element 
    
    def __init__(self, c_instance):                #initialize the AAAA class as a ControleSurface
        ControlSurface.__init__(self,c_instance)   #import the components of a ControlSurface
        with self.component_guard():
            self.__c_instance = c_instance

            self.labels = ["None", "1/4", "1/8", "1/8T", "1/8 + 1/8T", "1/16", "1/16T", "1/16 + 1/16T", "1/32"]

            #blah=str(dir(self.song().midi_recording_quantization.numerator))
            #blah=str(self.song().midi_recording_quantization)
            #current = self.song().midi_recording_quantization
            #self.song().midi_recording_quantization = 4
            #self.log_message(blah)
            #self.log_message(current)

            #self.log_message(str(dir(self.song().midi_recording_quantization.numerator)))
            #self.log_message(str(self.song().midi_recording_quantization.numerator))

            self.ButtonMoveDown=ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, 0, 60) # 0,60 = channel 1, C3 # identifies Pad1 as a ButtonElement. IS_MOMENTARY is true if the button send a message on being released
            self.ButtonMoveDown.add_value_listener(self.rq_movedown,identify_sender=False) #adda value listener that will lauch the method self.helloworld when Pad1 is pressed
            self.ButtonMoveUp=ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, 0, 62) # 0,60 = channel 1, C3 # identifies Pad1 as a ButtonElement. IS_MOMENTARY is true if the button send a message on being released
            self.ButtonMoveUp.add_value_listener(self.rq_moveup,identify_sender=False) #adda value listener that will lauch the method self.helloworld when Pad1 is pressed
            #self.helloworld()                     #call the helloworld function during the initialisation of your script

    def rq_movedown(self,status):  #create the movedown fuction (with the self argument, live uderstand that this function belong to the ControleSurface object, instanciated from the record_quantization class)
        if status > 0:  ## Ignore the release of the button (NoteOff)
            current = self.song().midi_recording_quantization.numerator
            self.log_message('1 movedown | current = ' + str(current)) 
            if current == 0: # Quantize is already set to 0 (meaning it is turned off)
                self.show_message('Record Quantization is already set to ' + self.labels[current])
                self.log_message('1A movedown | if | donothing = ' + str(current) + ' ,label = ' + self.labels[current]) 
            else: 
                new = current - 1
                self.song().midi_recording_quantization = new
                self.show_message('Record Quantization set to '+ self.labels[new])
                self.log_message('1B movedown | else | new = ' + str(new) + ' ,label = ' + self.labels[new]) 

    def rq_moveup(self,status):  #create moveup fuction (with the self argument, live uderstand that this function belong to the ControleSurface object, instanciated from the AAAA class)
        if status > 0:  ## Ignore the release of the button (NoteOff)
            current = self.song().midi_recording_quantization.numerator
            self.log_message('2 moveup | current = ' + str(current)) 
            if current == 8: # Quantize is already set to 8 (meaning it is set to 1/32 and can't move up anymore)
                self.show_message('Record Quantization is already set to ' + self.labels[current])
                self.log_message('2A moveup | if | donothing = ' + str(current) + ' ,label = ' + self.labels[current]) 
            else: 
                new = current + 1
                self.song().midi_recording_quantization = new
                self.show_message('Record Quantization set to ' + self.labels[new])
                self.log_message('2B moveup | else | new = ' + str(new) + ' ,label = ' + self.labels[new]) 
