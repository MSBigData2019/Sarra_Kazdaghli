import requests
import pandas as pd
import re

url = 'https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol'

pageAPI = requests.get(url)
if pageAPI.status_code:
    res = pageAPI.json()

df = pd.DataFrame([], columns=['Dosage', 'Labo', 'gélule/comprimé'])
for object in res:
    nom = object['denomination']
    reg = re.findall('(([\w]*){3})', nom)

    listOfObjects = nom.split(' ')
    labo = listOfObjects[1]
    dosage_list = re.findall('([0-9]+)', nom)
    if dosage_list:
        dosage = dosage_list[0]

    gélule = listOfObjects[len(listOfObjects) - 1]
    df2 = pd.DataFrame([[dosage, labo, gélule]], columns=['Dosage', 'Labo', 'gélule/comprimé'])
    df = df.append(df2, ignore_index=True)

print(df.head())
