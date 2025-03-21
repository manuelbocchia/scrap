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
file_path = '/home/manuel/manu/scrap/coldplay_lyrics.csv'
## --- SET DATAFRAME
df_ori = pd.read_csv(file_path)

##--- Clean data from useless or repeated lyrics

con1 = df_ori['Lyrics'].str.contains('i[Remix]', regex= True) == False
con2 = df_ori['Lyrics'].str.contains('i[Live]', regex= True) == False
con3 = df_ori['Lyrics'].str.contains('i[Edit]', regex= True) == False
con4 = df_ori['Lyrics'].str.contains('.*\[.*\].*', regex= True) == False

df1 = df_ori[con4]
df2 = df1[con1]
df3 = df2[con2]
df = df3[con3]

## --- GET VALUES FROM FILE

my_songs = df.to_dict()


print(my_songs = df.to_dict())

## --- BASE WEBSITE URL
base_url = 'https://www.lyrics.com/'

headers = {
    #'Referer':'https://www.lyrics.com/lyrics/coldplay',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
## ---- Get number to loop range
nmb_of_songs = len(my_songs['Lyrics'])

## ---- Loop through the DF index to get each song

for x in range(0 , nmb_of_songs-1):
 
    the_song = (my_songs['Lyrics'][x], my_songs['URL'][x])
 ## ---- Initialize empty dict
    get_lyrics_url = defaultdict(str)
 ## ---- Run session and get song page
    my_session = requests.Session()
    try:
        my_request = my_session.get(base_url + the_song[1], headers=headers)

        print(f'{the_song[0]} downloaded.')
        my_soup = bs(my_request.text, features="html.parser")
        ## --- GET CONTENT FROM SOUP
        lyric_content = my_soup.find('pre', id="lyric-body-text")

        #pprint.pp(type(''.join(lyric_content.stripped_strings)))
        try:
            my_song_str = ''.join(lyric_content.stripped_strings)
            output_file = 'LYRICS/' + the_song[0] + '_LYRICS.txt'

            with open(output_file, 'w') as file:
                file.write(my_song_str)

            print(f'{the_song[0]} saved.')
        except:
            print(f'{the_song[0]} skipped.')
    except:
        print(f'Failed to download {the_song[0]}.')