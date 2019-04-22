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
        loadUi('interfaceV4.ui',self)
        self.setWindowTitle('Tez Deneme UI')
        self.artirBtn.clicked.connect(self.artirBtn_clicked)
        self.azaltBtn.clicked.connect(self.azaltBtn_clicked)
        self.count = 0
        self.led1StatusLink = "http://192.168.137.103/5" #defining default link
        self.led1OnLink = "http://192.168.137.103/5/on"
        self.led1OffLink = "http://192.168.137.103/5/off"
        self.led2StatusLink = "http://192.168.137.103/4" #defining default link
        self.led2OnLink = "http://192.168.137.103/4/on"
        self.led2OffLink = "http://192.168.137.103/4/off"
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
    
    def led1StatusShow(self): #printing status of led_1
        led1Stat = "Oda Isigi Kapali"
        if self.led1Status():
            led1Stat = "Oda Isigi Acik"
        self.led1statusLbl.setText(led1Stat)

    def led2Status(self):
        try:
            led2Status = requests.post(self.led2StatusLink)
            return led2Status.json()
        except:
            return 0

    def led2StatusShow(self): #printing status of led_2
        led2Stat = "Gece Lambasi Kapali"
        if self.led2Status():
            led2Stat = "Gece Lambasi Acik"
        self.led2statusLbl.setText(led2Stat)

    def curtainStatus(self):
        try:
            curtainStatus = requests.post(self.curtainStatusLink)
            print(curtainStatus.json())
            return curtainStatus.json()
        except:
            return 0

    def curtainStatusShow(self): #printing status of curtain in room
        curtainStat = "Perde Kapali"
        if self.curtainStatus():
            curtainStat = "Perde Acik"
        self.curtainStatusLbl.setText(curtainStat)


class Book(QMainWindow):
    def __init__(self):
        super(Book,self).__init__()
        loadUi('books.ui',self)
        self.setWindowTitle('Kitap Okuma UI')
        self.bookCount = 0
        self.pageNo = 0
        self.sayfaArtirBtn.clicked.connect(self.sayfaArtirBtn_clicked)
        self.sayfaAzaltBtn.clicked.connect(self.sayfaAzaltBtn_clicked)
        

    @pyqtSlot()
    def sayfaArtirBtn_clicked(self):
        self.bookCount=self.bookCount + 1
        if int(self.bookCount) > len(self.bookListWidget):
            self.bookCount = 1
        self.pageLbl.setText(''+str(int(self.bookCount)))
        self.bookListWidget.setCurrentRow(self.bookCount-1)
        print(str(self.bookListWidget.currentItem().text())) #print selected item on listview

    def sayfaAzaltBtn_clicked(self):
        self.bookCount=self.bookCount - 1
        if int(self.bookCount) <= 0:
            self.bookCount = len(self.bookListWidget)
        self.pageLbl.setText(''+str(int(self.bookCount)))
        self.bookListWidget.setCurrentRow(self.bookCount-1)
        print(str(self.bookListWidget.currentItem().text()))

bookPage=0
if __name__ == "__main__":
    #try:
    app = QtWidgets.QApplication(sys.argv)
    widget=denemem()
    widget.show()
    book = Book()
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
                    bookPage=1
                    book.show()
        
    #except:
        #buttonReply = QMessageBox.information(None, 'HATA', "Ä°nternet BaÄŸlantÄ±nÄ±zÄ± Kontrol Ediniz.")
