from django.db import models
import urllib, json, datetime, sys

# Create your models here.
class Weather:
    def __init__(self, zipcode, country_code):
        url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + country_code
        try:
            response = urllib.urlopen(url);
            data = json.loads(response.read())
        except:
            self.error_msg = "Could not connect to the weather report service!"
        else:
            if data["cod"] != 200:
                self.error_msg = "Could not load weather report for " + zipcode + ", " + country_code
            else:
                self.location = data["name"]
                self.temperature_celsius = float(data["main"]["temp"]) - 273.15
                self.temperature_fahrenheit = ((9.0/5.0) * self.temperature_celsius) + 32
                self.iconId = data["weather"][0]["icon"]
                self.description = data["weather"][0]["description"]

