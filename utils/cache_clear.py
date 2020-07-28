"""
Module      : cache_clear.py
Description : Clear training data cache
Input       : dataset path
Author      : vinay.k.g@nokia.com
"""

def main(dataset_path='..\\dataset'):
    """
    Clear training data
    """
    dataset = ['urls', 'pages', 'pptext', 'pipe1_output', 'tagged']
    
    try:
        if dataset_path.find('..\\') == 0:
            import sys
            sys.path.insert(0, "..\\utils")
            from read_config import Configuration
            conf = Configuration()
        else:
            from utils.read_config import Configuration
            conf = Configuration('config\\configfile.conf')

        postfix = conf.get_attribute_value('startDate').replace('-', '') + conf.get_attribute_value('endDate').replace('-', '')

        for data in dataset:
            cache = dataset_path + '\\' + data + '\\' + postfix
            try:
                import shutil
                print("Clearing {}".format(cache))
                shutil.rmtree(cache)
            except FileNotFoundError:
                pass            
        
    except Exception as ex:
        print('Caught exception: {}'.format(ex))

if __name__ == '__main__':
    main()
