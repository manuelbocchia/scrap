#import numpy as np
import pandas as pd
#import requests
#from bs4 import BeautifulSoup as bs
#from rauth import OAuth1Service
import pprint
#from collections import defaultdict
#import string
import json
import os
import re
import enchant

# Initialize the English dictionary for checking correct spelling of words
d = enchant.Dict("en_US")

artist = 'Queen'
folder=f'LYRICS_{artist}'
list_of_songs = os.listdir(folder)

all_the_words = ''


# Words to be removed so as to leave only content words, where possible
structural_words = [
    'A', 'AN', 'THE',  # Articles
    'AND', 'BUT', 'OR', 'NOR', 'FOR', 'SO', 'YET',  # Conjunctions
    'TO', 'IN', 'ON', 'AT', 'BY', 'WITH', 'ABOUT', 'AGAINST', 'BETWEEN', 'UNDER', 'OVER', 'THROUGH', 'DURING', 'BEFORE', 'AFTER',  # Prepositions
    'OF', 'AS', 'FROM', 'UP', 'DOWN', 'FOR', 'INTO', 'ONTO', 'UPON', 'OUT', 'ALONG', 'AROUND', 'BEHIND', 'IN FRONT OF', 'OUTSIDE', 'INSIDE', 'WITHIN', 'WITHOUT',  # More Prepositions
    'I', 'YOU', 'HE', 'SHE', 'IT', 'WE', 'THEY', 'ME', 'HIM', 'HER', 'US', 'THEM', 'MY', 'YOUR', 'HIS', 'HER', 'ITS', 'OUR', 'THEIR',  # Pronouns
    'AM', 'IS', 'ARE', 'WAS', 'WERE', 'BE', 'BEEN', 'BEING',  # Forms of the verb 'to be'
    'HAVE', 'HAS', 'HAD', 'HAVING',  # Forms of the verb 'to have'
    'DO', 'DOES', 'DID', 'DOING',  # Forms of the verb 'to do'
    'WILL', 'SHALL', 'WOULD', 'SHOULD', 'CAN', 'COULD', 'MAY', 'MIGHT', 'MUST', 'OUGHT', 'NEED', 'DARE',  # Modal verbs
    'NOT', 'NO', 'YES', 'THIS', 'THAT', 'THESE', 'THOSE', 'THERE', 'HERE', 'WHERE', 'WHEN', 'WHY', 'HOW', 'ALL', 'SOME', 'ANY', 'EACH', 'EVERY', 'FEW', 'MANY', 'MUCH', 'MOST', 'MORE', 'LESS', 'LEAST',  # Determiners, adverbs, question words
    'EITHER', 'NEITHER', 'BOTH', 'EACH', 'ANOTHER', 'SUCH', 'OTHER', 'ANOTHER',  # More determiners
    'IF', 'UNLESS', 'ALTHOUGH', 'BECAUSE', 'SINCE', 'WHILE', 'BEFORE', 'AFTER', 'UNTIL', 'WHETHER', 'AS', 'AS LONG AS', 'EVEN THOUGH', 'SO THAT', 'IN CASE', 'UNLESS', 'PROVIDED THAT',  # Subordinating conjunctions
    'EITHER', 'NEITHER',  # Correlative conjunctions
    'THAN', 'AS', 'LIKE',  # Comparative conjunctions
    'I\'M', 'YOU\'RE', 'HE\'S', 'SHE\'S', 'IT\'S', 'WE\'RE', 'THEY\'RE',  # Contractions of "to be"
    'I\'VE', 'YOU\'VE', 'HE\'S', 'SHE\'S', 'IT\'S', 'WE\'VE', 'THEY\'VE',  # Contractions of "have"
    'I\'D', 'YOU\'D', 'HE\'D', 'SHE\'D', 'IT\'D', 'WE\'D', 'THEY\'D',  # Contractions of "would" and "had"
    'I\'LL', 'YOU\'LL', 'HE\'LL', 'SHE\'LL', 'IT\'LL', 'WE\'LL', 'THEY\'LL',  # Contractions of "will"
    'ISN\'T', 'AREN\'T', 'WASN\'T', 'WEREN\'T', 'HASN\'T', 'HAVEN\'T', 'DON\'T', 'DOESN\'T', 'DIDN\'T', 'CAN\'T', 'COULDN\'T', 'MAYN\'T', 'MIGHTN\'T', 'MUSTN\'T', 'SHAN\'T', 'SHOULDN\'T',  # Negative contractions
    'I\'VE GOT', 'YOU\'VE GOT', 'HE\'S GOT', 'SHE\'S GOT', 'IT\'S GOT', 'WE\'VE GOT', 'THEY\'VE GOT',  # Got contractions
    'OH', 'OOH', 'YEAH','AH', 'HEY', "GONNA"
]

# read all song lyrics and get them on a variable, and split it into a list

for song in list_of_songs:
    song_path = f'{folder}/{song}'
    with open(song_path, 'r') as file:
        for line in file:
            all_the_words = all_the_words + ' ' + line

song_words = re.sub('[)(*,_-]*','',all_the_words).upper().split()

# Create a DataFrame, then drop all structural words, count the occurrence of the words, then drop the words which are misspelt
# and those words which are under 3 letters.

song_df = pd.DataFrame(song_words, index=None, columns=['Words'])

song_df.drop(song_df.query(f'Words in {structural_words}').index,inplace=True)

song_df_count = song_df['Words'].value_counts()

valid_words = [word for word in song_df_count.index if d.check(word) and len(word) > 2]

## your dictionary to make the word map

valid_word_count_dict = song_df_count[song_df_count.index.isin(valid_words)].to_dict()

#pprint.pp(valid_word_count_dict.items())

file_path = f'{folder}/Word_dictionary_{artist}.json'

# Write the dictionary to the JSON file
with open(file_path, 'w') as file:
    json.dump(valid_word_count_dict, file)

print(f"Dictionary saved to {file_path}")