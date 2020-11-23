# Author: Remington Brandenburger
# Date created: September 2020
# Last Updated: October 2020
#
# Uses: 
# -Collect data from an attached DH22 temperature and humidity sensor
# -Compute related weather data
# -Send data in JSON format to a web server
#
# Dependencies: pysft, adafruitDHT drivers, requests, pytz
# use pip3 to install each dependency

from sensor import Sensor
from file_sender import Sender
from functions import Functions
from datetime import datetime
from ApiCaller import Forecast, Observation
import json
import time
import sys

if __name__ == "__main__":
        
    sensor = Sensor()
    sender = Sender()
    func = Functions()
    forecast = Forecast()
    observation = Observation()
    systemHour = -1
    actualHour = -1
    
    while(True):
        
        try:
            # Get current time info
            now = datetime.now()
            nowStr = now.strftime("%Y-%m-%dT%H:%M:%S")
            actualHour = now.hour
            actualMin = now.minute
            
            #Get the temperature in Celcius and humidity
            tempC, humidity = sensor.getReading()
            
            #Check for a bad reading from sensor
            if(humidity == 0.0 and tempC == 0.0):
                continue
                
            #Forecast updated hourly
            if(systemHour != actualHour):
               todaySummary,  sevenDayForecast, highLowTemps, sunrise, sunset = forecast.getData()
                
            #Check for a bad api call
            if(sevenDayForecast == None or sunrise == None):
                continue

            #Observations updated hourly
            if(systemHour != actualHour):
                windSpeed, windDirection, sky = observation.getData()

            #Check for a bad API Call
            if(windSpeed == None):
                continue

            weather = {
                'tempC' : tempC,
                'humidity' : humidity,
                'windSpeed' : windSpeed,
                'windDirection' : windDirection,
                'sky' : sky,
                'todaySummary' : todaySummary,
                'sevenDayForecast' : sevenDayForecast,
                'highLowTemps' : highLowTemps,
                'sunrise' : sunrise.strftime("%I:%M %p"),
                'sunset': sunset.strftime("%I:%M %p"),
                'timestamp' : nowStr
            }
            
            # Functions class holds math equation methods for getting certain relevant weather information
            weather['tempF'] = func.getFahrenheit(weather['tempC'])
            weather['dewPoint'] = func.getDewPoint(weather['tempC'], weather['humidity'])
            
            # NWS Reports heat index when temp greater than 80F, or wind chill when temp lower than 50F
            wind = float(weather['windSpeed'].replace(" mph", ""))
            
            if(weather['tempF'] > 80):
                weather['feelsLike'] =  func.getHeatIndex(weather['tempF'], weather['humidity'])
            
            elif(weather['tempF'] < 50 and wind >= 3):
                weather['feelsLike'] = func.getWindChill(weather['tempF'], wind)
            
            else:
                weather['feelsLike'] = None
            
            # Write to JSON file
            with open('/home/pi/WeatherSystem/data.json', 'w') as outfile:
                json.dump(weather, outfile, indent=4)
            
            # Send JSON file
            result = sender.send('/home/remipzuw/weatherApp','/home/pi/WeatherSystem/data.json')
            
            # Check for error
            if(result == 0):
                with open('log.txt', 'a') as log:
                    log.write('{} | There was an error with sending the file out\n'.format(now))
            else:
                print("Sent file successfully")
            # Update the system's hour
            systemHour = actualHour
            
            # Sleep for 5 mins (300 seconds)
            time.sleep(300) 

        except Exception as e:
            
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            print("Fatal error")
            print(e)
            
            with open('./WeatherSystem/log.txt', 'a') as log:
                log.write(timestamp + " Fatal error\n")
                log.write(repr(e) + "\n")
            
            exit()
