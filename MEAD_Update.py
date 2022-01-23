# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 22:27:44 2021
@author: martin.andersson-li

Look at each inventory that will be added to MEAD and see if all ID:s within 
tables matches. 

"""
import os
import pandas as pd
import re
import time

os.chdir("P:/eDNA/MEAD/IncludedProjects")
rootDir=os.listdir()

PS=re.compile("Sample.csv$")
PP=re.compile("project.csv$")
PO=re.compile("(?<!Update)OTU_[0-9]{6}MiFish_MEAD.csv$")

#PO=re.compile("MiFish_MEAD.csv$")
otu = []
project = []
sample = []
aVal = 0


for aDir in rootDir:
    aList = os.listdir(os.getcwd()+"\\"+aDir)
    for x in aList:
        sHit=re.search(PS,x)
        oHit=re.search(PO,x)
        pHit=re.search(PP,x)
        if sHit:
            sample.append(x)
            aVal+=1
        if oHit:
            otu.append(x)
            aVal+=1
        if pHit:
            project.append(x)
            aVal+=1
        if aVal == 3:
            aVal = 0
            print("Comparing SampleID in folder: ", aDir)
            oFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+otu[0])
            pFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+project[0],sep=";")
            sFile=pd.read_csv(os.getcwd()+"\\"+aDir+"\\"+sample[0])
            oID=oFile["SampleID"].str.match("^((?!Lab).)*$")
            ngID=[not y for y in oID]
            posFile=oFile[list(map(bool, oID))]
            negFile=oFile[list(map(bool, ngID))]
            print("Removed rows from OTU-table: ",negFile['SampleID'].unique())
            spSet=set(sFile['SampleID'])
            otSet=set(posFile['SampleID'])
            for x in posFile['SampleID'].unique():
                if x not in spSet:
                    print(f"This sampleID is missing in Sample-table: {x}")
            for y in sFile['SampleID'].unique():
                if y not in otSet:
                    print(f"This sampleID is missing in OTU-table: {y}")
            print("Do you want to save the updated OTU file? Y/N?")
            chkPoint=input()
            if chkPoint == "Y":
                oFile.to_csv(os.getcwd()+"\\"+aDir+"\\"+"Update"+otu[0])
                print("Updated file was stored at:\n", os.getcwd()+"\\"+aDir+"\\"+"Update"+otu[0],"\n\n")
                print("Continues to next folder in 2!\n")
                time.sleep(2)
                otu = []
                project = []
                sample = []
            else:
                print("Continues to next folder in 2!\n")
                time.sleep(2)
                otu = []
                project = []
                sample = []
            

#pSl=re.compile("[0-9]{6}_Sample\.csv$")
#pOt=re.compile("OTU_[0-9]{6}[A-Za-z]+_MEAD.csv")
#pPj=re.compile("[0-9]{6}_project\.csv$")
#files = os.listdir(rootPth+"\\"+topFiles[0])            
#fileP=re.compile("(Sample.csv$|project.csv$|MiFish_MEAD.csv$)")

#aList = ["OTU_102634MiFish_MEAD.csv","102634_Sample.csv","102634_project.csv"]
#sample = []
#project = []
#otu = []
#aList = os.listdir(os.getcwd()+"\\"+rootDir[0])

#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    if files
#    
#    for f in files:
#        if f.endswith('Sample.csv'):
#            sFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)
#        if f.endswith('project.csv'):
#            pFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)
#        if f.endswith('MEAD.csv'):
#            oFile=pd.read_csv(os.getcwd()+"\\"+subDir+"\\"+f)
#            print(os.getcwd()+"\\"+subDir+"\\"+f)

   
     
        
        
    #time.sleep(2)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#        if re.search(pOt, f):
#            oHit=re.search(pOt,f)
#            oFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+oHit[0])
#        if re.search(pPj, f):
#            pHit=re.search(pPj,f)
#            pFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+pHit[0], sep=";", nrows=1)
#        try:
#            oFile
#            pFile
#            sFile
#        except NameError:
#            continue
#        else:
#            print("\n\n",subDir)
#            print(rootPth+"\\"+subDir+"\\"+pHit[0])
#            print(rootPth+"\\"+subDir+"\\"+oHit[0])
#            print(rootPth+"\\"+subDir+"\\"+sHit[0])
#            oID=oFile["SampleID"].str.match("^((?!Lab).)*$")
#            ngID=[not y for y in oID]
#            posFile=oFile[list(map(bool, oID))]
#            negFile=oFile[list(map(bool, ngID))]
#            print("Removed rows from OTU-table: ",negFile['SampleID'].unique())
#            spSet=set(sFile['SampleID'])
#            otSet=set(posFile['SampleID'])
#            for x in posFile['SampleID'].unique():
#                if x not in spSet:
#                    print(f"This sampleID is missing in sample table: {x}")
#            for y in sFile['SampleID']:
#                if y not in otSet:
#                    print(f"This sampleID is missing in OTU-table: {y}")
#            del(oFile)
#            del(pFile)
#            del(sFile)
#            del(pHit)
#            del(sHit)
#            del(oHit)
#            
#            
        

#
#oFile.empty*1+sFile.empty*1+pFile.empty*1
#
#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    if(re.search(pSl,files)):
#        
#    if:
#       sampleFile = sFile[0]
#    if 
#    
#    sDf=pd.read_csv(sFile[0])
#    oFile = re.search(pOt,files[2]) 
#    oDf = pd.read_csv(oFile[0])
#    thID=oDf["SampleID"].str.match("^((?!Lab).)*$")
#    ngID=[not y for y in thID]
#    posDf=oDf[list(map(bool, thID))]
#    negDf=oDf[list(map(bool, ngID))]
#    print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#    spSet=set(sDf['SampleID'])
#    otSet=set(posDf['SampleID'])
#    for x in posDf['SampleID'].unique():
#        if x not in spSet:
#            print(f"This sampleID is missing in sample table: {x}")
#    for y in sDf['SampleID']:
#        if y not in otSet:
#            print(f"This sampleID is missing in OTU-table: {x}")
#
#
#import os
#wd  = os.getcwd()
#directories = os.walk(wd)
#[print(x) for x in directories]

#for root, dirs in os.walk("P:/eDNA/MEAD/IncludedProjects"):
#    for aDir in dirs:
#        files=os.listdir()
#        sFile=re.search(pSl,files[1])
#        sDf=pd.read_csv(sFile[0])
#        oFile = re.search(pOt,files[2]) 
#        oDf = pd.read_csv(oFile[0])
#        thID=oDf["SampleID"].str.match("^((?!Lab).)*$")
#        ngID=[not y for y in thID]
#        posDf=oDf[list(map(bool, thID))]
#        negDf=oDf[list(map(bool, ngID))]
#        print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#        spSet=set(sDf['SampleID'])
#        otSet=set(posDf['SampleID'])
#        for x in posDf['SampleID'].unique():
#            if x not in spSet:
#                print(f"This sampleID is missing in sample table: {x}")
#            for y in sDf['SampleID']:
#                if y not in otSet:
#                    print(f"This sampleID is missing in OTU-table: {x}")
        
    
#
#len(chk["SampleID"].unique())
#len(oDf["SampleID"].unique())
#len(sDf['SampleID'])
#
#aX = "EY001F_101664" 
#bX=re.sub("EY[0-9]{3}[A-Z]{1}", "EY[0-9]{3}",aX)


#Read project data
#pPr=re.compile("[0-9]{6}_project\.csv$")
#pFile=re.search(pPr,files[0])
#pDf=pd.read_csv(pFile[0], sep=";", nrows=1)

#Store
#sDf.sort_values(by=["SampleID"], inplace=True)
#oDf.sort_values(by=["SampleID"], inplace=True)


#for subDir in os.listdir(os.getcwd()):
#    files=os.listdir(subDir)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#            print(sFile.head())


#for f in files:
#    if re.search(pSl,f):
#        sHit=re.search(pSl, f)
#        sFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+sHit[0])
#    if re.search(pOt, f):
#        oHit=re.search(pOt,f)
#        oFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+oHit[0])
#    if re.search(pPj, f):
#        pHit=re.search(pPj,f)
#        pFile=pd.read_csv(rootPth+"\\"+topFiles[0]+"\\"+pHit[0], sep=";", nrows=1)
#        
#print(pHit[0])
#print(sHit[0])
#print(oHit[0])

     


        


      
#for subDir in os.listdir(os.getcwd()):
#    files = os.listdir(subDir)
#    #time.sleep(2)
#    for f in files:
#        if re.search(pSl,f):
#            sHit=re.search(pSl, f)
#            sFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+sHit[0])
#        if re.search(pOt, f):
#            oHit=re.search(pOt,f)
#            oFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+oHit[0])
#        if re.search(pPj, f):
#            pHit=re.search(pPj,f)
#            pFile=pd.read_csv(rootPth+"\\"+subDir+"\\"+pHit[0], sep=";", nrows=1)
#        try:
#            if oFile is not None and pFile is not None and sFile is not None:
#                oID=oFile["SampleID"].str.match("^((?!Lab).)*$")
#                ngID=[not y for y in oID]
#                posDf=oFile[list(map(bool, thID))]
#                negDf=oFile[list(map(bool, ngID))]
#                print("Removed rows from OTU-table: ",negDf['SampleID'].unique())
#                spSet=set(sFile['SampleID'])
#                otSet=set(posDf['SampleID'])
#                for x in posDf['SampleID'].unique():
#                    if x not in spSet:
#                        print(f"This sampleID is missing in sample table: {x}")
#                for y in sDf['SampleID']:
#                    if y not in otSet:
#                        print(f"This sampleID is missing in OTU-table: {x}")
#                del(oFile)
#                del(pFile)
#                del(sFile)
#                print("Ehh what?")
#        except Exception as e:
#                continue
            