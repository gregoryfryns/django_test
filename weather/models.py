from django.db import models
import urllib, json, datetime, sys

# Create your models here.
class AbstractWeatherReport(object):
    """Abstract class for weather reports. Assumes that correct zip code and country code are passed to the initializer"""
    def __init__(self, zipcode, country_code):
        self.zipcode = zipcode
        self.country_code = country_code
        self.error_msg = None
        self.location = ""
        self.temperature_kelvin = 0
        self.iconUrl = ""
        self.description = ""

    def has_error(self):
        return not self.error_msg == None

    def get_error_msg(self):
        return self.error_msg

    def get_location(self):
        return self.location

    def get_temperature_kelvin(self):
        return self.temperature_kelvin

    def get_temperature_celsius(self):
        return self.temperature_kelvin - 273.15

    def get_temperature_fahrenheit(self):
        return ((9.0/5.0) * self.get_temperature_celsius()) + 32

    def get_icon_url(self):
        return self.iconUrl

    def get_description(self):
        return self.description

    def update(self):
        raise NotImplementedError("Method not implemented")


class OpenWeatherMapReport(AbstractWeatherReport):
    """Implementation of the AbstractWeatherReport class using the Open Weather Map api: http://openweathermap.org/api"""
    def __init__(self, zipcode, country_code):
        super(OpenWeatherMapReport, self).__init__(zipcode, country_code)
        self.service_base_url = "http://api.openweathermap.org/data/2.5/weather?zip=%s,%s"
        self.icon_base_url = "http://openweathermap.org/img/w/%s.png"

    def update(self):
        url = self.service_base_url % (self.zipcode, self.country_code)
        try:
            response = urllib.urlopen(url);
            data = json.loads(response.read())
        except:
            self.error_msg = "Could not connect to http://api.openweathermap.org/, please try again!"
        else:
            if data["cod"] != 200:
                self.error_msg = data["cod"] + " - " + data["message"]
            else:
                self.location = data["name"]
                self.temperature_kelvin = float(data["main"]["temp"])
                self.iconUrl = self.icon_base_url % (data["weather"][0]["icon"])
                self.description = data["weather"][0]["description"]

