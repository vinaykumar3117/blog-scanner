"""
Module      : tagging.py
Description : Tag relevant texts
Input       : post processed file (csv file)
Ouput       : tagged file (csv file)
"""

import csv
import os

local_import = True
postfix = ''

def get_tags():
    """
    Get tags
    """
    global local_import
    if local_import:
        tag_file = '..\\config\\tags.txt'
    else:
        tag_file = '.\config\\tags.txt'
    
    tags = []
    with open(tag_file, 'r', encoding="utf-8") as fd:
        tags = fd.read().lower().splitlines()
    return tags

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
    
    print("Writing tagged data -> {}".format(output_file))
    with open(output_file, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

def tagit(input_file, output_file):
    """
    Tag relevant text
    """
    tags = get_tags()
    data = read_csv(input_file)
    temp_data = []
    
    for d in data:
        if d[0] == 'ID':
            temp_data.append([d[0], d[1], d[2], 'Tag'])
            continue

        for tag in tags:
            if d[1].find(tag) == 0:
                temp_data.append([d[0], d[1], d[2], 'Ok'])
                break
        else:
            temp_data.append([d[0], d[1], d[2], 'Not Ok'])

    write_csv(temp_data, output_file)

def main(input_path='..\\dataset\\pipe2_output\\', output_path='..\\dataset\\tagged\\'):
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
        output_file = output_path + postfix + "\\BS_Tagged.csv"
        
        tagit(input_file, output_file)
    except Exception as ex:
        print('Caught exception: {}'.format(ex))

if __name__ == '__main__':
    main()
