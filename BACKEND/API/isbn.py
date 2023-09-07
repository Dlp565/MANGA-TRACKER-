import requests
from bs4 import BeautifulSoup as BS
from dotenv import dotenv_values

config = dotenv_values(".env")


def getVizTitleInfo(title):
    title = title.split(',')
    series = title[0]
    print(series)
    volNum = None
    for s in title[1].split():
        if s.isdigit():
            volNum  = s
    print(volNum)

#get Volume info from isbn
def getVolume(isbns:int):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbns}')
    #print(res.json())
    rj = res.json()
    info = rj["items"][0]["volumeInfo"]
    print(rj["items"][0]['selfLink'])
    
    pub = info["publisher"]
    print(pub)
    #Extract name and volume number 
    title = info['title']
    if pub == "VIZ Media LLC":
        if title.contains('Omnibus'):
            print(title)
        else:
            getVizTitleInfo(title)
    else:
        print(title)
    print(info['authors'][0])
    print(info['imageLinks']["thumbnail"])
    
    


getVolume(9781612629612)