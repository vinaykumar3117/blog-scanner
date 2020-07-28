"""
Module      : batch_processor.py
Description : Utility module to batch process
"""

import csv

INPUT_FILE = '..\\dataset\\urls\\BS_URL.csv'
OUTPUT_PATH = '..\\dataset\\pages\\'

def parse_csv(input_file):
    """
    Parse CSV file
    """
    rows = []
    header = True
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if header:
                header = False
            else:
                rows.append(row)
    return rows

def url_master(input_file, output_path):
    """
    Batch process URL list
    """
    rows = parse_csv(input_file)
    for row in rows:
        url = row[2]
        output_file = output_path + 'BS_' + row[0] + '_' + row[1] + '_Page.txt'
        process_url(url, output_file)

def process_url(url, output_file):
    """
    Process URL using BeautifulSoup
    """
    print('{} -> {}'.format(url, output_file))

if __name__ == '__main__':
    url_master(INPUT_FILE, OUTPUT_PATH)
