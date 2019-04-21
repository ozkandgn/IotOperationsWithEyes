class Blinking():
    def __init__(self):
        self.__right_count = 0
        self.__left_count = 0
    
    def set_blink(self, val): # coming open eye = 1, close eye = 2
        print("val = ",val)
        self.__right_count = self.calculate(self.__right_count,val[0])
        self.__left_count = self.calculate(self.__left_count,val[1])
        print(self.__right_count)
        print(self.__left_count)
        
    def calculate(self,count,val):
        val -= 0.6            # after open eye = -0.6, close eye = 0.4
        count += val
        if count < -3:
            count = -3
        elif count > 3:
            count = 3
        if count <= 0:
            print("Open")
        else:
            print("Close")
        return count