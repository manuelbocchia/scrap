import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from rauth import OAuth1Service
import pprint
from collections import defaultdict
import string
import json
## --- OPEN FILE
file_path = '/home/manuel/manu/scrap/artists_letter_c.csv'
## --- SET DATAFRAME
df = pd.read_csv(file_path)

## --- GET VALUES FROM FILE

coldplay_url = df[df['Artists'] == 'Coldplay']['URL'].values[0] 
coldplay_name = df[df['Artists'] == 'Coldplay']['Artists'].values[0] 

## --- BASE WEBSITE URL
base_url = 'https://www.lyrics.com/'

##alphabet = list(string.ascii_lowercase)

coldplay = 'https://www.lyrics.com/lyrics/coldplay'

## --- HEADERS FOR REQUESTS
headers = {
    #'Referer':'https://www.lyrics.com/lyrics/coldplay',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

## --- Set up for collecting songs

get_lyrics_url = defaultdict(str)
my_session = requests.Session()
my_request = my_session.get(coldplay, headers=headers)
#my_request = my_session.get(base_url + str(coldplay_url), headers=headers)
my_request = my_session.get('https://www.lyrics.com/artist/Coldplay/435023', headers=headers)
my_soup = bs(my_request.text, features="html.parser")
## --- GET CONTENT FROM SOUP
content_body = my_soup.find('div', id='content-body')
lyric_links = content_body.find_all('a', href=lambda href: href and '/lyric/' in href)

## --- FIND ALL LINKS WHICH ARE LYRICS
#lyric_links_2 = filter(lambda x : 'lyric' in x['href'], lyric_links)
#pprint.pp(list(lyric_links))


## --- GET CONTENT FROM SOUP

get_lyrics_url = defaultdict(str)
for a in lyric_links:
    get_lyrics_url[a.text] = a['href']
    print(f"Lyrics {a.text} loaded.")
    dataframe = pd.DataFrame(list(get_lyrics_url.items()), columns=["Lyrics", "URL"])
#pprint.pp(get_lyrics_url)
    dataframe.to_csv(f'coldplay_lyrics.csv')

#for a in lyric_links:
#        get_lyrics_url[a.text] = a['href']
#        print(f"Song {a.text} loaded.")
#dataframe = pd.DataFrame(list(get_lyrics_url.items()), columns=["Artists", "URL"], index=False)

#print(lyric_links)

