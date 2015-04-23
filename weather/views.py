from django.shortcuts import render
from weather.models import OpenWeatherMapReport

# Create your views here.
def weather(request):
    #TODO: create a proper form
    try:
        zipcode = request.GET['zipcode']
        country_code = request.GET['countrycode']
    except:
        if 'zipcode' in request.session:
            zipcode = request.session['zipcode']
        else:
          zipcode = "94025"

        if 'country_code' in request.session:
            country_code = request.session['country_code']
        else:
            country_code = "US"

    request.session['zipcode'] = zipcode
    request.session['country_code'] = country_code

    weather_report = OpenWeatherMapReport(zipcode, country_code)
    weather_report.update()

    error_msg = weather_report.get_error_msg()
    location = weather_report.get_location()
    temp_celsius = str(weather_report.get_temperature_celsius())
    temp_fahrenheit = str(weather_report.get_temperature_fahrenheit())
    icon_url = weather_report.get_icon_url()
    description = weather_report.get_description()

    context = {'error_msg': error_msg,
               'location': location,
               'temp_celsius': temp_celsius,
               'temp_fahrenheit': temp_fahrenheit,
               'icon_url': icon_url,
               'description': description,
               'zipcode': zipcode,
               'country_code': country_code
    }
    return render(request, 'weather/index.html', context)

