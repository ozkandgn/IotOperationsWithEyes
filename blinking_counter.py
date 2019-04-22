class Blinking():
    def __init__(self):
        self.__right_count = -3
        self.__left_count = -3
        self.__back_right_count = 0
        self.__back_left_count = 0
    
    def set_blink(self, val): # coming open eye = 1, close eye = 2
        #print("val = ",val)
        self.__right_count = self.calculate(self.__right_count,val[0])
        self.__left_count = self.calculate(self.__left_count,val[1])
        print(self.__right_count)
        print(self.__left_count)
        if self.__right_count > -1 and self.__left_count > -1:
            print("Both Close")
            return 'c'
        elif self.__right_count > 0.5 and self.__left_count < -2 and \
             self.__back_right_count <= self.__right_count:
                print("Right Close")
                return '+'
        elif self.__left_count > 0.5 and self.__right_count < -2 and \
             self.__back_left_count <= self.__left_count:
            print("Left Close")
            return '-'
        if self.__right_count <= -1 and self.__left_count <= -1:
            print("Both Open")
            return 'o'
        elif self.__right_count <= 0 and self.__left_count > 2:
            print("Right Open")
            return 'r'
        elif self.__left_count <= 0 and self.__right_count > 2:
            print("Left Open")
            return 'l'
            
        self.__back_left_count = self.__left_count
        self.__back_right_count = self.__right_count
        
    def calculate(self,count,val):
        val -= 0.6            # after open eye = -0.6, close eye = 0.4
        count += val
        if count < -3:
            count = -3
        elif count > 3:
            count = 3
        '''
        if count <= 0:
            print("Open")
        else:
            print("Close")
        '''
        return count