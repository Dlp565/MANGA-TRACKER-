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
    series = series.replace("vol",'')
    series = series.strip()
    print(series)
    volNum = None
    for s in title[1].split():
        if s.isdigit():
            volNum  = s
    
    return (series,volNum)

def processVolume(results):
        info = results["volumeInfo"]
        google_link = None
        if 'selfLink' in results:
            google_link = results['selfLink']

        #print(info.keys())


        #pub = info["publisher"]
        #Extract name and volume number 

        #TODO: title section sometimes just contains the title and no vol number
        title: str = info['title']
        series, volume = None, None
        # if 'Omnibus'in title:
        #         print(title)
        # else:
        (series,volume) = getVizTitleInfo(title)
        author = ""
        
        if 'authors' in info:
            author = info['authors'][0]
        
        image = ""
        if 'imageLinks' in info :
            image = info['imageLinks']["thumbnail"]
        isbn = None
        if "industryIdentifiers" in info:
            isbn = info["industryIdentifiers"][0]['identifier']

        language = ""
        if 'language' in info:
            language = info['language']
        book = {}
        book["link"] = google_link
        book["series"] = series
        book["volume"] = volume
        book["author"] = author
        book["image"] = image
        book['isbn'] = isbn
        book['language'] = language
        return book 


        

#get Volume info from isbn
def getVolume(isbns:int):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbns}')
    #print(res.json())

    if res.status_code != 200:
        raise Exception("Request for this isbn could not be fulfilled!")

    rj = res.json()
    if rj["totalItems"] == 0:
        raise Exception("Request for this isbn could not be fulfilled!")
    ret = {}
    
    for i in range (0,len(rj["items"])):
        ret[i] = processVolume(rj["items"][i])
    
    return ret

def getVolumeName(name: str):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{name}')
    if res.status_code != 200:
        raise Exception("Request for this name could not be fulfilled!")

    rj = res.json()
    if rj["totalItems"] == 0:
        raise Exception("Request for this name could not be fulfilled!")
    ret = {}
    count = 0
    for i in range (0,len(rj["items"])):
        ret[i] = processVolume(rj["items"][i])
        count += 1
    return (ret,count)

def getLink(link: str):
   res = requests.get(link) 
   print(res.json())


def getSeries(series: str):
    query = '''
    query ($search: String) {
        Media (search: $search, type: MANGA) {
            id
            title {
                romaji
                english native
            }
            coverImage {
                extraLarge
            }
            genres
            popularity
        }
    }
    '''

    variables = {
        'search' : series
    }

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json = {'query':query, 'variables': variables})
    res = response.json()
    if 'errors' in res:
        raise Exception("Manga not found")
    return res
