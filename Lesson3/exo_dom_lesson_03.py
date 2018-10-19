import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json


def get_users():
    url = 'https://gist.github.com/paulmillr/2657075'
    page = requests.get(url)
    users = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        readme = soup.find(id='readme')
        if (readme):
            table = readme.find('table')
            if (table):
                df = pd.read_html(str(table))[0]
                df['Stars'] = pd.Series(0, index=df.index)
                print(df.head())

        return df


def get_stars(user):
    token = 'beaef5ccfed2a27f4fc4a4233fd5e9b891378547'
    # me = 'Sarah911'
    urlAPI = 'https://api.github.com/users/' + user.split(" ")[0] + '/repos?per_page=10&page=2'
    pageAPI = requests.get(urlAPI, headers={'Authentification': token})
    index = df.index[df['User'] == user][0]
    if pageAPI.status_code == 200:
        json_text = json.loads(pageAPI.text)
        star_count = 0
        for text in json_text:
            star_count += int(text['stargazers_count'])
        if (len(json_text) == 0):
            df['Stars'][index] = 0
        else:
            df['Stars'][index] = star_count / len(json_text)
    else:
        print('The code error is ' + str(pageAPI.status_code))


df = get_users()
for user in df['User']:
    get_stars(user)
df.sort_values(by=['Stars'])
print(df.head())
