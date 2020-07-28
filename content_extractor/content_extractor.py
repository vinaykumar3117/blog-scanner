"""
Module      : content_extractor.py
Description : Extract main text from news blog
Input       : List of keywords and url (csv file)
Ouput       : Blog contents as txt file (*_Page.txt) per URL
"""

import csv
import os

local_import = True

class ContentExtractor:
    """
    Batch processor class
    """
    def __init__(self, input_file, output_path):
        self.source = input_file
        self.processed_file = input_file.replace('.csv', '_Processed.csv')
        if (os.path.exists(self.processed_file)):
            self.source = self.processed_file
        self.output_path = output_path
        self.rows = []

    def read_csv(self):
        """
        Read from CSV
        """
        with open(self.source, 'r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.rows.append(row)

    def write_csv(self):
        """
        Write to CSV
        """
        with open(self.processed_file, 'w', newline='', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.rows)

    def url_master(self):
        """
        Batch process URL list
        """
        self.read_csv()
        if not self.rows or len(self.rows[0]) < 1:
            print('No URLs to process..!')
            return

        if local_import:
            import sys
            sys.path.insert(0, "..\\utils")
            from read_config import Configuration
            conf = Configuration()
        else:
            from utils.read_config import Configuration
            conf = Configuration('config\\configfile.conf')

        postfix = conf.get_attribute_value('startDate').replace('-', '') + conf.get_attribute_value('endDate').replace('-', '')
        self.output_path = self.output_path + postfix + "\\"
        
        try:
            import shutil
            shutil.rmtree(self.output_path)
        except FileNotFoundError:
            pass
        os.mkdir(self.output_path)
        
        processed = False
        for row in self.rows:
            if (len(row) == 3 or (len(row) == 4 and row[3] != 'PROCESSED')):
                url = row[2]
                output_file = self.output_path + 'BS_' + row[0] + '_' + row[1] + '_Page.txt'
                self.process_url(url, output_file)
                row.append('PROCESSED')
                processed = True

        if processed:
            self.write_csv()
        else:
            print('All URLs processed.')

    def process_url(self, url, output_file):
        """
        Process URL using BeautifulSoup
        """
        if local_import:
            from extract_blog_contents import ExtractContents
        else:
            from content_extractor.extract_blog_contents import ExtractContents
        print('Scrapping URL -> {}'.format(url))
        ExtractContents(url, output_file)

def main(input_path='..\\dataset\\urls\\', output_path='..\\dataset\\pages\\'):
    try:
        global local_import
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
        input_file = input_path + postfix + "\\BS_URL.csv"
        
        content_extractor = ContentExtractor(input_file, output_path)
        content_extractor.url_master()
    except Exception as ex:
        print('Caught exception: {}'.format(ex))
        content_extractor.write_csv()

if __name__ == '__main__':
    main()
