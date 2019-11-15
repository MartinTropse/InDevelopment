# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:28:52 2019
@author: MartinTropse
"""

from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import re
import time
import os 
import tabula
import pytesseract
from PIL import Image
from wand.image import Image as wi
import io
import shutil
import collections
import pandas as pd
from matplotlib import pyplot as plt
#import pickle

start=time.time()




os.chdir(r"C:\Py3\SMP\PDF_Mine\pdf")

myDf=pd.DataFrame(columns={"Path", 'Kommun', 'Year','SNI', 'BinaryHit'})
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pdfList=os.listdir()

mail="joakim.a.svensson@lansstyrelsen.se"
url = "https://smp.lansstyrelsen.se/Tillsynsmyndighet/SearchAnlaggning.aspx"
password = "!nneBandy22"


# =============================================================================
# Use input is given through this variables. Make sure that year and baseDir match. 
# =============================================================================
kommunList = ["Linköping","Mjölby","Motala","Norrköping", "Söderköping","Vadstena", "Valdemarsvik", "Ydre", "Åtvidaberg", "Ödeshög"] #"Kinda", "Boxholm"
year = 2016
baseDir='C:/SMP/2016'
#baseDir="C:/SMP/2015/Ödeshög"

# =============================================================================
# Defining functions section
# =============================================================================


# =============================================================================
# Download data (pdf and txt) from the SMP database. The data is divided by municipality
# and year.
# =============================================================================
def DownloadSMP(muni, year="2018"):
    muniPath="C:\SMP\\"+year+"\\"+muni
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
    while True:
        try:
            obj = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlLan'))
            obj.select_by_value("05")
        except StaleElementReferenceException:
            continue
        break
    while True:
        try:
            objKom = Select(browser.find_element_by_id('PageContent_ucSearchAnlaggning_ddlKommun'))
        except StaleElementReferenceException:
            continue
        break
    time.sleep(1)
    objKom.select_by_visible_text(muni)
    while True:
        try:
            objYear = Select(browser.find_element_by_id("PageContent_ucSearchAnlaggning_ddlVerksamhetsAr"))
            objYear.select_by_visible_text(year) #Value: 112 Linköping kommun. 134 LstE 
            objMynd = Select(browser.find_element_by_id("PageContent_ucSearchAnlaggning_ddlTillsynsmyndighet"))
            objMynd.select_by_index(0) #Value: 112 Linköping kommun. 134 LstE  
            elemShow=browser.find_element_by_id("btnSearch")
            elemShow.click()
        except (StaleElementReferenceException, ElementClickInterceptedException): #
            continue
        break
    while True:
        try:
            uStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassU").is_selected() #Check if the boxes are filled, if not, fill it!
            if not uStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassU").click()                
            tStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassT").is_selected()
            if not tStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassT").click()                
            pStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassP").is_selected()
            if not pStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassP").click()                
            cStatus=browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassC").is_selected()
            if not cStatus:
                time.sleep(0.2)
                browser.find_element_by_id("PageContent_ucSearchAnlaggning_cbxKlassC").click()
        except (StaleElementReferenceException, ElementClickInterceptedException):
            continue
        break
    count = 0 
    n = 0
    time.sleep(2)
    d=browser.find_elements_by_class_name('headRow')
    for x in d:
        hit=re.match(r".+\s\d-\d+\s[a-z,A-Z]+\s\d+", x.text) # Matches e.g. Visar 61-72 av 72
        if hit:
            D=hit.group(0).split(" ") #Splites the data by words
    while int(D[-1]) > n: #Takes out the last number of the string ~"Visar 61-72 av 72". n is increased by 30 per step in the loop, since the amount of shown values is 30. When n is bigger then D[-1] loop breaks.  
        n += 30
        elems = browser.find_elements_by_xpath('//a[@href]')
        for elem in elems:
            if elem.text == "Emissonsdeklaration":
                elem.click()
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
    print(f"\nCompleted downloads from {muni} {year}")  

# =============================================================================
# A tool to extract text from pdfs and condense the information through extracting 
# specific sentences
# =============================================================================
def pdfMiner(baseDir):
    #current_time = time.time()
    #print(f"this is current time {current_time}")
    imPath="C:/Users/Jessica Henestål/AppData/Local/Temp"
    for baseFold, subdir, files in os.walk(baseDir):
        for file in files:
            if '.pdf' in file:
                print(f"Extracting text from {file}")
                machineList= []
                extracted_text = []    
                imgBlobs = []
                pdf = wi(filename=baseFold+"/"+file, resolution = 300)
                pdfImg = pdf.convert('jpeg')
                for img in pdfImg.sequence:
                    page=wi(image=img) #This opens an actual image
                    imgBlobs.append(page.make_blob('jpeg')) #This object contains byte data, make_blob cause the conversion    
                #The bytes object is the converted back to image before being passed to pytesseract    
                for imgBlob in imgBlobs:
                    im = Image.open(io.BytesIO(imgBlob)) #"im" is an PIL, JpegImageFile which is assumes is the prefered object of tessearct
                    text = pytesseract.image_to_string(im, lang='swe')
                    extracted_text.append(text)    
                pos = -1
                pat = re.compile(r'([A-Z,Å,Ä,Ö][^\.!?]*[\.!?])', re.M) # pattern: Upercase, then anything that is not in (.!?), then one of them
                path=baseFold+"/"+file[:-4]
                os.makedirs(path, exist_ok=True)
                for page in extracted_text:
                    pos += 1
                    newSent = ""  
                    splitSent=pat.findall(page)
                    for sentc in splitSent:
                        newSent += re.sub("\n", " ", sentc)
                    extracted_text[pos] = newSent
                nPage = 0
                for page in extracted_text:
                    chkVal = 0
                    nPage += 1
                    pat = re.compile(r'([A-Z,Å,Ä,Ö][^\.!?]*[\.!?])', re.M)
                    splitSent=pat.findall(page)
                    nLine = 0
                    for x in splitSent:
                        nLine +=1
                        mash=re.search('CO2|MWh|TWh|KWh',x, re.IGNORECASE)
                        if mash:
                            machineList.append(x+" Page number "+str(nPage)+" sentence "+str(nLine))
                            if chkVal == 0:
                                imgBlob=imgBlobs[nPage-1]
                                im = Image.open(io.BytesIO(imgBlob))
                                im.save(path+"/"+"Page_"+str(nPage)+".jpeg")
                                chkVal +=1
                with open(path+"/"+file[:-4]+".txt", 'w') as nwFile:
                    if len(machineList) > 0:
                        for line in machineList:
                            nwFile.write(line)
                            nwFile.write('\n')
    print("Text extraction complete!")
    #return extracted_text
# =============================================================================
# Export tables that includes the matching 
# =============================================================================
def getTheTable(mainDir):
    SNI_List = []
    MNI_List = []
    path = []
    energy = []
    sValue = 0
    kValue = 0
    for mainDir, subDir, files in os.walk(baseDir):
        for file in files:
            if ".pdf" in file:
                df = tabula.read_pdf(mainDir+"/"+file, pages='all', multiple_tables=True)
                path.append(mainDir+"/"+file)
                count = 0
                for subDf in df:
                    if subDf.shape[0] > 0:
                        subDf.columns = subDf.iloc[0,:]
                        subDf=subDf.iloc[1:,:]
                        subDf=subDf.dropna(axis=[0], how='all')
                        subDf=subDf.dropna(axis=[1], how='all')                
                        count += 1
                        if "UPPGIFTER OM VERKSAMHETSUTÖVAREN" in subDf.columns:
                            for line in subDf.iloc[:,0]:
                                if type(line) == str:
                                    if kValue == 1:
                                        MNI_List.append(line)
                                        kValue = 0
                                    if sValue == 1:
                                        SNI_List.append(line)
                                        sValue = 0
                                    if 'Kommun:\r' in line:
                                        MNI_List.append(line[8:])
                                    elif "Kommun:" in line:
                                        kValue = 1
                                    if "Huvudverksamhet och verksamhetskod:\r" in line:
                                        SNI_List.append(line[36:])
                                    elif "Huvudverksamhet och verksamhetskod:" in line:
                                        sValue = 1
                        for cPos in range(0, subDf.shape[1]):
                            if energy:
                                energy = []
                                break
                            aCol=subDf.iloc[:,cPos].astype('str')
                            energy=list(filter(lambda x: re.search(pattern, x), aCol))
                            if energy and 0.65>sum(len(subDf) - subDf.count())/(subDf.shape[0]*subDf.shape[1]):
                                xlfile=(mainDir+"/"+file[:-4]+"/"+"Table"+str(count)+".xlsx").replace("\\", "/")
                                subDf.to_excel(xlfile, encoding='windows-1252', index=False)
    return SNI_List, MNI_List, path

# =============================================================================
# Moves the pdfs reports into their respective folder
# =============================================================================
def move_pdf(baseDir):
    for baseFold, subdir, files in os.walk(baseDir):
        for file in files:
            if '.pdf' in file:
                try:
                    src=(baseFold+"/"+file).replace("\\", "/")
                    dst=(baseFold+"/"+file[:-4]+"/"+file).replace("\\", "/")
                    shutil.move(src, dst)
                except Exception as e:
                    print("")

# =============================================================================
# Make a summary on the available data 
# =============================================================================
def pdfSummary(baseDir):
    hitList = []
    for baseFold, subdir, files in os.walk(baseDir):
        baseFold=baseFold.replace("\\","/")
        if len(baseFold.split('/')) == 3:
            pkomCount=collections.Counter(os.listdir(baseFold))
            nkomCount=collections.Counter(os.listdir(baseFold))
            pkomCount.subtract(nkomCount)
            nkomCount.subtract(nkomCount)
        if len(baseFold.split('/')) == 5:
            if len(files) > 2:
                pkomCount[baseFold.split('/')[-2]]+=1
                hitList.append(1)
            if len(files) <= 2:
                nkomCount[baseFold.split('/')[-2]] +=1
                hitList.append(0)
    for key in nkomCount.keys():
        aSum=pkomCount[key]+nkomCount[key]
        print("I ", key, year,"hittades information gällande energi och fossila utsläpp i", round(pkomCount[key]/aSum, 2)*100, "% av miljörapporterna\n")
    #return hitList

# =============================================================================
# Running the script section 
# =============================================================================
for muni in kommunList:
    DownloadSMP(muni, str(year))

pdfMiner(baseDir)
SNI_List, MNI_List, path=getTheTable(baseDir)
move_pdf(baseDir)
hitList=pdfSummary(baseDir)

# =============================================================================
# Minor adjustments, exporting data and creating graphs
# =============================================================================
myDf['Kommun'] = MNI_List
myDf['SNI'] = SNI_List
myDf['Path'] = path
for x in range(0, myDf.shape[0]):
    myDf['Path'][x]=re.sub(r"\\", "/", myDf['Path'][x])
    
myDf['Year'] =  [year]*myDf.shape[0]
myDf['Year']= myDf['Year'].astype('str')
myDf['BinaryHit'] = hitList

os.chdir(baseDir)
myDf.to_csv('Data.csv', index=False, encoding='latin-1')
MuniData=myDf.groupby(['Kommun']).mean()['Hit']
SNIData=myDf.groupby(['SNI']).mean()['Hit']

#Create/Export municipality graph 
plt.bar(x=hold.index, height=hold, color='k', width=0.4, edgecolor='w')
plt.xlabel('Kommun', size=15)
plt.ylabel('Andel matchande rapporter', size=15)
plt.title('Andel matchande rapporter per kommmun', size=15)
axes = plt.gca()
axes.set_ylim([0,1])
plt.show()
plt.savefig(f"KommunSammanställning {year}")

#Create/Export SNI graph
plt.bar(x=SNIData.index, height=SNIData, color='k', width=0.6, edgecolor='w')
plt.xlabel('SNI', size=15)
plt.title('Andel matchande rapporter per SNI', size=15)
plt.xticks(rotation=90)
fig.subplots_adjust(bottom=0.5)
plt.show()
plt.savefig(f"SNI_Sammanställning {year}")

end=time.time()
runtime=end-start

print(f"SMP analysis of {year} completed. Run time was {runtime} seconds")

##Code block that removes files from wand folder. Runs better if you close down spyder in between 
#imPath=r"C:\Users\Jessica Henestål\AppData\Local\Temp"
#for f in os.listdir(imPath):
#    creation_time = os.path.getctime(imPath+"/"+f)
#    if (creation_time - start) > 0:
#        try:
#            os.unlink(imPath+"/"+f)
#            print(f'{f} removed')
#        except Exception as e:
#            print(e)






# =============================================================================
# Test Ground
# =============================================================================




#def pdf_summary(baseDir):
#    for baseFold, subdir, files in os.walk(baseDir):
#        baseFold=baseFold.replace("\\","/")
#        if len(baseFold.split('/')) == 3:
#            pkomCount=collections.Counter(os.listdir(baseFold))
#            nkomCount=collections.Counter(os.listdir(baseFold))
#            pkomCount.subtract(nkomCount)
#            nkomCount.subtract(nkomCount)
#        if len(baseFold.split('/')) == 5:
#            if len(files) > 2:
#                pkomCount[baseFold.split('/')[-2]]+=1
#            if len(files) <= 2:
#                nkomCount[baseFold.split('/')[-2]] +=1
#    for key in nkomCount.keys():
#        aSum=pkomCount[key]+nkomCount[key]
#        print("I ", key, year,"hittades information gällande energi och fossila utsläpp i", round(pkomCount[key]/aSum, 2)*100, "% av miljörapporterna\n")
#        

#df = tabula.read_pdf("C:/SMP/2014/Boxholm/0560-60-001_2015_2.pdf", pages='all', multiple_tables=True)
#
#baseDir="C:/SMP/2014"
#
#pattern=re.compile(r"MWh|TWh|CO2", re.IGNORECASE)
#energy = []
#SNI_List = []
#MNI_List = []
#sValue = 0
#kValue = 0
#
#for mainDir, subDir, files in os.walk(baseDir):
#    for file in files:
#        if ".pdf" in file:
#            df = tabula.read_pdf(mainDir+"/"+file, pages='all', multiple_tables=True) 
#            count = 0
#            for subDf in df:
#                if subDf.shape[0] > 0:
#                    subDf.columns = subDf.iloc[0,:]
#                    subDf=subDf.iloc[1:,:]
#                    subDf=subDf.dropna(axis=[0], how='all')
#                    subDf=subDf.dropna(axis=[1], how='all')                
#                    count += 1
#                    if "UPPGIFTER OM VERKSAMHETSUTÖVAREN" in subDf.columns:
#                        print("Can I Enter?")
#                        for line in subDf.iloc[:,0]:
#                            if type(line) == str:
#                                if sValue == 1:
#                                    SNI_List.append(line)
#                                    sValue = 0
#                                    print(SNI_List)
#                                if kValue == 1:
#                                    MNI_List.append(line)
#                                    kValue = 0
#                                    print(MNI_List)
#                                    time.sleep(3)
#                                if "Huvudverksamhet och verksamhetskod:" in line:
#                                    sValue = 1
#                                if 'Kommun:' in line:
#                                    kValue = 1
#                    for cPos in range(0, subDf.shape[1]):
#                        if energy:
#                            energy = []
#                            break
#                        aCol=subDf.iloc[:,cPos].astype('str')
#                        energy=list(filter(lambda x: re.search(pattern, x), aCol))
#                        if energy and 0.65>sum(len(subDf) - subDf.count())/(subDf.shape[0]*subDf.shape[1]):
#                            xlfile=(mainDir+"/"+file[:-4]+"/"+"Table"+str(count)+".xlsx").replace("\\", "/")
#                            subDf.to_excel(xlfile, encoding='windows-1252', index=False)
#
#
#
#df = tabula.read_pdf(r"C:\SMP\2014\Boxholm\0560-233-01-C_2014_1.pdf", pages='all', multiple_tables=True)
#df[0]
#df = tabula.read_pdf(r"C:\SMP\2014\Boxholm\0560-60-001_2014_2.pdf", pages='all', multiple_tables=True)
#
#aDf=df[0].replace("\r", "\n")
#
#
#SNI_List = []
#MNI_List = []
#sValue = 0
#kValue = 0
#
#baseDir="C:/SMP/2014"
#
#pattern=re.compile(r"MWh|TWh|CO2", re.IGNORECASE)
#energy = []






                    

#def getTheTable(baseDir):
#    pattern=re.compile(r"MWh|TWh|CO2", re.IGNORECASE)
#    energy = []
#    SNI_List = []
#    MNI_List = []
#    sValue = 0
#    kValue = 0
#    for mainDir, subDir, files in os.walk(baseDir):
#        for file in files:
#            if ".pdf" in file:
#                df = tabula.read_pdf(mainDir+"/"+file, pages='all', multiple_tables=True) 
#                count = 0
#                for subDf in df:
#                    count += 1
#                    for line in subDf[0]:
#                        if sValue == 1:
#                            SNI_List.append(line)
#                            sValue = 0
#                        if kValue == 1:
#                            MNI_List.append(line)
#                            kValue = 0
#                        if "Huvudverksamhet och verksamhetskod:" in line:
#                            sValue = 1
#                        if 'Kommun:' in line:
#                            kValue = 1
#                    if subDf.shape[0] > 0:
#                        subDf.columns = subDf.iloc[0,:]
#                        subDf=subDf.iloc[1:,:]
#                        subDf=subDf.dropna(axis=[0], how='all')
#                        subDf=subDf.dropna(axis=[1], how='all')
#                        for cPos in range(0, subDf.shape[1]):
#                            if energy:
#                                energy = []
#                                break
#                            aCol=subDf.iloc[:,cPos].astype('str')
#                            energy=list(filter(lambda x: re.search(pattern, x), aCol))
#                            if energy and 0.65>sum(len(subDf) - subDf.count())/(subDf.shape[0]*subDf.shape[1]):
#                                xlfile=(mainDir+"/"+file[:-4]+"/"+"Table"+str(count)+".xlsx").replace("\\", "/")
#                                subDf.to_excel(xlfile, encoding='windows-1252', index=False)
#    return SNI_List, MNI_List