from urllib.request import urlopen

print('start')
fp = urlopen("https://www.python.org/")
data = fp.read()
html_doc = data.decode()
fp.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.title.string)
#for link in soup.find_all('a'):
#    print(link.get('href'))
print(soup.get_text())
print('end')