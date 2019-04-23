from Interface.interface_Opr import Interface
from eye import Eye
from blinking_counter import Blinking
import time

class Manage():
    def __init__(self):
        self.interface_frame = Interface().get_interface_frame
        self.blink = Blinking().set_blink
        self.eye_frame = Eye().get_eye_frame
        self.both_clicked = False
        self.right_click_count = 0
        self.left_click_count = 0
        self.interface_frame("")
        
    def get_all_frame(self):
        result_eye = self.eye_frame()
        if result_eye != None:
            #for both eye
            result = self.blink(result_eye)
            if result == 'c' and self.both_clicked == False:
                self.both_clicked = True
                
            elif result == 'c' and self.both_clicked == True:
                result = 'n'
                
            elif result == 'o':
                self.both_clicked = False
                result = 'n'
            
            #for right and left eye, used counter
            #right close
            elif result == '+' and self.right_click_count <= 0:
                self.right_click_count = 5
                
            elif result == '+' and self.right_click_count > 0:
                self.right_click_count -= 1
                result = 'n'
                
            #right open
            elif result == 'r' and self.right_click_count > 0:
                self.right_click_count -= 1
                result = 'n'
                
            ####    
            #left close
            elif result == '-' and self.left_click_count <= 0:
                self.left_click_count = 5
                
            elif result == '-' and self.left_click_count > 0:
                self.left_click_count -= 1
                result = 'n'
                
            #left open
            elif result == 'l' and self.left_click_count > 0:
                self.left_click_count -= 1
                result = 'n'
                
            if result != 'n' and result != 'r' and result != 'l' and result != 'o':
                print("result ",result)
            self.interface_frame(result)

if __name__ == "__main__":
    frames = Manage().get_all_frame
    while True:
        frames()
