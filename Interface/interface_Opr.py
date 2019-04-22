import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import *
from television import Television
from book import Book

class MainUI(QDialog):
    def __init__(self):
        super(MainUI,self).__init__()
        loadUi('interface.ui',self)
        self.setWindowTitle('MAIN PAGE UI')
        self.setWindowIcon(QtGui.QIcon('Photos/eye.jpg'))
        self.setStyleSheet("QDialog{background-image: url(Photos/room.jpg); background-repeat: no-repeat; background-position: center;}")
        self.pixmap2 = QPixmap('Photos/bulb.png')
        self.pixmap1 = QPixmap('Photos/bulbOpen.png')
        self.label_2.setPixmap(self.pixmap2)
        self.pixmap3 = QPixmap('Photos/nightLamp_close.png')
        self.pixmap4 = QPixmap('Photos/nightLamp_open.png')
        self.nightBulbLbl.setPixmap(self.pixmap3)
        self.curtainOpenPix = QPixmap('Photos/curtainOpen.png')
        self.curtainClosedPix = QPixmap('Photos/curtainClosed.png')
        self.curtainLbl.setPixmap(self.curtainClosedPix)
        self.tvOpenPix = QPixmap('Photos/uniteOpen.png')
        self.tvClosedPix = QPixmap('Photos/uniteClosed.png')
        self.tvLbl.setPixmap(self.tvClosedPix)
        self.artirBtn.clicked.connect(self.artirBtn_clicked)
        self.azaltBtn.clicked.connect(self.azaltBtn_clicked)
        self.count = 0
        self.led1StatusLink = "http://192.168.137.103/14" #defining default link
        self.led1OnLink = "http://192.168.137.103/14/on"
        self.led1OffLink = "http://192.168.137.103/14/off"
        self.led2StatusLink = "http://192.168.137.103/12" #defining default link
        self.led2OnLink = "http://192.168.137.103/12/on"
        self.led2OffLink = "http://192.168.137.103/12/off"
        self.curtainStatusLink = "http://192.168.137.103/2"
        self.curtainOnLink = "http://192.168.137.103/2/on"
        self.curtainOffLink = "http://192.168.137.103/2/off"
        self.led1StatusShow()
        self.led2StatusShow()
        self.curtainStatusShow()
            
        
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


bookPage = 0
tv_frame = 0 #state of tv frame
if __name__ == "__main__":
    #try:
    app = QtWidgets.QApplication(sys.argv)
    widget=MainUI()
    widget.show()
    book = Book()
    tv = Television()
    #sys.exit(app.exec_())
    
    while True:
        command = input("Enter a command: ")
        if bookPage:
            if command == "-":
                book.sayfaAzaltBtn_clicked()
            elif command == "+":
                book.sayfaArtirBtn_clicked()
            elif command == "c":
                if book.bookCount == 1:
                    QtWidgets.QTabWidget.setCurrentIndex(book.tabWidget, 1) # sonraki sayfaya git
                elif book.bookCount == 2:
                    QtWidgets.QTabWidget.setCurrentIndex(book.tabWidget, 0) # onceki sayfaya git
                elif book.bookCount == 3:
                    book.close()
                    bookPage = 0
        elif tv_frame:
            if command == "-":
                tv.tvAzaltBtn_clicked()
            elif command == "+":
                tv.tvArtirBtn_clicked()
            elif command == "c":
                if tv.tvCount == 1:
                    requests.post(tv.tvCh1Link)
                    tv.tvStatusLbl.setText("1. Kanal Acik")
                    widget.tvLbl.setPixmap(widget.tvOpenPix)
                elif tv.tvCount == 2:
                    requests.post(tv.tvCh2Link)
                    tv.tvStatusLbl.setText("2. Kanal Acik")
                    widget.tvLbl.setPixmap(widget.tvOpenPix)
                elif tv.tvCount == 3:
                    requests.post(tv.tvCloseLink)
                    tv.tvStatusLbl.setText("TV Kapali")
                    widget.tvLbl.setPixmap(widget.tvClosedPix)
                elif tv.tvCount == 4:
                    tv.close()
                    tv_frame = 0
        else:
            if command == "-":
                widget.azaltBtn_clicked()
            elif command == "+":
                widget.artirBtn_clicked()
            elif command == "c":
                if(widget.count == 1):
                    requests.post(widget.led1OnLink)
                    widget.led1StatusShow()
                elif(widget.count == 2):
                    requests.post(widget.led1OffLink)
                    widget.led1StatusShow()
                elif(widget.count == 3):
                    requests.post(widget.led2OnLink)
                    widget.led2StatusShow()
                elif(widget.count == 4):
                    requests.post(widget.led2OffLink)
                    widget.led2StatusShow()
                elif(widget.count == 5):
                    requests.post(widget.curtainOnLink)
                    widget.curtainStatusShow()
                elif(widget.count == 6):
                    requests.post(widget.curtainOffLink)
                    widget.curtainStatusShow()
                elif(widget.count == 7):
                    tv_frame = 1
                    tv.show()
                elif(widget.count == 8):
                    bookPage=1
                    book.show()
        
    #except:
        #buttonReply = QMessageBox.information(None, 'HATA', "Ä°nternet BaÄŸlantÄ±nÄ±zÄ± Kontrol Ediniz.")
