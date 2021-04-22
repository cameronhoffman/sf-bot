import pyautogui
from PIL import ImageFile, Image
from pytesseract import *
import time
import asyncio
pytesseract.tesseract_cmd = r'C:\\Users\\SERVER3-PC\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

rebGrab = dict()
impGrab = dict()

def checkPresence():
	y = 0
	rebShort = {}
	impShort = {}
	noImages = True
	while y <= 9:
		try:
			nameimg = Image.open("images/" + "name" + str(y) + ".png")
		except:
			y = y + 1
			if y == 10 and noImages:
				print("No images found to delete, continuing...")
			continue
		noImages = False
		name = pytesseract.image_to_string(nameimg, lang='eng')
		#Replacements
		name = name.rstrip('\n\x0c')
		name = name.replace('$', 'S')
		name = name.replace('¥', 'V')
		name = name.replace("‘", "")
		name = name.replace('’', '')
		name = name.replace("'", "")
		name = name.replace(':', '')
		name = name.replace('.', '')
		#Common Replacements
		name = name.replace("Tatoo ", "Tatooine ")
		name = name.replace("Gutpost", "Outpost")

		#Stylization
		name = name.replace("Rori Restuss", "Rori Restuss :boom:")
		name = name.replace(" System", " System **(Space)**")

		if name == '' or name == ' ' or name.startswith(r"|") or name.startswith(r"\\"):
			y = y + 1
			continue

		reb = True
		imp = True
		try:
			rebx = pyautogui.locate('refx.png', "images/" + "reb" + str(y) + ".png")
		except:
			reb = False
		if rebx == None:
			reb = False
		try:
			impx = pyautogui.locate('refx.png', "images/" + "imp" + str(y) + ".png")
		except:
			imp = False
		if impx == None:
			imp = False

		impShort[name] = imp
		rebShort[name] = reb
		impGrab[name] = imp
		rebGrab[name] = reb

		y = y + 1

	for key, value in impGrab.copy().items():
			if not key in impShort:
				impGrab.pop(key)

	for key, value in rebGrab.copy().items():
			if not key in rebShort:
				rebGrab.pop(key)