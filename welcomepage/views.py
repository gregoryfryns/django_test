from django.shortcuts import render
from welcomepage.models import Weather

# Create your views here.
def welcomepage(request):
    try:
        zipcode = request.GET['zipcode']
        country_code = request.POST['countrycode']
    except:
        zipcode = "94025"
        country_code = "US"

    weather_report = Weather(zipcode, country_code)
    context = {'weather_report': weather_report}
    return render(request, 'welcomepage/index.html', context)

