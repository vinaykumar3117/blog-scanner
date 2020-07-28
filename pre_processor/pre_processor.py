"""
Module      : pre_processor.py
Description : Pre-process the blog contents
                - convert to lower case
                - remove stop words
                - lemmatize
                - stemming
Input       : Blog contents as txt file (*_Page.txt) per URL
Ouput       : Pre-processed txt file (*_PPText.txt) per URL
"""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer

import glob
import os

stop_words = set(stopwords.words('english'))

def trim(text):
    """
    Eliminate new lines
    """
    text = " ".join(text.splitlines())
    #print('\t trim -> {}\n'.format(text[:50]))
    return text

def to_lower(text):
    """
    Converting text to lower case
    Example,
            a. "Hello" -> "hello"
            b. "HELLO" -> "hello"
    """
    text = ' '.join([w.lower() for w in word_tokenize(text)])
    #print('\t to_lower -> {}\n'.format(text[:50]))
    return text

def remove_stop_words(text):
    """
    Removes stop words from 'text' and returns resultant string
    """
    words = text.split()
    text = ' '.join([word for word in words if not word in stop_words])
    #print('\t remove_stop_words -> {}\n'.format(text[:50]))
    return text

def lemmatize(text):
    """
    Lemmatize the text so as to get its root form
    Example:
            functions,funtionality as function
    Based on The Porter Stemming Algorithm
    """    
    wordnet_lemmatizer = WordNetLemmatizer()
    text = ' '.join([wordnet_lemmatizer.lemmatize(word) for word in word_tokenize(text)])
    #print('\t lemmatize -> {}\n'.format(text[:50]))
    return text

def stemming(text):
    """
    Reduces inflected or derived words to their word stem, base or root form
    Based on The Porter Stemming Algorithm
    """
    snowball_stemmer = SnowballStemmer('english')
    text = ' '.join([snowball_stemmer.stem(word) for word in word_tokenize(text)])
    #print('\t stemming -> {}\n'.format(text[:100]))
    return text

def main(input_path = '..\\dataset\\pages\\'):
    print("{:*^50s}".format(" Pre-processing started "))

    if input_path.find('..\\') == 0:
        import sys
        sys.path.insert(0, "..\\utils")
        from read_config import Configuration
        conf = Configuration()
    else:
        from utils.read_config import Configuration
        conf = Configuration('config\\configfile.conf')

    postfix = conf.get_attribute_value('startDate').replace('-', '') + conf.get_attribute_value('endDate').replace('-', '')
    input_path = input_path + postfix + "\\"
    output_path = input_path.replace('pages', 'pptext')

    try:
        import shutil
        shutil.rmtree(output_path)
    except FileNotFoundError:
        pass
    os.mkdir(output_path)

    for in_file in glob.glob(input_path + '*_Page.txt'):
        print('processing file: {}'.format(in_file))
        out_file = in_file.replace('pages', 'pptext').replace('_Page', '_PPText')
        with open(in_file, 'r', encoding="utf-8") as ifp:
            text = ifp.read()

            #print("\t input text -> {}\n".format(text[:50]))

            preprocessed_text = remove_stop_words(to_lower(trim(text)))
            
            """
            preprocessed_text = stemming(
                                        lemmatize(
                                                remove_stop_words(
                                                                to_lower(
                                                                        trim(text)
                                                                        ))))
            """

            #print("\t pre-processed text -> {}\n".format(preprocessed_text[:50]))

        with open(out_file, 'w', encoding='utf-8') as ofp:
            ofp.write(preprocessed_text)

    print("{:*^50s}".format(" Pre-processing done "))

if __name__ == '__main__':
    main()
