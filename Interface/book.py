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
        self.setFixedSize(930,662)
        self.bookCount = 0
        degerler = list()
        self.pageNo = int()
        self.read1()
        self.textEdit.setText(''+str(self.degerler[int(self.pageNo)])+ "\n\n\n" + str(self.pageNo+1))
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
            self.nextPage()
        elif self.bookCount == 2:
            self.prevPage()
        elif self.bookCount == 3:
            self.close()
            self.bookPage = 0

    def nextPage(self):
        self.pageNo = self.pageNo + 1
        if(self.pageNo >= len(self.degerler)):
            self.pageNo = 0
        self.textEdit.setText(''+str(self.degerler[int(self.pageNo)])+ "\n\n\n" + str(self.pageNo+1))

    def prevPage(self):
        self.pageNo = self.pageNo - 1
        if(self.pageNo <= 0):
            self.pageNo = len(self.degerler)
        self.textEdit.setText(''+str(self.degerler[int(self.pageNo-1)])+ "\n\n\n" + str(self.pageNo))
        
    def read1(self):
        f = open("Interface/sefiller1.txt", "r")
        icerik = f.read()
        self.degerler = list()
        for satir in icerik.split('\n'):
            self.degerler.append(satir) 
