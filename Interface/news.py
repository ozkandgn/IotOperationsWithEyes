import sys, threading, requests, time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import *
from .Threading import thread

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from selenium.webdriver import Remote
from selenium.webdriver import  DesiredCapabilities
from selenium.webdriver.remote import webelement , command
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions

class News(QMainWindow):
    def __init__(self):
        super(News,self).__init__()
        loadUi('Interface/news.ui',self)
        self.setWindowTitle('HABERLER')
        self.newsCount = 0
        self.haberArtirBtn.clicked.connect(self.haberArtirBtn_clicked)
        self.haberAzaltBtn.clicked.connect(self.haberAzaltBtn_clicked)

    def open_browser(self):
        driver_path = "C:/Users/ozans/Desktop/haber/chromedriver_win32/chromedriver"
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.haberler = []
        self.link = "https://www.posta.com.tr"
        self.getNewsHeader()
        self.getNewsLink()
        
    @pyqtSlot()
    def haberArtirBtn_clicked(self):
        self.newsCount=self.newsCount + 1
        if int(self.newsCount) > len(self.haberList):
            self.newsCount = 1
        self.newsCountLbl.setText(''+str(int(self.newsCount)))
        self.haberList.setCurrentRow(self.newsCount-1)
        print(str(self.haberList.currentItem().text())) #print selected item on listview

    def haberAzaltBtn_clicked(self):
        self.newsCount=self.newsCount - 1
        if int(self.newsCount) <= 0:
            self.newsCount = len(self.haberList)
        self.newsCountLbl.setText(''+str(int(self.newsCount)))
        self.haberList.setCurrentRow(self.newsCount-1)
        print(str(self.haberList.currentItem().text()))

    def haberOnaylaBtn_clicked(self):
        if self.news.newsCount == 1:
            self.openNews()
        elif self.news.newsCount == 2:
            self.news.openNews()
        elif self.news.newsCount == 3:
            self.news.openNews()
        elif self.news.newsCount == 4:
            #self.news.browser.quit()
            self.close()
            #news_frame = 0

    def getNewsHeader(self):
        url = "https://www.posta.com.tr/son-dakika-haberleri"
        url_oku = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_oku, 'html.parser')
        icerik = soup.find_all('div',attrs={'class':'breaking-news__card'},limit=3)
        haber_basliklari=[]
        for i in range(3):
            haber_basliklari.append(str(icerik[i].text).strip())
        self.haber1Lbl.setText('' + str(haber_basliklari[0]))
        self.haber2Lbl.setText('' + str(haber_basliklari[1]))
        self.haber3Lbl.setText('' + str(haber_basliklari[2]))

    def getNewsLink(self):
        url = "https://www.posta.com.tr/son-dakika-haberleri"
        url_oku = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_oku, 'html.parser')
        haber_linki = soup.find_all("a",attrs={"class","breaking-news__title"}, limit=3)
        for link in haber_linki:
            self.haberler.append(link.get("href"))

    def openNews(self):
        url = "https://www.posta.com.tr/son-dakika-haberleri"
        url_oku = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_oku, 'html.parser')
        self.link += self.haberler[int(self.newsCount) - 1]
        self.browser.get(self.link)
        
    def newsScrollDown(self):
        touchactions = TouchActions(self.browser)
        self.browser.execute_script("window.scrollTo(0, 1000);")
        
