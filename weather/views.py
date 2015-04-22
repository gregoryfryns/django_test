from django.shortcuts import render
from weather.models import AbstractWeatherReport, OpenWeatherMapReport

# Create your views here.
def weather(request):
    try:
        zipcode = request.GET['zipcode']
        country_code = request.GET['countrycode']
    except:
        zipcode = "94025"
        country_code = "US"

    weather_report = OpenWeatherMapReport(zipcode, country_code)
    weather_report.update()

    error_msg = weather_report.get_error_msg()
    location = weather_report.get_location()
    temp_celsius = str(weather_report.get_temperature_celsius())
    temp_fahrenheit = str(weather_report.get_temperature_fahrenheit())
    icon_url = weather_report.get_icon_url()
    description = weather_report.get_description()

    context = {'error_msg': error_msg, 'location': location, 'temp_celsius': temp_celsius,'temp_fahrenheit': temp_fahrenheit, 'icon_url': icon_url, 'description': description}
    return render(request, 'weather/index.html', context)

