import time
import datetime
from datetime import datetime
import board
import neopixel
import random
import os
import glob


pixel_pin = board.D18
num_pixels = 24
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

#Neopixelin värit
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

#Lämpötilasensorin conffi
temp=['sensor code','tttttttttt','ddddddddddd','ssssssssss']
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

def ColorFill():
	for i in range(num_pixels):
		pixels[i] = (100,10,10)
		pixels.show()
		time.sleep(0.1)

	time.sleep(2)

def Empty():
	for a in range(num_pixels):
		pixels[a] = (0,0,0)
		pixels.show()
		time.sleep(0.05)


def Stars(toistot):
	for i in range(toistot):
		rnd = random.randint(0,23)
		pixels[rnd] = (255,255,255)
		rnd2 = random.randint(0,23)
		pixels[rnd2] = (25,155,125)
		pixels.show()
		time.sleep(0.1)
		pixels[rnd] = (0,0,0)
		pixels[rnd2] = (0,0,0)
		pixels.show()


def Dot():
	pixels.fill(PURPLE)
	for i in range(num_pixels):
		pixels[i] = GREEN
		pixels.show()
		time.sleep(0.2)
		pixels[i] = PURPLE
		pixels.show()


def Kello():
	for i in range(30):
		now = datetime.now()
		hour = now.hour 
		minute = now.minute % 24
		second = now.second % 24
		print(hour, minute, second)
		
		pixels[0] = RED
		pixels[6] = YELLOW
		pixels[12] = GREEN
		pixels[18] = YELLOW
		
		pixels[hour] = (10,10,10)
		#pixels[num_pixels - hour-1] = (2,2,2)
		pixels[minute] = (0,0,10)
		#pixels[num_pixels - minute-1] = (0,0,2)
		pixels[second] = (0,10,10)
		#pixels[second-1] = (0,2,2)
		pixels.show()
		time.sleep(1)
		pixels[num_pixels - hour] = (0,0,0)
		#pixels[num_pixels - hour-1] = (0,0,0)
		pixels[num_pixels - minute] = (0,0,0)
		#pixels[num_pixels - minute-1] = (0,0,0)
		pixels[second] = (0,0,0)
		#pixels[second-1] = (0,0,0)
		pixels.show()


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')



def read_temp_raw(device_file): 
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file): # checks the temp recieved for errors

    lines = read_temp_raw(device_file)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # set proper decimal place for C
        temp = float(temp_string) / 1000.0
        # Round temp to 2 decimal points
        temp = round(temp, 1)
    # value of temp might be unknown here if equals_pos == -1
    return temp


def temp_color():
	device_file = device_folders[0]+ '/w1_slave'
	temp = read_temp(device_file)
	print(temp)
	if temp < 20.0:
		pixels.fill(CYAN)
		pixels.show()
	if temp > 20.0:
		pixels.fill(GREEN)
		pixels.show()
	if temp > 25.0:
		pixels.fill(RED)
		pixels.show()
	pixels.show()
	time.sleep(2)

#ColorFill()
#Empty()
#Stars(100)
#Dot()
#Kello()
temp_color()
time.sleep(3)
Empty()



