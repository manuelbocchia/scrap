import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from rauth import OAuth1Service
import pprint

#genius = OAuth1Service(
#    name='genius',
#    consumer_key='',
#    consumer_secret='XTeGTX5qpEvcKGqV0mX88arcLgJlN5Mtq5kMRKllylutjBrqhDDdqrpu3rslY1IQmP_406ek2fJnj3RW63PGEw',
#    request_token_url='https://api.genius.com/oauth/authorize',
#    access_token_url='',
#    authorize_url='',
#    base_url=''
#)
#
#request = OAuth1Service(
#    client_id='ujqLOvkNBktXib3aLDW8voJVslcF9gmX-ryOU4r-yjLusGYeIhOhukh-tMLN735S',
#    redirect_uri='',
#    scope='GET /account',
#    state='',
#    response_type='code'
#)

# FOR GENIUS API
#client_id: ujqLOvkNBktXib3aLDW8voJVslcF9gmX-ryOU4r-yjLusGYeIhOhukh-tMLN735S
#token: XTeGTX5qpEvcKGqV0mX88arcLgJlN5Mtq5kMRKllylutjBrqhDDdqrpu3rslY1IQmP_406ek2fJnj3RW63PGEw

GENIUS_API_TOKEN='FxLc6cZq23mJK5zCWS62zCQj6CgkCN_b64E3gBZF6g-AeJexAnefmLxQ7OwB1VbP'


# Base URL for the Genius API
base_url = 'https://api.genius.com'

content_to_get = '/songs/378195'

# Authorization header with the Genius API token (replace GENIUS_API_TOKEN with your actual token)
headers1 = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}

my_request = requests.get(base_url + content_to_get, headers=headers1)

json = my_request.json()

json_df = pd.read_json(my_request.text)

json_df.to_json('/home/manuel/manu/my_song.json')

#pprint.pp(json)

#pprint.pp(my_request.content)

#soup = bs(html_doc, 'json.parser')

#print(soup.prettify())
