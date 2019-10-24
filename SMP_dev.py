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
from bs4 import BeautifulSoup


browser=webdriver.Chrome("C:/Py3/chromedriver.exe")



mail="joakim.a.svensson@lansstyrelsen.se"
url = "https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx"

password = ""

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

Login_data = {
"__EVENTTARGET":"", 
"__EVENTARGUMENT":"", 
"__VIEWSTATEGENERATOR": "CA0B0334",
"ctl00$PageContent$ucLogin$txtUsername": "joakim.a.svensson@lansstyrelsen.se",
"ctl00$PageContent$ucLogin$txtPassword": "",
"ctl00$PageContent$ucLogin$btnLogin": "Logga in"}

url = "https://smp.lansstyrelsen.se/Default.aspx"


#__VIEWSTATE
#__VIEWSTATE": "/wEPDwUKLTU0NzE3OTU5NQ9kFgJmD2QWAgIDD2QWDAIDD2QWBgIDDxBkZBYAZAIHD2QWAmYPDxYCHgdUb29sVGlwZWRkAgkPZBYCZg8WAh4EVGV4dAUITG9nZ2EgdXRkAgUPDxYCHwBlZGQCBw8PFgIfAGVkZAIJDw8WAh8AZWRkAg8PZBYKAgMPDxYCHwEFN1bDpGxrb21tZW4gdGlsbCBTdmVuc2thIE1pbGrDtnJhcHBvcnRlcmluZ3Nwb3J0YWxlbiBTTVBkZAIFDw8WAh8BBYAIPGJyPjxicj4NClNpc3RhIHJhcHBvcnRlcmluZ3NkYWcgZsO2ciAyMDE5OiAxIGFwcmlsIDIwMTkgw6RyIHNpc3RhIHJhcHBvcnRlcmluZ3NkYXR1bSBkw6UgMzE6ZSBtYXJzIGluZmFsbGVyIHDDpSBlbiBzw7ZuZGFnLiANCjxicj48YnI+DQpIw6RyIGthbiBkdSBza2FwYSBueWEgbWlsasO2cmFwcG9ydGVyIG9jaCB0aXR0YSBww6UgaW5za2lja2FkZSBtaWxqw7ZyYXBwb3J0ZXIuIA0KPGJyPjxicj4NCsOEdmVuIGlubMOkbW5pbmcgb2NoIGV2ZW50dWVsbCBrb21wbGV0dGVyaW5nIGF2IG1pbGrDtnJhcHBvcnRlbiB0aWxsIHRpbGxzeW5zbXluZGlnaGV0ZW4gc2tlciB2aWEgbWlsasO2cmFwcG9ydGVyaW5nc3BvcnRhbGVuLjwvYj4NCjxicj48YnI+PGJyPg0KDQpUYSBkZWwgYXYgdmlrdGlnIGluZm9ybWF0aW9uIGFuZ8OlZW5kZSBTTVAgb2NoIGFrdHVlbGxhIGbDtnLDpG5kcmluZ2FyIDxicj4gcMOlIHbDpXIgbnloZXRzc2lkYSBzb20gZHUgZmlubmVyIHDDpSBTTVAtSGrDpGxwLjxicj4NClDDpSB3ZWJicGxhdHNlbiwgPGEgaHJlZj0iaHR0cDovL2V4dHJhLmxhbnNzdHlyZWxzZW4uc2Uvc21wL3N2L1BhZ2VzL2RlZmF1bHQuYXNweCIgdGFyZ2V0PSJfYmxhbmsiPlNNUC1IasOkbHA8L2E+IGZpbm5zIMOkdmVuIHNhbWxhZCBpbmZvcm1hdGlvbiBvbSBkZXQgDQo8YnI+IG1lc3RhIGkgU01QLiBHw6UgZ8Okcm5hIGluIG9jaCB0YSBkZWwgYXYgaW5zdHJ1a3Rpb25lcm5hIA0Kb2NoIDxicj4NCm1hbGxhcm5hIHNvbSBsaWdnZXIgcMOlIGRlbi4gDQo8L2JpZz48YnI+PGJyPg0KDQpIYXIgZHUgcHJvYmxlbSBhdHQgbG9nZ2EgaW4gZWxsZXIgYmVow7Z2ZXIgaGrDpGxwIG1lZCBhdHQgYWRtaW5pc3RyZXJhIGtvbnRvbj8gDQo8YnI+DQpMw6RzIHVuZGVyIDxhIGhyZWY9Imh0dHA6Ly9leHRyYS5sYW5zc3R5cmVsc2VuLnNlL3NtcC9Tdi9odXItZ29yLWphZy9rb250b2hhbnRlcmluZy9TaWRvci9kZWZhdWx0LmFzcHgiIHRhcmdldD0iX2JsYW5rIj5rb250b2hhbnRlcmluZzwvYT4NCg0KPGJyPjxicj4NCmRkAgcPDxYEHgRtcmlkZB4HVmlzaWJsZWdkFhICAQ8PFgIfA2hkZAIDDw8WAh8BBQhMb2dnYSBpbmRkAgUPDxYCHwEFH0UtcG9zdGFkcmVzcy9hbnYmYXVtbDtuZGFybmFtbjpkZAIJDw8WAh8BBQ5MJm91bWw7c2Vub3JkOmRkAg0PDxYEHwEFCExvZ2dhIGluHwAFCExvZ2dhIGluZGQCDw8PFgIfA2hkZAIRDw8WBh8BBRZHbMO2bXQgbMO2c2Vub3JkZXQ/IMK7HwAFEkdsw7ZtdCBsw7ZzZW5vcmRldB4LTmF2aWdhdGVVcmwFHC9EZWZhdWx0LmFzcHg/c2VsZWN0ZWRWaWV3PTdkZAITDw8WBB8BBRxSZWdpc3RlcmEgYW5sJmF1bWw7Z2duaW5nIMK7HwAFFVJlZ2lzdGVyYSBhbmzDpGdnbmluZ2RkAhUPDxYEHwEFHlJlZ2lzdGVyYSB0aWxsc3luc215bmRpZ2hldCDCux8ABRtSZWdpc3RlcmEgdGlsbHN5bnNteW5kaWdoZXRkZAIJD2QWDgIBDw8WAh8BBRBHbMO2bXQgbMO2c2Vub3JkZGQCAw8PFgIfAQXgAUFuZ2UgZS1wb3N0YWRyZXNzL2FudiZhdW1sO25kYXJuYW1uIG9jaCB2JmF1bWw7bGogIlNraWNrYSIgZiZvdW1sO3IgYXR0IGYmYXJpbmc7IGV0dCBueXR0IGwmb3VtbDtzZW5vcmQgc2tpY2thdCB0aWxsIGFuZ2l2ZW4gZS1wb3N0YWRyZXNzLiBWJmF1bWw7bGogIkF2YnJ5dCIgZiZvdW1sO3IgYXR0ICZhcmluZzt0ZXJnJmFyaW5nOyB0aWxsIGlubG9nZ25pbmdzZm9ybXVsw6RyZXQuIDwvYnI+ZGQCBQ8PFgIfAQU6RXR0IG55dHQgbMO2c2Vub3JkIGhhciBza2lja2F0cyB0aWxsIGFuZ2l2ZW4gZS1wb3N0YWRyZXNzLmRkAgcPDxYCHwEFG0UtcG9zdGFkcmVzcy9hbnbDpG5kYXJuYW1uOmRkAgsPDxYEHwEFBlNraWNrYR8ABQZTa2lja2FkZAINDw8WBB8BBQZBdmJyeXQfAAUGQXZicnl0ZGQCEQ8PFgIfA2hkZAILD2QWAgIBDw8WCB8EBSpodHRwOi8vdXRzbGFwcGlzaWZmcm9yLm5hdHVydmFyZHN2ZXJrZXQuc2UfAAUSVXRzbMOkcHAgaSBzaWZmcm9yHwEFBFV0aXMeBlRhcmdldAUFYmxhbmtkZAIRD2QWEGYPFgIfA2gWBAIBDw8WAh8BBRNUaWxsc3luc215bmRpZ2hldDogZGQCBg8PFgIfAQUFVGVsOiBkZAICDw8WAh8BBQpBbnN2YXJpZzogZGQCBA8PFgYfAQUcc21wLnN1cHBvcnRAbGFuc3N0eXJlbHNlbi5zZR8ABSdNYWlsYSB0aWxsIHNtcC5zdXBwb3J0QGxhbnNzdHlyZWxzZW4uc2UfBAUjbWFpbHRvOnNtcC5zdXBwb3J0QGxhbnNzdHlyZWxzZW4uc2VkZAIGDw8WAh8BBQlTdXBwb3J0OiBkZAIHDw8WBh8BBRxzbXAuc3VwcG9ydEBsYW5zc3R5cmVsc2VuLnNlHwAFJ01haWxhIHRpbGwgc21wLnN1cHBvcnRAbGFuc3N0eXJlbHNlbi5zZR8EBSNtYWlsdG86c21wLnN1cHBvcnRAbGFuc3N0eXJlbHNlbi5zZWRkAgkPDxYEHwEFEk9tIGNvb2tpZXMgcMOlIFNNUB8AZWRkAgsPDxYEHwEFD09tIEdEUFIgcMOlIFNNUB8AZWRkAg0PDxYCHwEFDiBWZXJzaW9uIDE2LjE1ZGRkovD+lHDYkTWVU5TCY36oZKjclUM

with requests.Session() as s:
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    Login_data['__VIEWSTATE'] = soup.find('input', attrs={'name':'__VIEWSTATE'})['value']
    r=s.post(url, data=Login_data)
    print(r.content)
    r=s.get(url)
    r.content
    
