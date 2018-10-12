import requests
from bs4 import BeautifulSoup

urlAcerPCBureau = 'https://www.darty.com/nav/recherche?s=relevence&text=acer&fa=790'
urlDellPCBureau = 'https://www.darty.com/nav/recherche?s=relevence&text=dell&fa=790'


def _convert_string_to_int(string):
    if "%" in string:
        test = string.replace('%', '')  #
        if "-" in string:
            test2 = test.replace('- ', '')
    return int(test2)


def moyenne(list):
    s = 0
    for elem in list:
        s = s + elem
    return (s / len(list))


def moyenneDesReduc(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        reduction_ordi = soup.find_all(class_='darty_prix_barre_remise darty_small separator_top')
        if (reduction_ordi):
            list = []
            for elem in reduction_ordi:
                list.append(_convert_string_to_int(elem.get_text()))
            return (moyenne(list))


print('Pour Acer les reduc sont de l\'ordre de ', moyenneDesReduc(urlAcerPCBureau))
print('Pour Dell les reduc sont de l\'ordre de ', moyenneDesReduc(urlDellPCBureau))
