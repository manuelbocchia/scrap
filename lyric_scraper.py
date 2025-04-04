import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from rauth import OAuth1Service
import pprint
from collections import defaultdict
import string
import json

base_url = 'https://www.lyrics.com'

# option a) whole alphabet
#alphabet = list(string.ascii_lowercase)
# option b) one artist
alphabet = 'q'

headers = {
    #'Accept':'*/*',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

#get_artists_url = defaultdict(str)


#for x in alphabet:
#    my_request = requests.get(base_url + '/artists/' + x + '/99999', headers=headers)
#    my_soup = bs(my_request.text, features="html.parser")
#    content_body = my_soup.find('div', id='content-body')
#    artist_links = content_body.find_all('a')
#    #print(f'Artist list for letter: /" {x} /" scraped')
#    for a in artist_links:
#        get_artists_url[a.text] = a['href']
#        #print(f"Artist {a.text} loaded.")

#artists_url_df = pd.DataFrame.from_dict(get_artists_url)

#artists_url_df.to_csv('my_file.csv')

def get_artists(a):
    get_artists_url = defaultdict(str)
    my_request = requests.get(base_url + '/artists/' + a + '/99999', headers=headers)
    my_soup = bs(my_request.text, features="html.parser")
    content_body = my_soup.find('div', id='content-body')
    artist_links = content_body.find_all('a')
    print(f'Artist list for letter: /" {a} /" scraped')
    for a in artist_links:
        get_artists_url[a.text] = a['href']
        print(f"Artist {a.text} loaded.")
    dataframe = pd.DataFrame(list(get_artists_url.items()), columns=["Artists", "URL"])
    return dataframe

for x in alphabet:
    get_artists(x).to_csv(f'artists_letter_{x}.csv')


