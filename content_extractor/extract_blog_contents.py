# -*- coding: utf-8 -*-
"""
Module      : extract_blog_content.py
Description : Extract main text from news blog
Input       : link, filename
Ouput       : Extracted data is saved in file 'filename'

"""

import requests
from bs4 import BeautifulSoup, Comment
import re

class ExtractContents():
    def __init__(self, link , filename ):
        self.link=link
        self.filename=filename
        self.createSoup()
        
    def traverse(self,soup):
        if soup.name is not None:
            dom_dictionary = {}
            dom_dictionary['name'] = soup.name
            dom_dictionary['children'] = [ self.traverse(child) for child in soup.children if child.name is not None]
        return dom_dictionary
        
    def createSoup(self):

        f = requests.get(self.link).text
        soup = BeautifulSoup(f, "lxml")

        #Remove all photos
        formatters=[ "img", "audio",'footer','header','noscript','picture']
        for formats in soup.find_all(formatters):
            formats.extract()
     
        # kill all script 
        for script in soup.find_all(["script", "style"]):
            script.decompose()
        
        # remove comments
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
     
        # replace all references with the link address as text
        all_a = soup.findAll('a')
        for a in all_a:    
            tag = soup.new_tag("p")
            try:
                #href = a['href']
                a_text=a.get_text()
                tag.string = a_text #+ " (" + href +  ") "
                a.insert_after(tag)
            except:
                pass
            a.extract()
            
        # get text
        text = soup.get_text()
        
        # remove extra lines
        text = re.sub(r'(\n*)+\n+', '\n=======Para=======\n', text)
        file=open(self.filename,'a', encoding="utf-8")
        file.writelines(text)
        file.close() 

