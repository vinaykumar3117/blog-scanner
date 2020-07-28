"""
Module      : read_config.py
Description : Utility module to read configuration
Author      : vinay.k.g@nokia.com
"""

class Configuration:
    conf_dic = {}
    
    def __init__(self, conf_file='..\\config\\configfile.conf'):
        conf_list = []
        with open(conf_file, 'r') as fp:
            conf_list = fp.readlines()
            
        for item in conf_list:
            val = item.strip()
            if not val.startswith('['):
                self.conf_dic[val.split('=')[0]] = val.split('=')[1]

    def get_attribute_value(self, attribute=''):
        if attribute:
            try:
                return self.conf_dic[attribute]
            except KeyError:
                return ''
        return ''

    def get_attributes_dic(self):
        return self.conf_dic
