import requests
import json
import datetime
import pytz
from pytz import timezone

# The forecast class gets the "Predictions" for the day
# This includes a seven day forecast with high and low temps
# Also, this class retrieves the sunrise and sunset time for the day
class Forecast():

    def getData(self):
        
        shortForecasts = {}
        highLowTemps = {}
        todaySummary = {}
        sunrise = None
        sunset = None

        try:
            # Url for getting local forecast data from Nation Weather Service API 
            url = "https://api.weather.gov/gridpoints/OAX/56,39/forecast"
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
            data = json.loads(requests.get(url, headers = headers).text)
            
            # NWS has the forecast and the high-low temps for the next seven days
            for x in data['properties']['periods']:
                name = x['name']
                forecast = x['shortForecast']
                temp = x['temperature']
                shortForecasts[name] = forecast
                highLowTemps[name] = temp

            #This is the detailed summary for the next 24 hours (two 12-hour summaries)
            todaySummary[data['properties']['periods'][0]['name']] =  data['properties']['periods'][0]['detailedForecast']
            todaySummary[data['properties']['periods'][1]['name']] = data['properties']['periods'][1]['detailedForecast']
        
        # Log if any problem with collecting data from NWS
        except Exception as e:
            print("Problem getting forecast from NWS")

            with open('./log.txt', 'a') as log:
                log.write("Problem getting forecast from NWS\n")
                log.write(repr(e))
            print(e)
            
            shortForecasts = None
            highLowTemps = None
            todaySummary = None
            
            
        # Getting the sunrise and sunset time
        try:
            # Initialization
            url = "https://api.sunrise-sunset.org/json?lat=40.806862&lng=-96.681679"
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
            data = json.loads(requests.get(url, headers = headers).text)
            today = datetime.date.today()

            # Getting sunrise 
            sunrise = data['results']['sunrise']
            sunrise = datetime.datetime.strptime(sunrise, '%I:%M:%S %p')

            # Setting the date and time zone for API
            sunrise = sunrise.replace(day=int(today.strftime("%d")))
            sunrise = sunrise.replace(month=int(today.strftime("%m")))
            sunrise = sunrise.replace(year=int(today.strftime("%Y")))
            sunrise = sunrise.replace(tzinfo=pytz.UTC)

            # Converting from UTC time to local time
            local_tz = timezone('America/Chicago')
            sunrise = sunrise.astimezone(local_tz)

            # Getting Sunset
            sunset = data['results']['sunset']
            sunset = datetime.datetime.strptime(sunset, '%I:%M:%S %p')

            # Setting the date and time zone for API
            sunset = sunset.replace(day=int(today.strftime("%d")))
            sunset = sunset.replace(month=int(today.strftime("%m")))
            sunset = sunset.replace(year=int(today.strftime("%Y")))
            sunset = sunset.replace(tzinfo=pytz.UTC)

            # Converting from UTC time to local time
            local_tz = timezone('America/Chicago')
            sunset = sunset.astimezone(local_tz)

        except Exception as e:
            print("Problem getting data from Sunrise-Sunset")

            with open('./log.txt', 'a') as log:
                log.write("Problem getting data from Sunrise-Sunset\n")
                log.write(repr(e))
            print(e)
            
            sunrise = None
            sunset = None
            
        return(todaySummary, shortForecasts, highLowTemps, sunrise, sunset)

# The observation class gets recent weather observations from the NWS
# This includes wind speed, wind direction, and a brief description of the weather
class Observation():
    
    def getData(self):

        try:
            
            # Url for getting local forecast data from Nation Weather Service API 
            url = "https://api.weather.gov/gridpoints/OAX/56,39/forecast/hourly"
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
            data = json.loads(requests.get(url, headers = headers).text)
            
            # Collecting some other data from the NWS that I currently cannot collect locally
            windSpeed = data['properties']['periods'][0]['windSpeed']
            windDirection = data['properties']['periods'][0]['windDirection']
            sky = data['properties']['periods'][0]['shortForecast']
            
            return (windSpeed, windDirection, sky)


        # Log any errors
        except Exception as e:
            print("Problem getting observations from NWS")

            with open('./log.txt', 'a') as log:
                log.write("Problem getting observations from NWS\n")
                log.write(repr(e))
            print(e)

            return (None, None, None)




