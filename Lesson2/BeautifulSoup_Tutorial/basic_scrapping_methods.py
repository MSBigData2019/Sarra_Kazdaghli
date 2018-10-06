import requests

# Download a web page simulating a get request
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")

# print a response object
print("the response object is ")
print(page)

# the response has a status_code: if the page was downloaded successfully
print("\n")
print("the download response status is ")
print(page.status_code)

# print the html content
print("\n")
print("the page content is ")
print(page.content)

###############################      Parsing a page with BeautifulSoup      #############################################
from bs4 import BeautifulSoup

# create an instance of the library
soup = BeautifulSoup(page.content, 'html.parser')

# print the content of page formatted nicely
print("\n")
print("the page content prettier is  ")
print(soup.prettify())

# the top level elements of the page : call list on it because .children returns a list generator
print("\n")
print("the soup children are ")
print(list(soup.children))  # we find the intial tag <!DOCTYPE html> , and the <html> tag and also the line return

# see the type of each element in the top level element
# [<class 'bs4.element.Doctype'>, <class 'bs4.element.NavigableString'>, <class 'bs4.element.Tag'>]
print("\n")
print("the types of each element in soup.children are ")
print([type(item) for item in list(soup.children)])

# select the most important type which is the tag type which has the html
print("\n")
print("print the html: contained in soup.children list ")
html = list(soup.children)[2]
print(html)

# now, we search for children in the html tag
print("\n")
print("children in the html tag are ")
print(list(html.children))

# wanting to extract the text in the p tag:
print("\n")
print("the text in the p tag is ")
body = list(html.children)[3]
p = list(body.children)[1]
print(p.get_text())

#################################### Finding all instances of a tag at once ############################################

# Find all instance of the tag p
print("\n")
print(" all instances of p")
print(soup.find_all('p'))

# read the text on one instance of p
print("\n")
print("the text on p instance ")
print(soup.find_all('p')[0].get_text())

# find the first instance of a tag (p)
print("\n")
print("the text of the first instance of p is ")
print(soup.find('p').get_text())

#############################    Searching for tags by class and id #################################################

print("\n")
page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')

# find the tag and filter by class or id
print(" the instance for a tag p for a specific class ")
p = soup.find_all('p', class_='outer-text')
print(p[0].get_text())

# find all instances by a specific class
print("\n")
print("the instances for a specific class")
print(soup.find_all(class_='outer-text'))

# find all instances for a specific id
print("\n")
print("the instances for a specific id")
print(soup.find_all(id='first'))

###########################    Using CSS Selectors   ###########################################################


# p a — finds all a tags inside of a p tag.
# body p a — finds all a tags inside of a p tag inside of a body tag.
# html body — finds all body tags inside of an html tag.
# p.outer-text — finds all p tags with a class of outer-text.
# p  # first — finds all p tags with an id of first.
# body p.outer-text — finds any p tags with a class of outer-text inside of a body tag.

print("\n")
print(" select in the soup all the p tags inside a div => returns a list")
print(soup.select("div p"))
