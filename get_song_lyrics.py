import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from rauth import OAuth1Service
import pprint
from collections import defaultdict
import string
import json
import os
## --- OPEN FILE
artist = 'Queen'
folder=f'LYRICS_{artist}'
os.makedirs(folder,exist_ok=True)
file_path = f'/home/manuel/manu/scrap/{artist}_lyrics.csv'
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

number_songs = list(my_songs['Unnamed: 0'].keys())

#print(my_songs = df.to_dict())

## --- BASE WEBSITE URL
base_url = 'https://www.lyrics.com/'

headers = {
    #'Referer':'https://www.lyrics.com/lyrics/coldplay',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
## ---- Get number to loop range
nmb_of_songs = len(number_songs)

print(f'working on {nmb_of_songs} songs')
## ---- Loop through the DF index to get each song

#with open('radiohead_songs_dictionary.txt', 'w') as file:
#    for x, y in my_songs.items():
#        file.write(f"{x} in {y}\n")
#
#pprint.pp(my_songs)


for x in number_songs:
    print(f'Song {x}:')
    try:
        the_song = (my_songs['Lyrics'][x], my_songs['URL'][x])
 ##     ---- Initialize empty dict
        get_lyrics_url = defaultdict(str)
 ##     ---- Run session and get song page
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
                output_file = f'LYRICS_{artist}/' + the_song[0] + '_LYRICS.txt'

                with open(output_file, 'w') as file:
                    file.write(my_song_str)

                print(f'{the_song[0]} saved.')
            except Exception as e:
                print(f'{the_song[0]} skipped because of {e}.')
        except:
            print(f'Failed to download {the_song[0]}.')
    except Exception as e:
        print(f'Skipping number {x} because of {e}.')
        pass