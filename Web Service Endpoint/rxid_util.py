import pytz
from pytz import timezone
import calendar
import datetime
import os

# _________ Parse API input string for parameters _________________
#  input->  sample API input string(s)-> /indentify/param1=Red&param2=Pill
#  ouputs -->  
def parse_input(s):
    weekday, hour = day_hour()
    # parse input string for model input values
    weather_str = ''
    weather_loc = s.find("weather=") # returns -1 if not found
    if weather_loc > 0:
        weather_str = s[s.find("weather=")+8:s.find("&",weather_loc)]

    day_str = ''
    day_loc = s.find("day=")
    if day_loc > 0:
        day_str = s[day_loc+4:s.find("&",day_loc)]

    month_num = 1
    month_loc = s.find("month=")
    if month_loc > 0:
        month_str = s[month_loc+7:s.find("&",month_loc)]
        month_str = s.find()
        month_num = 1
        month_dict = dict((v,k) for k,v in enumerate(calendar.month_name))
        for key, value in month_dict.items():
            if key == month_str:
                month_num = value

# _______ chromedriver test __________
def chromedriver_test():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/")
    element_text = driver.find_element_by_id("title").text
    return element_text

# _______ GET CURRENT DAY AND HOUR __________
def day_hour():
    # get current time in pacific timezone
    utc = pytz.utc
    utc.zone
    pacific = timezone('US/Pacific')
    #  bin the current hour
    time = datetime.datetime.today().astimezone(pacific)    
    hour = (time.hour)
    if hour <= 4:
        hour = 1
    elif 4 > hour <= 8:
        hour = 2
    elif 8 > hour <= 12:
        hour = 3
    elif 12 > hour <= 16:
        hour = 4
    elif 16 > hour <= 20:
        hour = 5
    else:
        hour = 6
    # Day of the week
    weekday = time.isoweekday()
    d = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 
        5: 'FRIDAY', 6: 'SATURDAY', 7: 'SUNDAY'}
    for key, value in d.items():
        if key == weekday:
            weekday = value
    return weekday, hour
