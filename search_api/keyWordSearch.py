# -*- coding: utf-8 -*-
from googlesearch import search
from pandas import DataFrame
import re
import os

local_import = True

class keyWordSearch:
    
    def __init__(self, input_file, output_file):
        if local_import:
            self.configFile = "..\\config\\configfile.conf"
        else:
            self.configFile = ".\\config\\configfile.conf"
        self.inputFile = input_file
        self.keywordUrlFile=output_file
        self.urlList=[]
        self.keywordList=[]
        self.ignoreFileFormats=('.pdf','.doc','.docx','.xls')
        self.ignoredlinks=[]
        if local_import:
            import configParser
        else:
            import search_api.configParser as configParser
        self.noOfUrlsPerKeyword=int(configParser.configFileRead(self.configFile,'url','urlsPerKeyword'))
        
        
    #Function to do google search and get the web links
    def googleSearch(self):
        self.keywordList=self.getKeywords()
        #print(self.keywordList)
        
        for keyword in self.keywordList:
            keyIndex=1
            keyword=keyword.strip()
            # For all the keywords in the KeywordList.txt file perform the google query with dates search and get the web links
            print("Goooooooogling -> %s" % keyword)
            googleQuery=self.queryBuilder(keyword)
        
            for link in search(googleQuery,tld='com',num=10,stop=self.noOfUrlsPerKeyword,pause=2):
                #Check for links ends with file formats like .doc,.pdf etc
                if (link.endswith(self.ignoreFileFormats)):
                    self.ignoredlinks.append(link)
                    
                else:         
                #keyName=keyword+"_"+str(keyIndex)
                    self.urlList.append([keyword,keyIndex,link])
                    keyIndex=keyIndex+1
                
        if self.urlList != '':
            self.saveToUrlCsv()
    
    #Function to build google query with the gien dates    
    def queryBuilder(self,keyword):
        dateInterval=self.getDates()
        if len(dateInterval) != '':
            if dateInterval[0] != '':
                startDate=dateInterval[0]
            else:
                startDate=0
            if dateInterval[1] != '':
                endDate=dateInterval[1]
            else:
                endDate=0
        if startDate == 0 and endDate == 0:
            query=keyword
        elif startDate != 0 and endDate == 0:
            query= "{} after:{}".format(keyword,startDate)
        elif startDate == 0 and endDate !=0 :
            query= "{} before:{}".format(keyword,endDate)
        elif startDate != 0 and endDate !=0 :
            query= "{} after:{} before:{}".format(keyword,startDate,endDate)
        return query
        
    
    #Function to get the dates from the configuration file    
    def getDates(self):
        if local_import:
            import configParser
        else:
            import search_api.configParser as configParser
        startDate=configParser.configFileRead(self.configFile,'Date','startDate')
        endDate=configParser.configFileRead(self.configFile,'Date','endDate')
        return startDate,endDate
    
    #Function to get the keywords from the configuration file    
    def getKeywords(self):
        if local_import:
            import configParser
        else:
            import search_api.configParser as configParser
        with open(self.inputFile, 'r') as fp:
            keywords = fp.read()
        keywordList=keywords.split("\n")
        return keywordList
    
    #Function to save the google search weblinks results to .csv file.          
    def saveToUrlCsv(self):
        urlDataFrame=DataFrame(self.urlList)
        print (urlDataFrame)
        urlDataFrame.to_csv (self.keywordUrlFile, index = None, header=False)

def main(input_file = "..\\dataset\\keywords\\BS_KW.txt", output_path = "..\\dataset\\urls\\"):
    global local_import
    if input_file.find('..\\') == 0:
        local_import = True
        import sys
        sys.path.insert(0, "..\\utils")
        from read_config import Configuration
        conf = Configuration()
    else:
        local_import = False
        from utils.read_config import Configuration
        conf = Configuration('config\\configfile.conf')

    postfix = conf.get_attribute_value('startDate').replace('-', '') + conf.get_attribute_value('endDate').replace('-', '')
    output_file = output_path + postfix + "\\BS_URL.csv"

    try:
        import shutil
        shutil.rmtree(os.path.dirname(output_file))
    except FileNotFoundError:
        pass
    os.mkdir(os.path.dirname(output_file))

    keyword_Search=keyWordSearch(input_file, output_file)
    keyword_Search.googleSearch()
        
if __name__ == "__main__":
    main()
