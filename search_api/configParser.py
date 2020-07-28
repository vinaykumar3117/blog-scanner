# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 09:17:08 2019

"""
import configparser
def configFileRead(fileName,section,option):
    configFile = configparser.ConfigParser()
    configFile.read(fileName)
    optionValue = configFile.get(section, option)
    return optionValue
def configFileWrite(fileName,section,option,parameterValue):
    configFile=configparser.ConfigParser()
    configFile.read(fileName)
    configFile.set(section,option,parameterValue)
    with open(fileName , 'w') as configFileOpen :
        configFile.write(configFileOpen)
        return 1
