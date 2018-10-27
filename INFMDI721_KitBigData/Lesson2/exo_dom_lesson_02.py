import requests
from bs4 import BeautifulSoup
import re

prefix = 'https://www.reuters.com/finance/stocks/financial-highlights/'


# les ventes au quartier à fin décembre 2018
# Sales for Quarter Ending Dec-18

## Method 1: Not a perfect method
def findSalesForQuarterDec18_meth1(soup):
    sectionHeader = soup.find(class_="dataTable").find(class_="stripe").find_all("td", class_="data")
    if sectionHeader:
        print("1rst Method : Estimate of sales in Quarter Ending Dec-18 is " + sectionHeader[1].get_text())
    else:
        print('Oups we cannot find th section header')


## Method 2: a better filtering
def findSalesForQuarterDec18_meth2(soup):
    SalesEndQuarterDec18 = listOfStripesInTable[0].select(" .data")[1].get_text()
    print("2nd method : Estimate of sales in Quarter Ending Dec-18 is " + SalesEndQuarterDec18)


# le prix de l'action et son % de changement au moment du crawling
# Price of an action and percentage of change at the crawling

def findPriceAndPercOfAction(soup):
    values = soup.find(id="headerQuoteContainer").find(class_="sectionQuote priceChange").find(
        class_="sectionQuoteDetail")

    if values:
        priceOfAction = values.find(class_="valueContent").find(class_="neg")
        if (priceOfAction):
            print("Price of action is " + priceOfAction.get_text().strip())
        else:
            print("oups we cannot find the price of action")

        priceChange = values.find(class_="valueContentPercent")
        if priceChange:
            print("The percentage of change is " + priceChange.get_text().strip())
        else:
            print("oups we cannot find the percentage of change")
    else:
        print("oups we cannot find the section with action values")


# le % Shares Owned des investisseurs institutionels
# Percentage of shares for institutional holders
def findPercOfSharesInstHolders(soup):
    percentageOfInstShares = " "
    for s in listOfStripesInTable:
        listOfTd = s.select("td")
        for td in listOfTd:
            if (td.get_text() == '% Shares Owned:'):
                percentageOfInstShares = s.select(" .data")[0].get_text()
                print("The percentage of shares for institutional holders is " + percentageOfInstShares)


# le dividend yield de la company, le secteur et de l'industrie
# Dividend yield of the company, sector and industry
def findDividendYield(soup):
    dyCompany = ""
    dySector = ""
    dyIndustry = ""
    for s in listOfStripesInTable:
        listOfTd = s.select("td")
        for td in listOfTd:
            if (td.get_text() == 'Dividend Yield'):
                dyCompany = s.select(" .data")[0].get_text()
                dySector = s.select(" .data")[1].get_text()
                dyIndustry = s.select(" .data")[2].get_text()

    print("Dividend Yield Of Company is " + dyCompany)
    print("Dividend Yield Of Sector is " + dySector)
    print("Dividend Yield Of Industry is " + dyIndustry)


listCompanies = ['AIR.PA', 'LVMH.PA', 'DANO.PA']
for company in listCompanies:
    url = prefix + company
    page = requests.get(url)
    print("\n")
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        print(" this is the financial highlights for " + company)
        listOfStripesInTable = soup.select("#content .sectionContent .sectionColumns .dataTable .stripe ")
        if listOfStripesInTable:
            findSalesForQuarterDec18_meth1(soup)
            findSalesForQuarterDec18_meth2(soup)
            findPriceAndPercOfAction(soup)
            findPercOfSharesInstHolders(soup)
            findDividendYield(soup)
        else:
            print("oups we cannot find the list of stripes in the table")
    else:
        print("Page not loaded for " + company)
