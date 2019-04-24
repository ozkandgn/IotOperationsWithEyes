import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import *

class Book(QMainWindow):
    def __init__(self):
        super(Book,self).__init__()
        loadUi('Interface/books.ui',self)
        self.setWindowTitle('Kitap Okuma UI')
        self.setStyleSheet("QMainWindow{background-image: url(Interface/Photos/bookBackground.png); background-repeat: no-repeat; background-position: center;}")
        self.bookCount = 0
        self.pageNo = 0
        self.sayfaArtirBtn.clicked.connect(self.sayfaArtirBtn_clicked)
        self.sayfaAzaltBtn.clicked.connect(self.sayfaAzaltBtn_clicked)
        self.kitapOnaylaBtn.clicked.connect(self.kitapOnaylaBtn_clicked)

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

    def kitapOnaylaBtn_clicked(self):
        if self.bookCount == 1:
            QtWidgets.QTabWidget.setCurrentIndex(self.book.tabWidget, 1) # sonraki sayfaya git
        elif self.bookCount == 2:
            QtWidgets.QTabWidget.setCurrentIndex(self.book.tabWidget, 0) # onceki sayfaya git
        elif self.bookCount == 3:
            self.close()
            self.bookPage = 0

