import requests
from bs4 import BeautifulSoup as BS
from dotenv import dotenv_values

config = dotenv_values(".env")



def getVizTitleInfo(title):
    if ',' in title:
        title = title.split(',')
    else:
        title = [title,title]
    ret = []
    series = ""
    
    for s in title[0].split():
        if not s.isdigit():
            series = series +  " " +str(s)
    
    series = series.replace("volume",'')
    series = series.replace("Volume",'')
    

    volNum = None
    for s in title[1].split():
        if s.isdigit():
            volNum  = s
    
    return (series,volNum)

#get Volume info from isbn
def getVolume(isbns:int):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbns}')
    #print(res.json())

    if res.status_code != 200:
        raise Exception("Request for this isbn could not be fulfilled!")

    ret = {}
    rj = res.json()
    if rj["totalItems"] == 0:
        raise Exception("Request for this isbn could not be fulfilled!")

    info = rj["items"][0]["volumeInfo"]
    google_link = rj["items"][0]['selfLink']
    
    pub = info["publisher"]
    #Extract name and volume number 

    #TODO: title section sometimes just contains the title and no vol number
    title: str = info['title']
    series, volume = None, None
    if 'Omnibus'in title:
            print(title)
    else:
        (series,volume) = getVizTitleInfo(title)
    
    author = info['authors'][0]
    image = None
    if 'imageLinks' in info :
        image = info['imageLinks']["thumbnail"]
    book = {}
    book["link"] = google_link
    book["series"] = series
    book["volume"] = volume
    book["author"] = author
    book["image"] = image
    return book 

book = getVolume(1974709930)
print(book)