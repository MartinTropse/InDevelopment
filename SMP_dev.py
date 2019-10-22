# -*- coding: utf-8 -*-

"""
Created on Tue Oct 22 14:41:06 2019
@author: BigTail 
"""



from selenium import webdriver
import selenium

#from selenium.webdriver.common.keys import Keys

browser=webdriver.Chrome("C:\Py3\chromedriver.exe")
mail="joakim.a.svensson@lansstyrelsen.se"

def loginFunc(password):
    browser=webdriver.Chrome("C:\Py3\chromedriver.exe")    
    browser.get("https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx")
    elemMail=browser.find_element_by_id("PageContent_ucLogin_txtUsername")
    elemMail.send_keys(mail)
    elemPass=browser.find_element_by_id("PageContent_ucLogin_txtPassword")
    elemPass.send_keys(password)
    logButton=browser.find_element_by_name("ctl00$PageContent$ucLogin$btnLogin")
    logButton.click()


loginFunc("!nneBandy22")



=browser.find_element_by_name=("ctl00$PageContent$ucSearchAnlaggning$ddlLan")


<select name="ctl00$PageContent$ucSearchAnlaggning$ddlLan" id="PageContent_ucSearchAnlaggning_ddlLan" class="select1000_1" onchange="UpdateKommunList()" onkeydown="if( event.keyCode == 13 ) return Search();">
	
</option><option value="05">Östergötlands län</option></select>

<select name="ctl00$PageContent$ucSearchAnlaggning$ddlLan" id="PageContent_ucSearchAnlaggning_ddlLan" class="select1000_1" onchange="UpdateKommunList()" onkeydown="if( event.keyCode == 13 ) return Search();">
	






	


#browser=webdriver.Chrome("C:\Py3\chromedriver.exe")
#browser.get("https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx")
#
#elem.click()
#
#<input type="submit" name="ctl00$PageContent$ucLogin$btnLogin" value="Logga in" id="PageContent_ucLogin_btnLogin" title="Logga in">