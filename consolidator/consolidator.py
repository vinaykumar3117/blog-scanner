"""
Module      : consolidator.py
Description : Combine all txt files and convert to CSV
                - each paragraph becomes a separate row
Input       : List of pre-processed txt files (*_PPText.txt)
Ouput       : Consolidated csv file (*_PPText.csv)
"""

import glob
import csv
import os

class Consolidator:
    """
    Class to parse and consolidate csv data
    """

    def __init__(self, input_path):
        if input_path.find('..\\') == 0:
            import sys
            sys.path.insert(0, "..\\utils")
            from read_config import Configuration
            conf = Configuration()
        else:
            from utils.read_config import Configuration
            conf = Configuration('config\\configfile.conf')

        postfix = conf.get_attribute_value('startDate').replace('-', '') + conf.get_attribute_value('endDate').replace('-', '')

        self.input_path = input_path + postfix + "\\"
        self.csv_data = {}          # create data in dict {'KW_ID': 'Text content'} format
        self.csv_file_name = ''     # destination file

    def get_paragraphs_list(self, text):
        """
        Remove empty 'str' in the list
        """
        return list(filter(None, text.split('=======para=======')))

    def parse_preprocessed_txt_files(self):
        """
        Parse all pre-processed txt files and store contents in 'csv_data' dict
        """
        try:
            for in_file in glob.glob(self.input_path + '*_PPText.txt'):
                print('Processing file: {}'.format(in_file))
                kw_id = in_file.split('_')[1] +"_" + in_file.split('_')[2]
                with open(in_file, 'r', encoding="utf-8") as fp:
                    self.csv_data[kw_id] = self.get_paragraphs_list(fp.read())

            self.csv_file_name = in_file.split('_')[0] +"_" + in_file.split('_')[3]
            self.csv_file_name = self.csv_file_name.replace('.txt', '.csv')
            self.csv_file_name = self.csv_file_name.replace('pptext', 'pipe1_output')
        except IOError as ex:
            print(ex)

    def populate_csv(self):
        """
        Consolidate the 'csv_data' dict to single csv file
        """
        try:
            import shutil
            shutil.rmtree(os.path.dirname(self.csv_file_name))
        except FileNotFoundError:
            pass
        os.mkdir(os.path.dirname(self.csv_file_name))

        try:
            with open(self.csv_file_name, 'w', newline='', encoding="utf-8") as fp:
                fieldnames = ['ID', 'Text']
                writer = csv.DictWriter(fp, fieldnames=fieldnames)
                writer.writeheader()
                for key in self.csv_data.keys():
                    print('Migrating {} to csv'.format(key))
                    for para in self.csv_data[key]:
                        if para.strip():
                            writer.writerow({'ID': key, 'Text': para})
        except csv.Error as ex:
            print(ex)

def main(input_path='..\\dataset\\pptext\\'):
    consolidator = Consolidator(input_path)
    consolidator.parse_preprocessed_txt_files()
    consolidator.populate_csv()

if __name__ == '__main__':
    main()
