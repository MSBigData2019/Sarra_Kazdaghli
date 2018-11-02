import requests
from bs4 import BeautifulSoup
import re
import base64
import unidecode
import numpy as np
import pandas as pd
import json

prefix = 'https://www.lacentrale.fr/'
url = prefix + 'listing?makesModelsCommercialNames=RENAULT%3AZOE&regions='
# FR-IDF
request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive"
}


def get_soup_from_url(url, headers):
    page = requests.get(url, headers=headers);
    if (page.status_code == 200):
        return BeautifulSoup(page.content, 'html.parser')
    else:
        return None


def formPrix(prix):
    prix_ascii = str(prix.get_text().encode("ascii", "ignore"))
    prix_chiffre = re.findall('([0-9]+)', prix_ascii)
    vrai_prix = int(prix_chiffre[0])
    return vrai_prix


def findTelephone(voiture):
    adresse_annonce = voiture.find('a')['href']
    url_adresse_annonce = prefix + adresse_annonce
    soup_annonce = get_soup_from_url(url_adresse_annonce, request_headers)
    telephone = soup_annonce.find(class_='phoneNumber1')
    telephone_tuple = re.findall('(0[0-9]((\s[0-9]{2}){4}))', telephone.get_text())[0]
    telephone_only = [x.encode('ascii', 'ignore') for x in telephone_tuple]
    final_telephone = telephone_only[0].decode('utf-8')
    return final_telephone


def findArgus(version, annee):
    cote = prefix + 'cote-auto-renault-zoe-' + version.replace(' ', '+') + '-' + annee + '.html'
    soup = get_soup_from_url(cote, request_headers)
    if soup:
        argus = soup.find(class_="jsRefinedQuot")
        if argus is not None:
            argus = argus.get_text().strip().replace(' ', '')
        else:
            argus = "None"
    return argus


def traitement(url, region, page):
    df3 = pd.DataFrame([],
                       columns=["Version", "Année", "Prix", "Téléphone du propriétaire", "pro ou particulier", "Argus"])
    soup = get_soup_from_url(url + '&page=' + str(page), request_headers)
    if soup:
        table = soup.find_all(class_='adContainer')
        if table:
            for voiture in table:
                version = voiture.find(class_='version txtGrey7C noBold')
                if version:
                    version = version.get_text()
                    annee = voiture.find(class_='fieldYear').get_text()
                    argus = findArgus(version, annee)
                    prix = voiture.find(class_='fieldPrice sizeC')
                    if prix:
                        prix = formPrix(prix)
                    pro_ou_part = voiture.find(class_='txtBlack typeSeller hiddenPhone').get_text()
                    telephone = findTelephone(voiture)

                    df2 = pd.DataFrame([[version, annee, prix, telephone, pro_ou_part, argus]],
                                       columns=["Version", "Année", "Prix", "Téléphone du propriétaire",
                                                "pro ou particulier", "Argus"])
                    df3 = df3.append(df2, ignore_index=True)
    return df3


def SummaryByRegion(url, region):
    urlRegion = url + region
    soup = get_soup_from_url(urlRegion, request_headers)
    df = pd.DataFrame([],
                      columns=["Version", "Année", "Prix", "Téléphone du propriétaire", "pro ou particulier", "Argus"])
    if soup:
        finalPage = soup.find(class_='rch-pagination').find(class_='last')
        if finalPage:
            if finalPage.getText() == '...':
                final = 9
            else:
                final = int(finalPage.getText())
            for page in np.arange(final):
                df_temp = traitement(urlRegion, region, page)
                df = df.append(df_temp, ignore_index=True)
        print('Pour la région ' + region, ': ', df.head())


SummaryByRegion(url, 'FR-IDF')
SummaryByRegion(url, 'FR-PAC')
SummaryByRegion(url, 'FR-NAQ')
