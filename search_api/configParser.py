# -*- coding: utf-8 -*-

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
