"""
Author: Talyn Propst
Date: 20240311
Contact: tpropst@aerosurvey.com
Allsky Camera Heater Control
This program controls a heater for an All Sky camera heater ring that starts 
at sunrise the heater goes for 1 hour after sunrise to prevent fogging of dome.
"""
from gpiozero import OutputDevice
from pysolar.solar import *
import datetime
from time import sleep

#Variables
GPIO18 = OutputDevice(18) #GPIO Output for Raspberri Pi
heater_state = 0
latitude = ##.##### Enter Your Latitude
longitude = ##.#####Enter Your Longitude

#Returns current sun altitude which is an angle
def sun_altitude_current():
    my_utc_time = datetime.datetime.now().astimezone(datetime.timezone.utc)
    date_for_current_altitude = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, 
												datetime.datetime.now().day, int(my_utc_time.hour),
												int(my_utc_time.minute), tzinfo=datetime.timezone.utc)
    raw_result = float(get_altitude(latitude, longitude, date_for_current_altitude))
    rounded_result = round(raw_result,3)
    return rounded_result

#Returns Local Time
def current_local_time():
    return datetime.datetime.now()

#Returns if time is AM or PM
def am_or_pm():    
    return str(current_local_time().strftime("%p"))

#While loop to continously run (Loops at 1 min interval)
while True:
	#Says that if sun angle is bwetween -0.5 and 0.5 and time is AM then enter statement
	if((sun_altitude_current() > -0.5 and sun_altitude_current() < 0.5) and am_or_pm() == "AM"):
		start_hour = current_local_time().hour
		start_min = current_local_time().minute
		sleep(60)

		#Takes current time and determines 1 hour from when sunrise time is. Which is recorded when entering the previous if statement
		while((current_local_time().hour-start_hour == 0 or current_local_time().hour-start_hour == 1) and current_local_time().minute-start_min != 0):
			GPIO18.on() #Turns Raspberry Pi Pin On
			heater_state = 1 #State for troubleshooting
			sleep(60)
	else:
		GPIO18.off() #Turns Raspberry Pi Pin Off
		heater_state = 0
		sleep(60) #1 Minute Interval