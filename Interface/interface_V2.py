import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import *

class denemem(QDialog):
    def __init__(self):
        super(denemem,self).__init__()
        loadUi('denememV2.ui',self)
        self.setWindowTitle('Tez Deneme UI')
        self.artirBtn.clicked.connect(self.artirBtn_clicked)
        self.azaltBtn.clicked.connect(self.azaltBtn_clicked)
        self.count = 0
        self.led1StatusLink = "http://192.168.137.103/5" #defining default link
        self.led1OnLink = "http://192.168.137.103/5/on"
        self.led1OffLink = "http://192.168.137.103/5/off"
        self.led1StatusShow()
        
    @pyqtSlot()
    def artirBtn_clicked(self):
        self.count=self.count + 1
        if int(self.count) > 4:
            self.count = 1
        self.label.setText(''+str(int(self.count)))
        self.listWidget.setCurrentRow(self.count-1)
        print(str(self.listWidget.currentItem().text())) #print selected item on listview

    def azaltBtn_clicked(self):
        self.count=self.count - 1
        if int(self.count) <= 0:
            self.count = 4
        self.label.setText(''+str(int(self.count)))
        self.listWidget.setCurrentRow(self.count-1)
        print(str(self.listWidget.currentItem().text()))

    def led1Status(self):
        led1status = requests.post(self.led1StatusLink)
        return led1status.json()
    
    def led1StatusShow(self): #printing status of led_1
        led1Stat = "led 1 kapalı"
        if self.led1Status():
            led1Stat = "led 1 açık"
        self.led1statusLbl.setText(led1Stat)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        widget=denemem()
        widget.show()
        #sys.exit(app.exec_())
        
        while True:
            command = input("Enter a command: ")
            if(command == "-"):
                widget.azaltBtn_clicked()
            elif(command == "+"):
                widget.artirBtn_clicked()
            elif(command == "c"):
                if(widget.count == 1):
                    try:
                        requests.post(widget.led1OnLink)
                        widget.led1StatusShow()
                    except:
                        print("hata")
                elif(widget.count == 2):
                    requests.post(widget.led1OffLink)
                    widget.led1StatusShow()
        
    except:
        buttonReply = QMessageBox.information(None, 'HATA', "İnternet Bağlantınızı Kontrol Ediniz.")

        
