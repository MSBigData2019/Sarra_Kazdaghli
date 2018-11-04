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
api_key = 'AIzaSyCgW3B5fFOPrztmBmHZOeZc0dmlmrsLCq0'

url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

urls = url + '&origins={}&destinations={}&key=' + api_key
villes = '|'.join(df['Commune'].values[:10])

url_formatted = urls.format(villes, villes)
print(url_formatted)

pageAPI = requests.get(url_formatted)
if pageAPI.status_code:
    res = pageAPI.json()

df_matrix = pd.DataFrame(index=np.arange(10), columns=np.arange(10))
i = 0
for row in res['rows']:
    elements = row['elements']
    j = 0
    for element in elements:
        status = element['status']
        if status == 'OK':
            distance = element['distance']['text']
        else:
            distance = 'NaN'
        df_matrix[i][j] = distance
        j = j + 1
    i = i + 1

df_matrix = df_matrix.rename(lambda x: df['Commune'].values[int(x)], axis=1)
df_matrix = df_matrix.rename(lambda x: df['Commune'].values[int(x)], axis=0)
print(df_matrix.head())
