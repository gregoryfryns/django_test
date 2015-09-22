from django.test import TestCase
from weather.models import AbstractWeatherReport, OpenWeatherMapReport

# Create your tests here.
class WeatherReportTests(TestCase):
    def test_correct_location_returned(self):
        """
        If a correct zip code is entered, openweathermap should return the weather report
        for this area.
        """
        weather = OpenWeatherMapReport('94025','US')
        weather.update()
        self.assertEqual(weather.location, 'West Menlo Park')

    def test_incorrect_zip_code_entered(self):
        """
        If an incorrect zip code is entered, an appropriate error message should be returned to the view
        """
        weather = OpenWeatherMapReport('X0000','XXX')
        weather.update()
        self.assertNotEqual(weather.error_msg, None)
