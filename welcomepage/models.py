from django.db import models
#from django.utils import timezone
import urllib, json, datetime

# Create your models here.
class Weather:
#    iconId = "01d"
#    sunrise = timezone.now()
#    sunset = timezone.now()
#    temperature = 298
#    location = "Ici"
#    description = "description"
    def __init__(self, zipcode, country_code):
        url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + country_code
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        self.location = data["name"]
        self.sunrise = datetime.datetime.fromtimestamp(int(data["sys"]["sunrise"])).strftime('%Y-%m-%d %H:%M:%S')
        self.sunset = datetime.datetime.fromtimestamp(int(data["sys"]["sunset"])).strftime('%Y-%m-%d %H:%M:%S')
        self.temperature = data["main"]["temp"]
        self.iconId = data["weather"][0]["icon"]
        self.description = data["weather"][0]["description"]
        
