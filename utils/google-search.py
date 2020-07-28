from googlesearch import search

query = "python"
for link in search(query, tld='co.in', num=10, stop=5, pause=2):
    print(link)
