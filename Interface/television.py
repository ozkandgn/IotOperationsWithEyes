import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import *


class Television(QMainWindow):
    def __init__(self):
        super(Television, self).__init__()
        loadUi('Interface/television.ui',self)
        self.setWindowTitle('Television Control')
        self.setStyleSheet("QMainWindow{background-image: url(Interface/Photos/tvBackground.png); background-repeat: no-repeat; background-position: center;}")
        self.tvCount = 0
        self.setFixedSize(918,616)
        self.tvArtirBtn.clicked.connect(self.tvArtirBtn_clicked)
        self.tvAzaltBtn.clicked.connect(self.tvAzaltBtn_clicked)
        IP="http://192.168.137.22"
        self.tvCh1Link = IP+"/3/kanal1"
        self.tvCh2Link = IP+"/3/kanal2"
        self.tvCloseLink =IP+"/3/kapat"
        self.statusLink = IP+"/3"

    @pyqtSlot()
    def tvArtirBtn_clicked(self):
        self.tvCount = self.tvCount + 1
        if int(self.tvCount) > len(self.tvListWidget):
            self.tvCount = 1
        self.label.setText(''+str(int(self.tvCount)))
        self.tvListWidget.setCurrentRow(self.tvCount-1)
        print(str(self.tvListWidget.currentItem().text()))

    def tvAzaltBtn_clicked(self):
        self.tvCount = self.tvCount - 1
        if int(self.tvCount) <= 0:
            self.tvCount = len(self.tvListWidget)
        self.label.setText(''+str(int(self.tvCount)))
        self.tvListWidget.setCurrentRow(self.tvCount-1)
        print(str(self.tvListWidget.currentItem().text()))

    def tvStatus(self):
        try:
            tv_status = requests.post(self.statusLink)
            return tv_status.json()
        except:
            return 0
        
    def tvOnaylaBtn_clicked(self):
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
    
    def chStatusShow(self): #showing channel status
        if self.tvStatus() == 1:
            chStat = "Kanal 1 Acik"
        elif self.tvStatus() == 2:
            chStat = "Kanal 2 Acik"
        else:
            chStat = "TV Kapali"
        self.tvStatusLbl.setText(chStat)
        
