from asyncio import wait
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from rauth import OAuth1Service
import pprint
from collections import defaultdict
import string
import json

## Enter your ARTIST
my_artist = 'Incomplete'

letter = my_artist[0].lower()

## --- OPEN FILE
file_path = f'/home/manuel/manu/scrap/artists_letter_{letter}.csv'

## --- SET DATAFRAME

df = pd.read_csv(file_path)

## --- GET VALUES FROM FILE

artist_url = df[df['Artists'] == my_artist]['URL'].values[0] 
artist_name = df[df['Artists'] == my_artist]['Artists'].values[0] 



## --- BASE WEBSITE URL
base_url = 'https://www.lyrics.com/'

##alphabet = list(string.ascii_lowercase)

#artist = 'https://www.lyrics.com/lyrics/radiohead'

## --- HEADERS FOR REQUESTS
headers = {
    #'Referer':'https://www.lyrics.com/lyrics/coldplay',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

## --- Set up for collecting songs
artist = my_artist.replace(" ", "_")

get_lyrics_url = defaultdict(str)
my_session = requests.Session()
my_request = my_session.get(base_url, headers=headers)
wait(5)
my_request = my_session.get(base_url + "artist/" + str(artist), headers=headers)
wait(5)
my_request = my_session.get(base_url + str(artist_url), headers=headers)

my_soup = bs(my_request.text, features="html.parser")
#print(my_soup)
## --- GET CONTENT FROM SOUP
content_body = my_soup.find('div', id='content-body')

## --- FIND ALL LINKS WHICH ARE LYRICS
lyric_links = content_body.find_all('a', href=lambda href: href and '/lyric/' in href)

## --- GET CONTENT FROM SOUP

get_lyrics_url = defaultdict(str)
for a in lyric_links:
    get_lyrics_url[a.text] = a['href']
    print(f"Lyrics {a.text} loaded.")

dataframe = pd.DataFrame(list(get_lyrics_url.items()), columns=["Lyrics", "URL"])

dataframe.to_csv(f'{artist_name}_lyrics.csv')

