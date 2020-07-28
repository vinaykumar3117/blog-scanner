# Blog Scanner

Scan news blogs for interesting text using machine learning. 

_1. Google Search - Automated search based on keyword and time frame_
<br />
_2. Extract main text from news blog - Convert HTML to relevant text portion_
<br />
_3. Preprocess the text - convert to lowercase, removes stop-words from txt content, lemma and stemming (optional)_
<br />
_4. Consolidator - Combine all txt files and convert to CSV_
<br />
_5. Postprocess the text - Eliminate blacklisted words_
<br />
_6. Prepare Training data (auto-tagging of paragraphs)_

<br />

| ___Modules___ | ___Input___ | ___Output___ |
| :--- | :--- | :--- |
| __search_api__ | keyword list (BS_KW.txt) + time frame (config) | URL list (BS_URL.csv) |
| __content_extractor__ | URL list (BS_URL.csv) | Text files (BS_KW1_ID1_Page.txt one per URL) |
| __pre_processor__ | Text files (BS_KW1_ID1_Page.txt one per URL) | Text files (BS_KW1_ID1_PPText.txt one per URL)|
| __consolidator__ | Text files (BS_KW1_ID1_PPText.txt one per URL) | Single CSV file (BS_PPText.csv) |
| __post_processor__ | Single CSV file (pipe1 - BS_PPText.csv) | Single CSV file (pipe2 - BS_PPText.csv)|
| __tagging__ | Single CSV file (BS_PPText.csv) | Single CSV file (BS_Tagged.csv) |
<br />

### Datasets:
```
 > keywords -I/P from user; Keyword list + Time window
 > urls - O/P from google search; URL list
 > pages - O/P from blog extractor; Txt files - one per URL
 > pptext - O/P from pre-processor; Txt files - one per URL
 > pipe1_output - O/P from consolidator; Single CSV file
 > pipe2_output - O/P from post-processor; Single CSV file
 > tagged - O/P from tagging; Single CSV file
```

### Input:
###### User keywords - `blog-scanner / dataset / keywords / BS_KW.txt` <br />
_e.g._ Line seperated queries <br />
`Resistor shortage` <br />
`Capacitor shortage` <br />

### Configurations:
###### Configure search parameters - `blog-scanner / config / configfile.conf` <br />
_e.g._ Search ___10___ URLs per keyword for the ___October___ month <br />
`urlsPerKeyword=10` <br />
`startDate=2019-10-01` <br />
`endDate=2019-10-31` <br />

###### Blacklisted words - `blog-scanner / config / blacklist.txt` <br />
_e.g._ <br />
`login` <br />
`tweet` <br />
`facebook` <br />

###### Tags - `blog-scanner / config / tags.txt` <br />
_e.g._ <br />
`Shortage` <br />
`Supply constraints` <br />
`Capacity` <br />

### Output:
###### End training data - `blog-scanner / dataset / tagged / 2019100120191031 / BS_Tagged.csv` <br />
_e.g._ Sample o/p <br />
`ID,Text,URL,Tag` <br />
`Capacitor shortage_1, shortage tiny capacitors..., https://www..., Ok` <br />
`Capacitor shortage_1, /marketintelligence/..., https://www..., Not Ok` <br />

### Usage: 
> Execute `launcher.py` python module

```
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

Enter your option: 
```

### References:
###### Beautiful Soup
 :link: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ <br />
 :link: https://www.dataquest.io/blog/web-scraping-beautifulsoup/ <br />

###### Google Search
 :link: https://github.com/MarioVilas/googlesearch <br />
 :link: https://www.geeksforgeeks.org/performing-google-search-using-python-code/ <br />

###### Pre-processing
 :link: https://medium.com/@pemagrg/pre-processing-text-in-python-ad13ea544dae <br />
 :link: https://www.nltk.org/data.html <br />
 :link: https://pypi.org/project/stop-words/ <br />
