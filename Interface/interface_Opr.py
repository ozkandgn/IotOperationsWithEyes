import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import *
from .television import Television
from .book import Book

class MainUI(QDialog):
    def __init__(self):
        super(MainUI,self).__init__()
        loadUi('Interface/interface.ui',self)
        self.setWindowTitle('MAIN PAGE UI')
        self.setWindowIcon(QtGui.QIcon('Photos/eye.jpg'))
        self.setStyleSheet("QDialog{background-image: url(Interface/Photos/room3.jpg); background-repeat: no-repeat; background-position: center;}")
        self.countPix = QPixmap('Interface/Photos/countFrame2.png')
        self.frameLbl.setPixmap(self.countPix)
        self.pixmap2 = QPixmap('Interface/Photos/chandelier.png')
        self.pixmap1 = QPixmap('Interface/Photos/chandelieropen.png')
        self.label_2.setPixmap(self.pixmap2)
        self.pixmap3 = QPixmap('Interface/Photos/nightLamp_close.png')
        self.pixmap4 = QPixmap('Interface/Photos/nightLamp_open.png')
        self.nightBulbLbl.setPixmap(self.pixmap3)
        self.curtainOpenPix = QPixmap('Interface/Photos/curtainOpen.png')
        self.curtainClosedPix = QPixmap('Interface/Photos/curtainClosed.png')
        self.curtainLbl.setPixmap(self.curtainClosedPix)
        self.tvOpenPix = QPixmap('Interface/Photos/uniteOpen.png')
        self.tvClosedPix = QPixmap('Interface/Photos/uniteClosed.png')
        self.tvLbl.setPixmap(self.tvClosedPix)
        self.artirBtn.clicked.connect(self.artirBtn_clicked)
        self.azaltBtn.clicked.connect(self.azaltBtn_clicked)
        self.onaylaBtn.clicked.connect(self.onaylaBtn_clicked)
        self.count = 0
        IP="http://192.168.137.101"
        self.led1StatusLink = IP+"/14" #defining default link
        self.led1OnLink = IP+"/14/on"
        self.led1OffLink = IP+"/14/off"
        self.led2StatusLink = IP+"/0" #defining default link of night lamp
        self.led2OnLink = IP+"/0/on"
        self.led2OffLink = IP+"/0/off"
        self.curtainStatusLink = IP+"/2"
        self.curtainOnLink = IP+"/2/on"
        self.curtainOffLink = IP+"/2/off"
        self.led1StatusShow()
        self.led2StatusShow()
        self.curtainStatusShow()
        self.book = Book()
        self.tv = Television()
            
        
    @pyqtSlot()
    def artirBtn_clicked(self):
        self.count=self.count + 1
        if int(self.count) > len(self.listWidget):
            self.count = 1
        self.label.setText(''+str(int(self.count)))
        self.listWidget.setCurrentRow(self.count-1)
        print(str(self.listWidget.currentItem().text())) #print selected item on listview

    def azaltBtn_clicked(self):
        self.count=self.count - 1
        if int(self.count) <= 0:
            self.count = len(self.listWidget)
        self.label.setText(''+str(int(self.count)))
        self.listWidget.setCurrentRow(self.count-1)
        print(str(self.listWidget.currentItem().text()))

    def onaylaBtn_clicked(self):
        if(self.count == 1):
            requests.post(self.led1OnLink)
            self.led1StatusShow()
        elif(self.count == 2):
            requests.post(self.led1OffLink)
            self.led1StatusShow()
        elif(self.count == 3):
            requests.post(self.led2OnLink)
            self.led2StatusShow()
        elif(self.count == 4):
            requests.post(self.led2OffLink)
            self.led2StatusShow()
        elif(self.count == 5):
            requests.post(self.curtainOnLink)
            self.curtainStatusShow()
        elif(self.count == 6):
            requests.post(self.curtainOffLink)
            self.curtainStatusShow()
        elif (self.count == 7):
            tv_frame = 1
            self.tv.show()
        elif(self.count == 8):
            bookPage = 1
            self.book.show()

    def led1Status(self):
        try:
            led1status = requests.post(self.led1StatusLink)
            return led1status.json()
        except:
            return 0
    
    def led1StatusShow(self): #showing status of led_1
        self.label_2.setPixmap(self.pixmap2)
        if self.led1Status():
            self.label_2.setPixmap(self.pixmap1)

    def led2Status(self):
        try:
            led2Status = requests.post(self.led2StatusLink)
            return led2Status.json()
        except:
            return 0

    def led2StatusShow(self): #printing status of led_2
        self.nightBulbLbl.setPixmap(self.pixmap3)
        if self.led2Status():
            self.nightBulbLbl.setPixmap(self.pixmap4)

    def curtainStatus(self):
        try:
            curtainStatus = requests.post(self.curtainStatusLink)
            return curtainStatus.json()
        except:
            return 0

    def curtainStatusShow(self): #printing status of curtain in room
        self.curtainLbl.setPixmap(self.curtainClosedPix)
        if self.curtainStatus():
            self.curtainLbl.setPixmap(self.curtainOpenPix)

