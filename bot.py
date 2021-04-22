# bot.py
import os, re, os.path
from datetime import datetime
import discord
import asyncio
from dotenv import load_dotenv
import pyautogui
from PIL import ImageFile, Image
from pytesseract import *
import pyautogui
import time
pytesseract.tesseract_cmd = r'C:\\Users\\SERVER3-PC\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
from textgrab import *
from  screengrab import *

# Bot Initialization ----------
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# Arrays for restuss notifications
rebLast = list()
impLast = list()
rebLast.append(datetime.utcnow())
impLast.append(datetime.utcnow())

channels = [672912582247710734, 833815365708152843, 834224098858106890]

async def sendMessage(message):
	for c in channels:
		channel = client.get_channel(c)
		await channel.send(message)
async def sendEmbed(embed):
	for c in channels:
		channel = client.get_channel(c)
		await channel.send(embed=embed)

def clearImages():
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
# Bot Logic ----------
#async def my_background_task():
@client.event
async def on_message(message):
    if '!status' == message.content.lower():
    	await sendInfo(True, True, message.author)
    if '!status rebel' == message.content.lower() or '!status reb' == message.content.lower():
    	await sendInfo(True, False, message.author)
    if '!status imperial' == message.content.lower() or '!status imp' == message.content.lower():
    	await sendInfo(False, True, message.author)
    if '!help' == message.content.lower():
    	await sendMessage("To get all Special Forces info type '!status'\nTo Get only rebel or only imperial sf info type '!status reb' or '!status imp'\nSFAlert was created by **Brudr/Spe'k**")

        
async def sendInfo(rebel, imperial, author):
	if impGrab == {} or rebGrab == {}:
		await asyncio.sleep(1)
		await sendInfo(rebel, imperial)

	print("Retrieving Data...")
	impdesc = ""
	rebdesc = ""
	imptitle = "Imperial Special Forces - List of Locations"
	rebtitle = "Rebel Special Forces - List of Locations"
	# Check Rebels
	rebFound = False
	if len(rebGrab) == 0:
		rebdesc = "No special forces rebels anywhere in the galaxy"
		rebtitle = "No SF Rebels Found"
	else:
		for key, value in rebGrab.items():
			if rebGrab[key] == True:
					rebFound = True	
					rebdesc = rebdesc + key + "\n"
	if rebFound == False:
		rebdesc = "No special forces rebels anywhere in the galaxy"
		rebtitle = "No SF Rebels Found"

	# Check Imperials
	impFound = False
	if len(impGrab) == 0:
		impdesc = "No special forces imperials anywhere in the galaxy"
		imptitle = "No SF Imperials Found"
	else:
		for key, value in impGrab.items():
			if impGrab[key] == True:
					impFound = True	
					impdesc = impdesc + key + "\n"
	if impFound == False:
		impdesc = "No special forces imperials anywhere in the galaxy"
		imptitle = "No SF Imperials Found"

	if rebel == True:
		rebembed=discord.Embed(title=rebtitle, url="", description=rebdesc, color=discord.Color.red())
		rebembed.set_footer(text="Requested by: " + author.name + "\nFor command support  type !help")
		rebembed.timestamp = datetime.utcnow()
		rebembed.set_thumbnail(url="https://i.imgur.com/tQuxcCR.png")
		await sendEmbed(rebembed)
	if imperial == True:
		impembed=discord.Embed(title=imptitle, url="", description=impdesc, color=discord.Color.blue())
		impembed.set_footer(text="Requested by: " + author.name + "\nFor command support  type !help")
		impembed.timestamp = datetime.utcnow()
		impembed.set_thumbnail(url="https://i.imgur.com/4gTiklE.png")
		await sendEmbed(impembed)

async def my_background_task():
	await client.wait_until_ready()
	print("Starting background task in 5 seconds...")
	await asyncio.sleep(5)
	print("Background Task Started")
	while True:
		try:
			grabScreenInfo()
		except:
			print("Error grabbing gcw screen data. Clearing local data.")
			rebGrab.clear()
			print("Rebel data cleared")
			impGrab.clear()
			print("Imperial data cleared")
			try:
				clearImages()
			except:
				print("No more images to delete")
		await asyncio.sleep(2)
		print("Checking Presence...")
		try:
			checkPresence()
		except:
			print("Error checking presence, continuing...")
			continue
		print("Rebel Table:")
		print(rebGrab)
		print("Imperial Table:")
		print(impGrab)
		if len(rebLast) > 0:
			print("Last Rebel restuss update: " + str(rebLast[0]))
		if len(impLast) > 0:
			print("Last Imperial restuss update: " + str(impLast[0]))

async def rebel_restuss_task():
	await client.wait_until_ready()
	print("Starting Rebel Restuss Task in 5 seconds...")
	await asyncio.sleep(5)
	while True:
		print("Checking Restuss for Rebels...")
		rebrestuss = False

		# Check Rebels
		for key, value in rebGrab.items():
			if rebGrab[key] == True and "Restuss" in key:	
					rebrestuss = True
					break

		rebready = len(rebLast) > 0 and (((datetime.utcnow() - rebLast[0]).total_seconds() / 60.0) > 5)

		if rebrestuss == True and rebready:
			print("Rebels found in Restuss.")
			rebLast.clear()
			rebLast.append(datetime.utcnow())
			rebembed=discord.Embed(title="Rebels in Restuss :boom:", url="", description="Rebels detected in Restuss\nIf you do not want to receieve notifications, right click on the channel and mute it", color=discord.Color.red())
			rebembed.set_footer(text="For command support type !help")
			rebembed.timestamp = datetime.utcnow()
			rebembed.set_thumbnail(url="https://i.imgur.com/tQuxcCR.png")
			rebembed.set_author(name="Restuss Alert", url="", icon_url="https://i.imgur.com/JAorro3.png")
			await sendEmbed(rebembed)
		else:
			if not rebready and rebrestuss == True:
				print("Rebels found in restuss, but notification is on timer.")
			else:
				print("No Rebels found in Restuss.")

		await asyncio.sleep(10)

async def imperial_restuss_task():
	await client.wait_until_ready()
	print("Starting Imperial Restuss Task in 5 seconds...")
	await asyncio.sleep(5)
	while True:
		print("Checking Restuss for Imperials...")
		imprestuss = False

		# Check Imperials
		for key, value in impGrab.items():
			if impGrab[key] == True and "Restuss" in key:	
					imprestuss = True
					break

		impready = len(impLast) > 0 and (((datetime.utcnow() - impLast[0]).total_seconds() / 60.0) > 5)

		if imprestuss == True and impready:
			print("Imperials found in Restuss.")
			impLast.clear()
			impLast.append(datetime.utcnow())
			impembed=discord.Embed(title="Imperials in Restuss :boom:", url="", description="Imperials detected in Restuss\nIf you do not want to receieve notifications, right click on the channel and mute it", color=discord.Color.blue())
			impembed.set_footer(text="For command support type !help")
			impembed.timestamp = datetime.utcnow()
			impembed.set_thumbnail(url="https://i.imgur.com/4gTiklE.png")
			impembed.set_author(name="Restuss Alert", url="", icon_url="https://i.imgur.com/JAorro3.png")
			await sendEmbed(impembed)
		else:
			if not impready and imprestuss == True:
				print("Imperials found in restuss, but notification is on timer.")
			else:
				print("No Imperials found in Restuss.")
			
		await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.loop.create_task(my_background_task())
client.loop.create_task(rebel_restuss_task())
client.loop.create_task(imperial_restuss_task())

client.run(TOKEN)