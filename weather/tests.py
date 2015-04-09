from django.test import TestCase
from weather.models import Weather

# Create your tests here.
class WeatherReportTests(TestCase):
    def test_correct_location_returned(self):
        """
        If a correct zip code is entered, openweathermap should return the weather report
        for this area.
        """
        weather = Weather('94025','US')
        self.assertEqual(weather.location, 'Menlo Park')

    def test_incorrect_zip_code_entered(self):
        """
        If an incorrect zip code is entered, an appropriate error message should be returned to the view
        """
        weather = Weather('X0000','XXX')
        self.assertEqual(isinstance(weather.error_msg, str), True)
