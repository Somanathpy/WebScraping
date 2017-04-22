import requests
from bs4 import BeautifulSoup
import pandas as pd

#accessing laredo,Texeas Weather Data
page = requests.get('http://forecast.weather.gov/MapClick.php?lat=27.5064&lon=-99.5075#.WPuHmfkrLIU')
response = page.content
#print(page.status_code) # printing status Code
#print(response) # printing content of the HTML

soup = BeautifulSoup(page.content,'html.parser')
#print(soup.prettify) #printing nicely with prettify

seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
#print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

#print(period) # checking the period
#print(short_desc) # checking short description
#print(temp) # checking temperature

img = tonight.find("img")
desc = img['title']

#print(desc) # checking short rescription extacted properly or not

# Extracting all the information at once

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
#print(periods) # checking the days extracted or not

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

# checking for each day
#print(short_descs)
#print(temps)
#print(descs)

# combining data in to DataFrame
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })
#print(weather) # checking the data Frame
 # using re to extract the numeric values of temp
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
#print(temp_nums)
#mean of teparature
#print(weather["temp_num"].mean())

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
#print(is_night)

print(weather[is_night])



