import Adafruit_DHT

class Sensor():
	
	def __init__(self):
		self.pin = 14
		self.sensor = Adafruit_DHT.DHT22
	
	def getReading(self):
		
		humidity, temp = Adafruit_DHT.read_retry(self.sensor, self.pin)
		
		if humidity is None and temp is None :
			print("Error: No reading")
			return 0.0, 0.0
		else:
			return temp, humidity
