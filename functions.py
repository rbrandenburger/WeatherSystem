import math

class Functions():
    def getFahrenheit(self, tempC):
            
        tempF = (tempC * 1.8) + 32	
        return tempF
        
    def getDewPoint(self, temp, RH):
        
        #NOTE: Temp needs to be in Celcius
        dewPoint = temp - ((100.0 - RH) / 5.0)
        dewPoint = self.getFahrenheit(dewPoint)
        return dewPoint
        
    def getHeatIndex(self, temp, RH):
        
        #Note: Temp needs to be in Farenheit
        #Following formula from NOAA on computing the heat index
        
        #Compute simple formula and average with current temp
        heatIndex = 0.5 * (temp + 61.0 + ((temp - 68.0) * 1.2) + (RH * 0.094))
        heatIndex = (heatIndex + temp) / 2.0
        
        #If heat index is >80, then a more complex formula is needed...
        if (heatIndex > 80.0):
            
            heatIndex = -42.379 + (2.04901523 * temp) + (10.14333127 * RH) \
            - (0.22475541 * temp * RH) - (0.00683783 * temp * temp) - \
            (0.05481717 * RH * RH) + (0.00122874 * temp * temp * RH) + \
            (0.00085282 * temp * RH * RH) - (0.00000199 * temp * temp * RH * RH)
            
            # There are two possibly necessary adjustments that depend on certain
            # temperature and relative humidity combinations
            if ( RH < 13.0 and ( 80.0 < temp and 112.0 > temp)):
                
                adjustment = ((13.0 - RH) /  4.0) * math.sqrt((17.0 - abs(temp - 95.0)) / 17.0)
                heatIndex = heatIndex - adjustment
                
            elif ( RH > 85.0 and ( 80.0 < temp and 87.0 > temp)):
                
                adjustment = ((RH - 85.0) / 10) * ((87 - temp) / 5)
                heatIndex = heatIndex + adjustment
                
        return heatIndex
                
    def getWindChill(self, temp, windSpeed):
        
        #Note: temp needs to be in Farenheit and windSpeed in mph
        #Following formula from NWS on computing wind chill
        
        windChill = 35.74 + (0.6215 * temp) - (35.75 * (windSpeed**0.16)) + (0.4275 * temp * (windSpeed**0.16))
        
        return windChill
