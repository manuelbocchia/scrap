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
import re

artist = 'Queen'
folder=f'LYRICS_{artist}'
list_of_songs = os.listdir(folder)

all_the_words = ''

#pprint.pp(list_of_songs)

for song in list_of_songs:
    song_path = f'{folder}/{song}'
    with open(song_path, 'r') as file:
        for line in file:
            all_the_words = all_the_words + ' ' + line

#song_words = defaultdict(list)

song_words = re.sub('[)(*,_-]*','',all_the_words).upper().split()



print(song_words)