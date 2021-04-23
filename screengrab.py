import pyautogui
import time
import os
dir = "C:/Users/SERVER3-PC/Desktop/SFAlert/images/" # Set this directory
# GCW Factional Presence Window must be 650 pixels wide

def clearImagesSG():
	try:
		dir = 'images'
		if len(os.listdir(dir)) > 0:
			print("Deleting images...")
			for f in os.listdir(dir):
				rmvpth = os.path.join(dir, f)
				os.remove(rmvpth)
				print("Deleting file: " + rmvpth)
	except:
		print("Error while deleting files")

def grabScreenInfo(retry=False):
	y = 0
	try:
		windowtopleft = pyautogui.locateOnScreen('refimg.png',confidence=0.5,region=(0,0,600,250))
		windowtopright = pyautogui.locateOnScreen('refimg2.png',confidence=0.5)
		winwidth = windowtopright[0] + windowtopright[2]
		origin = windowtopleft[0]
		leftoffset = winwidth*0.0224
		rightoffset = winwidth*0.035
		topoffset = 150
		print("Window found")
		print("Gathering Screenshots...")
		while y <= 9:
			cell = (winwidth-leftoffset-rightoffset)/3
			# Location
			im = pyautogui.screenshot(region=(origin+leftoffset,topoffset+(y*20), cell, 15))
			path = dir+"name"+str(y)+".png"
			im.save(path)
			# Rebel
			im = pyautogui.screenshot(region=(origin+leftoffset+cell,topoffset+(y*20), 17, 15))
			path = dir+"reb"+str(y)+".png"
			im.save(path)
			# Imperial
			im = pyautogui.screenshot(region=(origin+leftoffset+(cell*2),topoffset+(y*20), 17, 15))
			path = dir+"imp"+str(y)+".png"
			im.save(path)
			y = y + 1
		print("Done")
	except:
		if retry == True:
			print("Could not find window after retry")
			clearImagesSG()
		else:
			delay = 2
			print("Could not find window, trying again in " + str(delay) + " seconds.")
			time.sleep(delay)
			grabScreenInfo(True)

grabScreenInfo()