"""
Module      : post_processor.py
Description : eliminate blacklisted words, append URL column
Input       : pipe1_output (csv file)
Ouput       : pipe2_output (csv file)
"""

import csv
import os

local_import = True
postfix = ''
MIN_CHAR_COUNT = 19

def get_blacklist():
    """
    Get blacklist words
    """
    global local_import
    if local_import:
        blacklist_file = '..\\config\\blacklist.txt'
    else:
        blacklist_file = '.\config\\blacklist.txt'
    
    blacklist = []
    with open(blacklist_file, 'r', encoding="utf-8") as fd:
        blacklist = fd.read().splitlines()
    return blacklist

def read_csv(input_file):
    """
    Read from CSV
    """
    rows = []
    with open(input_file, 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            rows.append(row)
    return rows

def write_csv(data, output_file):
    """
    Write to CSV
    """
    try:
        import shutil
        shutil.rmtree(os.path.dirname(output_file))
    except FileNotFoundError:
        pass
    os.mkdir(os.path.dirname(output_file))
    
    print("Writing post-processed data -> {}".format(output_file))
    with open(output_file, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

def remove_blacklist(data):
    """
    Remove blacklisted words
    """
    print("Eliminating blacklist words..")
    blacklist = get_blacklist()
    temp_data = []
    for d in data:
        text = d[1].strip()
        if len(text) > MIN_CHAR_COUNT and (text not in blacklist):
            temp_data.append([d[0], text])
    return temp_data

def append_url(data):
    """
    Read from CSV
    """
    print("Appending URLs...")
    global postfix
    urls = []
    if local_import:
        url_file = '..\\dataset\\urls\\'
    else:
        url_file = '.\\dataset\\urls\\'

    url_file = url_file + postfix + "\\BS_URL.csv"
    urls = read_csv(url_file)
    temp_data = []
    temp_data.append(['ID', 'Text', 'URL'])
    for d in data:
        for url in urls:
            pattern = url[0] + '_' + url[1]
            if d[0] == pattern:
                temp_data.append([d[0], d[1], url[2]])
    return temp_data

def post_process(input_file, output_file):
    """
    Post process data
    """
    print("************* Post-processing started *************")
    data = read_csv(input_file)
    data = remove_blacklist(data)        
    data = append_url(data)
    write_csv(data, output_file)
    print("************* Post-processing done *************")

def main(input_path='..\\dataset\\pipe1_output\\', output_path='..\\dataset\\pipe2_output\\'):
    try:
        global local_import
        global postfix
        if input_path.find('..\\') == 0:
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
        input_file = input_path + postfix + "\\BS_PPText.csv"
        output_file = output_path + postfix + "\\BS_PPText.csv"
        
        post_process(input_file, output_file)
    except Exception as ex:
        print('Caught exception: {}'.format(ex))

if __name__ == '__main__':
    main()
