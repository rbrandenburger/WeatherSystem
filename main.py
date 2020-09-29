# Author: Remington Brandenburger
# Date created: September 2020
#
# Uses: 
# -Collect data from an attached DH22 temperature and humidity sensor
# -Compute related weather data
# -Send data in JSON format to a web server
#
# Dependencies: pysft, adafruitDHT drivers

from sensor import Sensor
from file_sender import Sender
from functions import Functions
from datetime import datetime
import json
import time

if __name__ == "__main__":
	
	sensor = Sensor()
	sender = Sender()
	func = Functions()
	
	while(True):
		
		tempC, humidity = sensor.getReading()
		
		if(humidity == 0.0 and tempC == 0.0):
			continue
			
		weather = {
			'tempC' : tempC,
			'humidity' : humidity
		}
		
		weather['tempF'] = func.getFahrenheit(weather['tempC'])
		weather['dewPoint'] = func.getDewPoint(weather['tempC'], weather['humidity'])
		weather['heatIndex'] =  func.getHeatIndex(weather['tempF'], weather['humidity'])
		
		#Delete later
		print("The temp is: {}C or {}F, and the humidity is: {}%".format(weather['tempC'], weather['tempF'], weather['humidity']))
		with open('log.txt', 'a') as log:
			log.write("The temp is: {}C or {}F, and the humidity is: {}%\n".format(weather['tempC'], weather['tempF'], weather['humidity']))
		
		#Write out file
		with open('data.json', 'w') as outfile:
			json.dump(weather, outfile)
		
		#Send json file
		result = sender.send('/home/remipzuw/weatherApp','data.json')
		
		#Check for error
		if(result == 0):
			now = datetime.now()
			with open('log.txt', 'a') as log:
				log.write('{} | There was an error with sending the file out\n'.format(now))
				
		#Sleep for 5 mins (300 seconds)
		time.sleep(300)
