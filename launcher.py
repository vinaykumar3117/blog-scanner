"""
Module      : launcher.py
Description : Launcher for Blog Scanner
"""

import sys
import os
import timeit

usage = '''
*************************** Welcome to ***************************
    ____  __               _____                                 
   / __ )/ /___  ____ _   / ___/_________ _____  ____  ___  _____
  / __  / / __ \/ __ `/   \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / /_/ / / /_/ / /_/ /   ___/ / /__/ /_/ / / / / / / /  __/ /    
/_____/_/\____/\__, /   /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
              /____/                                             

Scan news blogs for interesting text using machine learning. 

Press one of the options below to execute, 
1. Google Search
2. Blog extractor
3. Pre-processor
4. Consolidator
5. Post-processor
6. Tagging
7. Do All
8. Clear cache
0. Exit

******************************************************************
'''

def print_header(string):
    print("{} {}\n".format("########## ", string))

def search_api():
    print_header("Performing google search..")
    from search_api.keyWordSearch import main
    start_time = timeit.default_timer()
    main(input_file = ".\\dataset\\keywords\\BS_KW.txt", output_path = ".\\dataset\\urls\\")
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def content_extractor():
    print_header("Extracting blog contents.. This might take sometime. Please be patient.")
    from content_extractor.content_extractor import main
    start_time = timeit.default_timer()
    main(input_path = '.\\dataset\\urls\\', output_path = '.\\dataset\\pages\\')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def pre_processor():
    print_header("Pre-processing text.. This might take sometime. Please be patient.")
    from pre_processor.pre_processor import main
    start_time = timeit.default_timer()
    main(input_path = '.\\dataset\\pages\\')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def post_processor():
    print_header("Post-processing text.. This might take sometime. Please be patient.")
    from post_processor.post_processor import main
    start_time = timeit.default_timer()
    main(input_path = '.\\dataset\\pipe1_output\\', output_path = '.\\dataset\\pipe2_output\\')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def consolidator():
    print_header("Consolidating texts..")
    from consolidator.consolidator import main
    start_time = timeit.default_timer()
    main(input_path = '.\\dataset\\pptext\\')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def tagging():
    print_header("Prepare training data..")
    from tagging.tagging import main
    start_time = timeit.default_timer()
    main(input_path='.\\dataset\\pipe2_output\\', output_path='.\\dataset\\tagged\\')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def do_all():
    print_header("Framing training data..")
    start_time = timeit.default_timer()
    search_api()
    content_extractor()
    pre_processor()
    consolidator()
    post_processor()
    tagging()
    print("Total time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def clear_cache():
    print_header("Cleaning up training data..")
    from utils.cache_clear import main
    start_time = timeit.default_timer()
    main(dataset_path='.\\dataset')
    print("Time elapsed: %3.3fs" % (timeit.default_timer() - start_time))

def terminate():
    print_header("Terminating the process.")
    sys.exit(0)

switcher = {
                1: search_api, 
                2: content_extractor, 
                3: pre_processor, 
                4: consolidator, 
                5: post_processor, 
                6: tagging, 
                7: do_all, 
                8: clear_cache, 
                0: terminate
            }

while True:
    print(usage)
    option = int(input("Enter your option: "))
    func = switcher.get(option, lambda: print("Invalid option!!! - Retry"))
    func()
