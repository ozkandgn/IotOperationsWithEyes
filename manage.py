from Interface.interface_v4 import Interface
from eye import Eye
from blinking_counter import Blinking
import time

class Manage():
    def __init__(self):
        #self.interface_frame = Interface().get_interface_frame
        self.blink = Blinking().set_blink
        self.eye_frame = Eye().get_eye_frame
        
    def get_all_frame(self):
        #command = input("Enter a command: ")
        #self.interface_frame(command)
        #time.sleep(0.5)
        #print(self.eye_frame())
        result = self.eye_frame()
        if result != None:
            print(result)
            self.blink(result)
        
if __name__ == "__main__":
    frames = Manage().get_all_frame
    while True:
        frames()