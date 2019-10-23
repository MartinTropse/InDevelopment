# -*- coding: utf-8 -*-

"""
Created on Tue Oct 22 14:41:06 2019
@author: BigTail 
"""

from selenium import webdriver
import selenium
#from selenium.webdriver.common.keys import Keys
import requests
import pyautogui as auto
import bs4 as bs 
from selenium.webdriver.support.select import Select

browser=webdriver.Chrome("C:/Py3/chromedriver.exe")



mail="joakim.a.svensson@lansstyrelsen.se"
url = "https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx"

password = '!nneBandy22'

#browser=webdriver.Firefox(executable_path=r'C:\Py3\geckodriver.exe')    

def loginFunc(password):
    browser=webdriver.Chrome("C:/Py3/chromedriver.exe")
    browser.get(url)
    elemMail=browser.find_element_by_id("PageContent_ucLogin_txtUsername")
    elemMail.send_keys(mail)
    elemPass=browser.find_element_by_id("PageContent_ucLogin_txtPassword")
    elemPass.send_keys(password)
    logButton=browser.find_element_by_name("ctl00$PageContent$ucLogin$btnLogin")
    logButton.click()  
    lanElem=browser.find_element_by_id("_Miljörapport")
    lanElem.click()
    return browser

browser=loginFunc(password)

kommunList = ["Boxholm", "Finspång", "Kinda","Linköping","Mjölby","Motala","Norrköping", "Söderköping","Vadstena", "Valdemarsvik", "Ydre", "Åtvidaberg", "Ödeshög"]

obj = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlLan'))
obj.select_by_value("05")
objKom = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlKommun'))
objKom.select_by_visible_text("Linköping")

elemShow=browser.find_element_by_id("btnSearch")
elemShow.click()

browser.find_element_by_link_text()

s = requests.session()
a=s.get(url)
c=a.text


