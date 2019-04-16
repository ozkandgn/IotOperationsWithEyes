class Blinking():
    def __init__(self):
        self.__count = 0
    
    def set_blink(self, val): # coming open eye = 1, close eye = 2
        print("val = ",val)
        val -= 1.6            # after open eye = -0.6, close eye = 0.4
        if self.__count <= 3 and self.__count >= -3:
            self.__count += val
        if self.__count <= 0:
            return "Open"
        else:
            return "Close"