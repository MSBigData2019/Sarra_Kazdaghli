import requests

url = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168'
page = requests.get(url)
print(page)

if (page.status_code == 200):
    text = page.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(page.content, 'html.parser')

seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())

# the name of forecast item, in this case tonight
print(" th name of the forecast item ", tonight.find(class_="period-name").get_text())

# The description of the conditions — this is stored in the title property of img.
# the title attribute from the img tag (treat the object of beautiful soup as a dictionnary and 'title' is a key
print(" The description of the conditions ", tonight.find("img")['title'])

# A short description of the conditions — in this case, Mostly Clear.
print(" A short description of the conditions ", tonight.find(class_="short-desc").get_text())

# The temperature low
print("The temperature low ", tonight.find(class_="temp temp-high").get_text())

# Select all items with the class period-name inside an item with the class tombstone-container in seven_day.
print(" Select all items with the class period-name inside an item with the class tombstone-container in seven_day",
      seven_day.select(' div.tombstone-container  p.period-name'))

# Use a list comprehension to call the get_text method on each BeautifulSoup object.
print([item.get_text() for item in seven_day.select(' div.tombstone-container  p.period-name')])

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)
