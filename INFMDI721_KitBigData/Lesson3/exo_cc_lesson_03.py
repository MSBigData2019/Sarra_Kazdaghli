import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json


def get_soup_from_url(url):
    page = requests.get(url);
    if (page.status_code == 200):
        return BeautifulSoup(page.content, 'html.parser')
    else:
        return None


url = 'https://www.insee.fr/fr/statistiques/1906659?sommaire=1906743'
soup = get_soup_from_url(url)
villes = soup.find(id='produit-tableau-T16F014T4')
if villes:
    df = pd.read_html(str(villes))[0]
    print(df.head())

# enter your api key here
api_key = 'AIzaSyAtnNffeavyAuEHW5k8ThcwvFvinsrNB_8'

url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

urls = url + 'origins= {} &destinations= {} &key=' + api_key
villes = '|'.join(df['Commune'].values)
print(villes)
url_formatted = urls.format(villes, villes)
print(url_formatted)

pageAPI = requests.get(url_formatted)
if pageAPI.status_code:
    res = pageAPI.json()
    print(res)