class Interface():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.bookPage = 0
        self.tv_frame = 0
        self.widget = MainUI()
        self.widget.show()
        self.book = Book()
        self.tv = Television()
        #sys.exit(self.app.exec_())
        
    def get_interface_frame(self,command):
        if self.bookPage:
            if command == "-":
                self.book.sayfaAzaltBtn_clicked()
            elif command == "+":
                self.book.sayfaArtirBtn_clicked()
            elif command == "c":
                if self.book.bookCount == 1:
                    QtWidgets.QTabWidget.setCurrentIndex(self.book.tabWidget, 1) # sonraki sayfaya git
                elif self.book.bookCount == 2:
                    QtWidgets.QTabWidget.setCurrentIndex(self.book.tabWidget, 0) # onceki sayfaya git
                elif self.book.bookCount == 3:
                    self.book.close()
                    self.bookPage = 0
        
        elif self.tv_frame:
            if command == "-":
                self.tv.tvAzaltBtn_clicked()
            elif command == "+":
                self.tv.tvArtirBtn_clicked()
            elif command == "c":
                if self.tv.tvCount == 1:
                    requests.post(self.tv.tvCh1Link)
                    self.tv.tvStatusLbl.setText("1. Kanal Acik")
                    self.widget.tvLbl.setPixmap(self.widget.tvOpenPix)
                elif self.tv.tvCount == 2:
                    requests.post(self.tv.tvCh2Link)
                    self.tv.tvStatusLbl.setText("2. Kanal Acik")
                    self.widget.tvLbl.setPixmap(self.widget.tvOpenPix)
                elif self.tv.tvCount == 3:
                    requests.post(self.tv.tvCloseLink)
                    self.tv.tvStatusLbl.setText("TV Kapali")
                    self.widget.tvLbl.setPixmap(self.widget.tvClosedPix)
                elif self.tv.tvCount == 4:
                    self.tv.close()
                    self.tv_frame = 0

        else:
            if command == "-":
                self.widget.azaltBtn_clicked()
            elif command == "+":
                self.widget.artirBtn_clicked()
            elif command == "c":
                if(self.widget.count == 1):
                    try:
                        requests.post(self.widget.led1OnLink)
                    except:
                        pass
                    self.widget.led1StatusShow()
                elif(self.widget.count == 2):
                    requests.post(self.widget.led1OffLink)
                    self.widget.led1StatusShow()
                elif(self.widget.count == 3):
                    requests.post(self.widget.led2OnLink)
                    self.widget.led2StatusShow()
                elif(self.widget.count == 4):
                    requests.post(self.widget.led2OffLink)
                    self.widget.led2StatusShow()
                elif(self.widget.count == 5):
                    requests.post(self.widget.curtainOnLink)
                    self.widget.curtainStatusShow()
                elif(self.widget.count == 6):
                    requests.post(self.widget.curtainOffLink)
                    self.widget.curtainStatusShow()
                elif (self.widget.count == 7):
                    self.tv_frame = 1
                    self.tv.show()
                elif(self.widget.count == 8):
                    self.bookPage = 1
                    self.book.show()
