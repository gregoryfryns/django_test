from django.shortcuts import render
from weather.models import Weather

# Create your views here.
def weather(request):
    try:
        zipcode = request.GET['zipcode']
        country_code = request.GET['countrycode']
    except:
        zipcode = "94025"
        country_code = "US"

    weather_report = Weather(zipcode, country_code)
    context = {'weather_report': weather_report}
    return render(request, 'weather/index.html', context)

