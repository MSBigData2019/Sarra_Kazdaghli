import requests
from bs4 import BeautifulSoup
import re

prefix = 'https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque__'

def _convert_string_to_int(string):
    if "%" in string:
        number = string.replace('%', '')  #
        if "-" in string:
            numberInt = number.replace('- ', '')
    return int(numberInt)


def moyenne(list):
    s = 0
    for elem in list:
        s = s + elem
    if len(list) != 0:
        return (s / len(list))
    else:
        return 0


def moyenneDesReduc(url):
    i = 1
    listOfPages = []
    list = []

    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        currentPage = soup.find(class_='darty_product_list_pages_list')
        if (currentPage):
            listOfPages = re.findall('\d', currentPage.get_text())
        reduction_ordi = soup.find_all(class_='darty_prix_barre_remise darty_small separator_top')
        if (reduction_ordi):
            for elem in reduction_ordi:
                list.append(_convert_string_to_int(elem.get_text()))
    while i < len(listOfPages):
        if i > 1:
            url = url.replace('marque_' + str(i), 'marque_' + str(i + 1))
        else:
            url = url.replace('marque', 'marque_' + str(i + 1))
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            reduction_ordi = soup.find_all(class_='darty_prix_barre_remise darty_small separator_top')
            if (reduction_ordi):
                for elem in reduction_ordi:
                    list.append(_convert_string_to_int(elem.get_text()))
        i = i + 1
    return moyenne(list)


ListMarques = ['Acer', 'Dell', 'HP', 'Asus', 'Apple']
for marque in ListMarques:
    url = prefix + marque.lower() + '__' + marque.upper() + '.html'
    print('Pour ' + marque + ' les reduc sont de l\'ordre de ', moyenneDesReduc(url))
