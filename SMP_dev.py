# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 12:03:21 2019
@author: BigTail
"""

"""
Cleaner SMP download Script 
"""

from selenium import webdriver
import requests
import bs4 as bs 
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.chrome.options import Options
import os 

mail="joakim.a.svensson@lansstyrelsen.se"
url = "https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx"
password = ""
kommunList = ["Boxholm", "Finspång", "Kinda","Linköping","Mjölby","Motala","Norrköping", "Söderköping","Vadstena", "Valdemarsvik", "Ydre", "Åtvidaberg", "Ödeshög"]
     
def searchMuni(muni):
    muniPath="C:\Py3\\"+muni
    os.makedirs(muniPath, exist_ok=True)
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs", {"download.default_directory":muniPath})
    browser=webdriver.Chrome(executable_path="C:/Py3/chromedriver.exe", options=chromeOptions)
    browser.get(url)
    elemMail=browser.find_element_by_id("PageContent_ucLogin_txtUsername")
    elemMail.send_keys(mail)
    elemPass=browser.find_element_by_id("PageContent_ucLogin_txtPassword")
    elemPass.send_keys(password)
    logButton=browser.find_element_by_name("ctl00$PageContent$ucLogin$btnLogin")
    logButton.click()
    lanElem=browser.find_element_by_id("_Miljörapport")
    lanElem.click()
    obj = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlLan'))
    obj.select_by_value("05")
    objKom = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlKommun'))
    objKom.select_by_visible_text(muni)
    objMynd = Select(browser.find_element_by_id("PageContent_ucSearchAnlaggning_ddlTillsynsmyndighet"))
    objMynd.select_by_index(0) #Value: 112 Linköping kommun. 134 LstE  
    elemShow=browser.find_element_by_id("btnSearch")
    elemShow.click()
    time.sleep(3)
    count = 0 
    n = 0 
    d=browser.find_elements_by_class_name('headRow')
    for x in d:
        hit=re.match(r".+\s\d-\d+\s[a-z,A-Z]+\s\d+", x.text) # Matches e.g. Visar 61-72 av 72
        if hit:
            D=hit.group(0).split(" ")    
    while int(D[-1]) > n:
        n += 30
        elems = browser.find_elements_by_xpath('//a[@href]')
        for elem in elems:
            if elem.text == "nästa >>":
                elem.click()
                time.sleep(5)
                count = 0
                break
            if count == 1:
                elem.click()
                time.sleep(4)
                count = 0
            else:
                 a=re.match(r'\d{6},\s\d{2}:\d{2}\s\(\d\)', elem.text) #Matches e.g. 190711, 14:59 (3)
                 if a:
                    count += 1

for muni in kommunList:
    searchMuni(muni)
